"""Encrypt submission file using RSA public key."""
import sys
import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_file(input_path, public_key_path, output_path):
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
    
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    
    aes_key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    
    encrypted_data = (len(encrypted_aes_key).to_bytes(4, 'big') +
                      encrypted_aes_key + iv + ciphertext)
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)
    
    print(f"Encrypted: {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python encryption/encrypt_submission.py predictions.csv")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"File not found: {input_file}")
        sys.exit(1)
    
    public_key = Path("encryption/public_key.pem")
    if not public_key.exists():
        print(f"Public key not found: {public_key}")
        sys.exit(1)
    
    output_file = input_file.with_suffix('.csv.enc')
    encrypt_file(input_file, public_key, output_file)
    print(f"\nSubmit {output_file.name} in your PR (NOT the original CSV)")