"""Remove anything that looks like a secret before text leaves this machine."""

import re

REDACTED = "[REDACTED]"

# Each pattern matches one kind of secret. They are deliberately broad: hiding
# a harmless string is better than sending a real key to an outside service.
SECRET_PATTERNS = [
    # Private key blocks, for example "-----BEGIN RSA PRIVATE KEY-----".
    re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
        re.DOTALL,
    ),
    # Well-known key formats: OpenAI, Anthropic, GitHub, Slack, AWS, Google.
    re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}"),
    # JSON Web Tokens: three dot-separated parts starting with "eyJ".
    re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}"),
    # "Authorization: Bearer <token>" and similar.
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-~+/]{16,}=*"),
    # 32-character hex IDs, such as Cloudflare account and zone IDs. Git
    # commit hashes are 40 characters, so they are kept.
    re.compile(r"\b[0-9a-f]{32}\b"),
]

# `.env` style lines and JSON fields whose name suggests a secret, for example
# OPENAI_API_KEY=..., "accessToken": "...", password: ...
NAMED_SECRET = re.compile(
    r"""(?ix)
    (?P<name>[A-Za-z0-9_\-]*(?:api[_-]?key|token|secret|password|passwd|private[_-]?key)[A-Za-z0-9_\-]*)
    (?P<sep>["']?\s*[:=]\s*["']?)
    (?P<value>[^\s"',;]{8,})
    """
)

# Long random-looking strings that mix upper case, lower case and digits.
# Git commit hashes and UUIDs are lower case only, so they are kept. "/" is
# not allowed, so file paths such as /home/chris/projects/Docs/1.md are kept.
LONG_MIXED = re.compile(r"\b(?=[A-Za-z0-9_\-+]*[A-Z])(?=[A-Za-z0-9_\-+]*[a-z])(?=[A-Za-z0-9_\-+]*[0-9])[A-Za-z0-9_\-+]{40,}={0,2}")


def redact_secrets(text: str) -> tuple[str, int]:
    """Return the text with secrets replaced, and how many were replaced."""
    count = 0

    def replace(_match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return REDACTED

    def replace_value(match: re.Match[str]) -> str:
        nonlocal count
        if match.group("value") == REDACTED:
            return match.group(0)
        count += 1
        return f"{match.group('name')}{match.group('sep')}{REDACTED}"

    for pattern in SECRET_PATTERNS:
        text = pattern.sub(replace, text)
    text = NAMED_SECRET.sub(replace_value, text)
    text = LONG_MIXED.sub(replace, text)
    return text, count
