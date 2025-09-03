import os

REQUIRED_KEYS = [
    "SECRET_KEY",
    "DEBUG",
    "ALLOWED_HOSTS",
    "OPEN_METEO_BASE_URL"
]

def check_env_keys():
    missing = [key for key in REQUIRED_KEYS if os.getenv(key) is None]
    if missing:
        print(f"Missing keys in .env: {missing}")
    else:
        print("All required .env keys are present.")

if __name__ == "__main__":
    check_env_keys()