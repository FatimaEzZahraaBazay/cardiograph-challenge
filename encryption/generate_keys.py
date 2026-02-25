"""
Generate RSA key pair for encryption (run once by organizer).
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path


def generate_rsa_keys():
    """Generate RSA-2048 key pair."""
    print("Generating RSA-2048 key pair...")
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    private_path = Path("encryption/private_key.pem")
    with open(private_path, 'wb') as f:
        f.write(private_pem)
    
    print(f"Private key saved: {private_path}")
    print("WARNING: NEVER commit this file!")
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    public_path = Path("encryption/public_key.pem")
    with open(public_path, 'wb') as f:
        f.write(public_pem)
    
    print(f"Public key saved: {public_path}")
    print("Commit this file to repo for participants")
    
    print("\nNext steps:")
    print("1. Copy private_key.pem content to GitHub Secrets (name: PRIVATE_KEY)")
    print("2. Commit public_key.pem to repository")
    print("3. Delete private_key.pem from local disk")


if __name__ == "__main__":
    generate_rsa_keys()