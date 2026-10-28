"""Secrets must be removed before any text is sent to OpenAI."""

from session_docs.redaction import REDACTED, redact_secrets


def test_removes_common_key_formats() -> None:
    samples = [
        "sk-proj-abcdefghijklmnopqrstuvwx1234",
        "ghp_abcdefghijklmnopqrstuvwxyz0123456789",
        "github_pat_11ABCDEFG0123456789_abcdefghijklmnop",
        "xoxb-1234567890-abcdefghij",
        "AKIAABCDEFGHIJKLMNOP",
        "0123456789abcdef0123456789abcdef",
        "AIzaSyA1234567890abcdefghijklmnopqrstuv",
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijk",
    ]
    for secret in samples:
        text, count = redact_secrets(f"here it is: {secret} thanks")
        assert secret not in text, secret
        assert count >= 1


def test_removes_env_lines_and_named_fields() -> None:
    text, count = redact_secrets(
        "OPENAI_API_KEY=abc123def456ghi\n"
        'CLOUDFLARE_API_TOKEN="tok_live_9999xxxx"\n'
        '{"accessToken": "short-but-secret-value"}\n'
        "password: hunter2hunter2"
    )
    assert "abc123def456ghi" not in text
    assert "tok_live_9999xxxx" not in text
    assert "short-but-secret-value" not in text
    assert "hunter2hunter2" not in text
    assert "OPENAI_API_KEY=" + REDACTED in text
    assert count == 4


def test_removes_bearer_tokens_and_private_keys() -> None:
    text, _ = redact_secrets(
        "Authorization: Bearer abcDEF123456ghiJKL789\n"
        "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg\n-----END PRIVATE KEY-----"
    )
    assert "abcDEF123456ghiJKL789" not in text
    assert "MIIEvQIBADANBg" not in text


def test_removes_long_random_strings() -> None:
    secret = "Ab3" * 15
    text, count = redact_secrets(f"value {secret}")
    assert secret not in text
    assert count == 1


def test_keeps_ordinary_text_commit_hashes_and_ids() -> None:
    ordinary = (
        "We agreed to keep gpt-4o-mini. Commit 4e7bb42b5f6c58e0ae55b62e0187d9dc2e3d6a36 "
        "and session 01a11a13-0226-7df2-9886-bb53d5f27cf0. max_tokens=1000. "
        "The token count was high. See /home/chris/projects/domain-check/docs/Feedback/1.md."
    )
    text, count = redact_secrets(ordinary)
    assert text == ordinary
    assert count == 0
