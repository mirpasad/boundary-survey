import hashlib

def hash_prompt(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()