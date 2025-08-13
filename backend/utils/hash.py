import hashlib

# Utility function for generating a SHA-256 hash of a survey prompt.
# Used for cache keys and deduplication.
def hash_prompt(text: str) -> str:
    """
    Stable, normalized hash of the user description.
    - trims whitespace
    - collapses inner whitespace
    - lowercases
    - prefixes a version to allow future cache invalidation
    """
    normalized = "v1|" + " ".join(text.strip().split()).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()