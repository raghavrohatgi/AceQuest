"""
ARI Grammar Checker — Phase 4
Connects to the public LanguageTool API for lightweight grammar and spell checking.
"""

import json
import urllib.parse
import urllib.request
from typing import List, Dict, Any

LANGUAGETOOL_API_URL = "https://api.languagetoolplus.com/v2/check"

def check_grammar(text: str) -> List[Dict[str, Any]]:
    """
    Check the provided text for grammar and spelling errors using the public LanguageTool API.
    
    Returns a simplified list of issues finding within the text, including the
    error message, context string, and suggested replacements.
    """
    if not text or not text.strip():
        return []

    data_encoded = urllib.parse.urlencode({
        "text": text,
        "language": "en"  # Using base English to cover both IN/UK/US spellings broadly
    }).encode("utf-8")
    
    req = urllib.request.Request(LANGUAGETOOL_API_URL, data=data_encoded)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            out = json.loads(response.read().decode("utf-8"))
            
            issues = []
            for match in out.get("matches", []):
                # Only take up to 3 replacements for brevity
                replacements = [r["value"] for r in match.get("replacements", [])][:3]
                
                issues.append({
                    "message": match.get("message", "Potential error"),
                    "context": match.get("context", {}).get("text", ""),
                    "replacements": replacements
                })
                
            return issues
            
    except Exception as e:
        # If the API is purely unreachable (e.g. rate limit / network error),
        # return an empty array rather than breaking the application pipeline.
        print(f"[ARI Grammar] Failed to contact LanguageTool API: {e}")
        return []
