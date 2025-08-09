from hashlib import sha256

def hash_prompt(s: str) -> str:
    return sha256(s.strip().encode("utf-8")).hexdigest()
