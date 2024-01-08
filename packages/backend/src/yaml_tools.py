from cryptography.fernet import Fernet
import yaml

file_path = '../configuration/access_token.yml'
def generate_key():
    return Fernet.generate_key()

def encrypt(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def encrypt_yaml(data, key):
    encrypted_data = encrypt(yaml.dump(data), key)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_yaml(key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = decrypt(encrypted_data, key)
    return yaml.safe_load(decrypted_data)