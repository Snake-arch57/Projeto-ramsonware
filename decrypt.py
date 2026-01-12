import os
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt_file(enc_file_path: str, password: str):
    with open(enc_file_path, 'rb') as f:
        data = f.read()
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = padded.rstrip(b'\0')  # remove padding zero
    original_path = enc_file_path.replace('.aes', '')
    with open(original_path, 'wb') as f:
        f.write(plaintext)
    os.remove(enc_file_path)
    print(f"Decrypted: {original_path}")

def decrypt_directory(directory: str, password: str):
    for file in os.listdir(directory):
        if file.endswith('.aes'):
            file_path = os.path.join(directory, file)
            decrypt_file(file_path, password)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python decrypt.py sua_senha")
        sys.exit(1)
    
    password = sys.argv[1]
    directory = os.path.dirname(os.path.abspath(__file__))
    decrypt_directory(directory, password)