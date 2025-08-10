import hashlib

# Utility function for generating a SHA-256 hash of a survey prompt.
# Used for cache keys and deduplication.
def hash_prompt(text: str) -> str:
    return