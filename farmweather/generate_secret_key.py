import secrets

def generate_key():
    key = secrets.token_urlsafe(50)
    print(f"Generated SECRET_KEY:\n{key}")

if __name__ == "__main__":
    generate_key()