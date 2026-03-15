"""
PII detection and redaction for chat messages.
Replicates the PHP chat filter logic from UKQuranAcademy_CurrentPHPProject.
"""
import re
from typing import Tuple, List

# Patterns to detect
PATTERNS = {
    'email': re.compile(
        r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
        re.IGNORECASE
    ),
    'phone_pk': re.compile(
        r'(?:0|\+?92)[\s\-]?3[0-9]{2}[\s\-]?[0-9]{7}',
    ),
    'phone_intl': re.compile(
        r'(?:\+|00)[1-9][0-9]{1,3}[\s\-]?(?:\([0-9]{1,4}\)[\s\-]?)?[0-9]{4,14}(?:x[0-9]+)?',
    ),
    'phone_generic': re.compile(
        r'\b0[0-9]{9,12}\b',
    ),
    'url': re.compile(
        r'(?:https?://|www\.)[^\s\'"<>()]+',
        re.IGNORECASE
    ),
    'whatsapp': re.compile(
        r'(?i)(?:whatsapp|whats\s*app|wa\.me/|wa\s*number|add\s+me\s+on\s+whatsapp)',
    ),
}

BLOCK_LABEL = '[BLOCKED]'


def redact(text: str) -> Tuple[str, bool, List[str]]:
    """
    Scan `text` for PII patterns and replace them with [BLOCKED].

    Returns:
        (clean_text, was_blocked, patterns_found)
        - clean_text: text with PII replaced; equals original if no PII found
        - was_blocked: True if any pattern matched
        - patterns_found: list of pattern keys that matched
    """
    patterns_found: List[str] = []
    modified = text

    for name, pattern in PATTERNS.items():
        if pattern.search(modified):
            patterns_found.append(name)
            modified = pattern.sub(BLOCK_LABEL, modified)

    was_blocked = bool(patterns_found)
    return modified, was_blocked, patterns_found
