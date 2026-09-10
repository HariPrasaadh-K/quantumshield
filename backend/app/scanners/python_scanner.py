import re
from typing import List, Dict, Any
from app.scanners.base import BaseScanner
from app.utils.file_utils import PYTHON_EXTENSIONS, safe_read_lines, get_surrounding_context
from app.utils.crypto_patterns import PYTHON_PATTERNS

class PythonScanner(BaseScanner):
    def __init__(self):
        super().__init__(name="Python Static Scanner", language="Python")

    def can_scan(self, file_path: str) -> bool:
        return any(file_path.endswith(ext) for ext in PYTHON_EXTENSIONS)

    def scan_file(self, file_path: str, relative_path: str) -> List[Dict[str, Any]]:
        findings = []
        lines, truncated = safe_read_lines(file_path)
        if truncated or not lines:
            return findings

        for line_idx, line_content in enumerate(lines):
            line_num = line_idx + 1
            
            for pattern_obj in PYTHON_PATTERNS:
                regex = pattern_obj["pattern"]
                matches = re.finditer(regex, line_content, re.IGNORECASE)
                
                for match in matches:
                    matched_text = match.group(0)
                    algorithm_hint = None
                    library_hint = None
                    confidence = 0.90
                    
                    if "hashlib" in matched_text:
                        library_hint = "hashlib (Standard Library)"
                        if match.groups():
                            algo_grp = [g for g in match.groups() if g]
                            if algo_grp:
                                algorithm_hint = algo_grp[-1].upper()
                    elif "cryptography" in matched_text:
                        library_hint = "pyca/cryptography"
                    elif "Crypto" in matched_text:
                        library_hint = "PyCryptodome / PyCrypto"
                    elif "ssl" in matched_text:
                        library_hint = "ssl (Standard Library)"

                    if not algorithm_hint and "algorithm" in pattern_obj:
                        algorithm_hint = pattern_obj["algorithm"]

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
