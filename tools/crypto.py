import hashlib

def text_to_sha256(text: str) -> str:
    """Return the SHA256 hexadecimal digest of the input text.

    Args:
        text: Input string to hash.

    Returns:
        Hexadecimal SHA256 hash string.
    """
    if not isinstance(text, str):
        # Coerce non-string inputs to string
        text = str(text)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()