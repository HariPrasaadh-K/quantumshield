import os
from typing import List, Dict, Any
from app.scanners.base import BaseScanner
from app.utils.file_utils import MANIFEST_FILENAMES, safe_read_lines, get_surrounding_context
from app.utils.crypto_patterns import MANIFEST_DEPENDENCIES

class LibraryScanner(BaseScanner):
    def __init__(self):
        super().__init__(name="Manifest Library Scanner", language="Manifest")

    def can_scan(self, file_path: str) -> bool:
        filename = os.path.basename(file_path).lower()
        return filename in MANIFEST_FILENAMES

    def scan_file(self, file_path: str, relative_path: str) -> List[Dict[str, Any]]:
        findings = []
        filename = os.path.basename(file_path).lower()
        lines, truncated = safe_read_lines(file_path)
        if truncated or not lines:
            return findings

        # Check known package lists for this manifest type
        target_key = "pom.xml" if "pom" in filename else ("package.json" if "package" in filename else "requirements.txt")
        known_pkgs = MANIFEST_DEPENDENCIES.get(target_key, [])

        full_text = "".join(lines).lower()

        for line_idx, line_content in enumerate(lines):
            line_num = line_idx + 1
            line_lower = line_content.lower()

            for pkg_info in known_pkgs:
                pkg_name = pkg_info["package"].lower()
                if pkg_name in line_lower:
                    context = get_surrounding_context(lines, line_num)
                    
                    # Lower confidence because library presence is not proof of active crypto usage
                    findings.append({
                        "detector": self.name,
                        "file_path": relative_path,
                        "line_number": line_num,
                        "matched_text": line_content.strip(),
                        "surrounding_context": context,
                        "language": "Manifest",
                        "algorithm_hint": pkg_info["algorithm"],
                        "library_hint": f"{pkg_info['package']} ({pkg_info['hint']})",
                        "confidence": 0.40,
                        "metadata": {
                            "manifest_file": filename,
                            "package": pkg_info["package"],
                            "hint": pkg_info["hint"],
                            "usage_confirmed": False
                        }
                    })

        return findings
