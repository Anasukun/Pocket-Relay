import re

REDACTION_PATTERNS = [
    # Telegram Bot Token
    (r"\b[0-9]{8,10}:[A-Za-z0-9_-]{35}\b", "[REDACTED_TELEGRAM_TOKEN]"),
    # GitHub Personal Access Token
    (r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,255}\b", "[REDACTED_GITHUB_TOKEN]"),
    # GitHub Fine-grained PAT
    (r"\bgithub_pat_[A-Za-z0-9_]{82}\b", "[REDACTED_GITHUB_TOKEN]"),
    # AWS Access Key ID
    (r"\b(AKIA|ASIA)[0-9A-Z]{16}\b", "[REDACTED_AWS_KEY]"),
    # Private Key Block
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (RSA |EC |OPENSSH )?PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]"),
    # Generic Bearer Header
    (r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", "Bearer [REDACTED_TOKEN]"),
    # Database Connection Strings with Passwords
    (r"(postgres|postgresql|mysql|mongodb)://[^:]+:([^@]+)@", r"\1://[REDACTED_USER]:[REDACTED_PASSWORD]@"),
]

def redact_secrets(text: str) -> str:
    if not text:
        return ""
    sanitized = text
    for pattern, replacement in REDACTION_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.MULTILINE | re.DOTALL)
    return sanitized
