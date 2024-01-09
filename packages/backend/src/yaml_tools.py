from cryptography.fernet import Fernet
import yaml

file_path = 'configuration/access_token.yml'
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

def load_yaml():
    with open('configuration/access_token.yml', 'r') as file:
        data = yaml.safe_load(file)
    return data