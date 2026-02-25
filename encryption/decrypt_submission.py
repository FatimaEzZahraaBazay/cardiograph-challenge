"""Decrypt submission file using RSA private key (organizer only)."""
import sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file(encrypted_path, private_key_path, output_path):
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend())
    
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    
    key_length = int.from_bytes(encrypted_data[:4], 'big')
    encrypted_aes_key = encrypted_data[4:4+key_length]
    iv = encrypted_data[4+key_length:4+key_length+16]
    ciphertext = encrypted_data[4+key_length+16:]
    
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"Decrypted: {encrypted_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python decrypt_submission.py <encrypted.enc> <private_key.pem> <output.csv>")
        sys.exit(1)
    
    decrypt_file(sys.argv[1], sys.argv[2], sys.argv[3])