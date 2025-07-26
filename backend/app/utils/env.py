import os
from dotenv import load_dotenv
from secrets import token_hex

load_dotenv()

# Auto-generate JWT_SECRET_KEY if not set
if not os.getenv("JWT_SECRET_KEY"):
    with open(".env", "a") as f:
        secret_key = token_hex(32)
        f.write(f"JWT_SECRET_KEY={secret_key}\n")
    os.environ["JWT_SECRET_KEY"] = secret_key
