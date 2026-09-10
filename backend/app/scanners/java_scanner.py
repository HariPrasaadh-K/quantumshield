import re
from typing import List, Dict, Any
from app.scanners.base import BaseScanner
from app.utils.file_utils import JAVA_EXTENSIONS, safe_read_lines, get_surrounding_context
from app.utils.crypto_patterns import JAVA_PATTERNS

class JavaScanner(BaseScanner):
    def __init__(self):
        super().__init__(name="Java Static Scanner", language="Java")

    def can_scan(self, file_path: str) -> bool:
        return any(file_path.endswith(ext) for ext in JAVA_EXTENSIONS)

    def scan_file(self, file_path: str, relative_path: str) -> List[Dict[str, Any]]:
        findings = []
        lines, truncated = safe_read_lines(file_path)
        if truncated or not lines:
            return findings

        for line_idx, line_content in enumerate(lines):
            line_num = line_idx + 1
            
            # First check specific API getInstance calls
            for pattern_obj in JAVA_PATTERNS:
                regex = pattern_obj["pattern"]
                matches = re.finditer(regex, line_content, re.IGNORECASE)
                
                for match in matches:
                    matched_text = match.group(0)
                    algorithm_hint = None
                    library_hint = None
                    confidence = 0.95
                    
                    if pattern_obj["type"] == "api" and match.groups():
                        algorithm_hint = match.group(1).upper()
                    elif "algorithm" in pattern_obj:
                        algorithm_hint = pattern_obj["algorithm"]

                    if "BouncyCastle" in matched_text:
                        library_hint = "Bouncy Castle Provider"

                    context = get_surrounding_context(lines, line_num)
                    
                    findings.append({
                        "detector": self.name,
                        "file_path": relative_path,
                        "line_number": line_num,
                        "matched_text": matched_text,
                        "surrounding_context": context,
                        "language": self.language,
                        "algorithm_hint": algorithm_hint or "Unknown",
                        "library_hint": library_hint,
                        "confidence": confidence,
                        "metadata": {
                            "pattern_name": pattern_obj["name"],
                            "pattern_type": pattern_obj["type"]
                        }
                    })

        return findings
