import re

SUPPLIER_PATTERNS = [
    r"supplier",
    r"manufacturing partner",
    r"depends on",
    r"third-party worker"
]

def extract_relationships(text):
    matches = []

    for pattern in SUPPLIER_PATTERNS:
        found = re.finditer(pattern, text, re.IGNORECASE)
        for match in found:
            start = max(0, match.start() - 200)
            end = min(len(text), match.end() + 200)
            context = text[start:end]
            matches.append({
                "pattern": pattern,
                "context": context
            })
    
    return matches