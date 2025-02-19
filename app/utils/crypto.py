import uuid
import hashlib

def generate_unique_id(uuid1: str, uuid2: str, algo: str = "md5") -> str:
    """
    Generate a unique ID based on two UUIDs using a specified hashing algorithm.

    Args:
        uuid1 (str): First UUID.
        uuid2 (str): Second UUID.
        algo (str): Hashing algorithm (default: 'sha256'). Options: 'md5', 'sha1', 'sha256', 'sha512'.

    Returns:
        str: A unique hash-based ID.
    """
    # Combine the two UUIDs
    combined_str = f"{uuid1}{uuid2}"

    # Choose hashing algorithm
    if algo == "md5":
        hash_obj = hashlib.md5(combined_str.encode())
    elif algo == "sha1":
        hash_obj = hashlib.sha1(combined_str.encode())
    elif algo == "sha256":
        hash_obj = hashlib.sha256(combined_str.encode())
    elif algo == "sha512":
        hash_obj = hashlib.sha512(combined_str.encode())
    else:
        raise ValueError("Unsupported hashing algorithm")

    return hash_obj.hexdigest()