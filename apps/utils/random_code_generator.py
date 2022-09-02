import secrets
import string


def generate_code(length: int = 5):
    alphabet = string.ascii_letters + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(length))
    return code
