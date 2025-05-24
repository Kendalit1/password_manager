import os
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), '../static/data')
BREACHED_FILE = os.path.join(DATA_DIR, 'breached_passwords.txt')
BREACHED_URL = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt'

def load_breached_passwords():
    if not os.path.exists(BREACHED_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        print("[i] Загрузка базы скомпрометированных паролей...")
        response = requests.get(BREACHED_URL)
        with open(BREACHED_FILE, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("[+] Загружено:", BREACHED_FILE)

    with open(BREACHED_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

breached_passwords = load_breached_passwords()

def is_password_breached(password: str) -> bool:
    return password.lower() in breached_passwords
