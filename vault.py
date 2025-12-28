import json
from crypto import decrypt, encrypt

data = []

def add_entry(url, username, password):
    data.append({
        "url": url,
        "username": username,
        "password": password
    })

def delete(index):
    if 0 <= index < len(data):
        removed = data.pop(index)
        print(f"Deleted entry: {removed['url']} / {removed['username']}")
    else:
        print("Invalid index")

def show_vault():
    if not data:
        print("Vault is empty.")
        return

    for i, entry in enumerate(data, start=1):  # number each entry starting from 1
        print(f"{i}. URL: {entry['url']}, Username: {entry['username']}, Password: {entry['password']}")

def save_vault(password: str, filename: str):
    json_vault = json.dumps(data)
    encrypted_vault = encrypt(json_vault, password)
    with open(filename, "wb") as f:
        f.write(encrypted_vault)

def load_vault(password: str, filename: str):
    global data
    f = open(filename, "rb")
    encrypted_vault = f.read()
    f.close()
    json_vault = decrypt(encrypted_vault, password)
    data = json.loads(json_vault)