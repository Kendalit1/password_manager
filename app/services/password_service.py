import secrets
import string
import math
import random
import string
import secrets

def generate_password():
    # Генерируем случайную "сложность"
    level = random.choice(["easy", "medium", "hard"])

    if level == "easy":
        charset = string.ascii_lowercase
        length = random.randint(6, 8)
    elif level == "medium":
        charset = string.ascii_letters + string.digits
        length = random.randint(8, 12)
    else:  # hard
        charset = string.ascii_letters + string.digits + string.punctuation
        length = random.randint(12, 18)

    return ''.join(secrets.choice(charset) for _ in range(length))


def evaluate_entropy(password: str) -> float:
    charset = set()

    for c in password:
        if c in string.ascii_lowercase:
            charset.update(string.ascii_lowercase)
        elif c in string.ascii_uppercase:
            charset.update(string.ascii_uppercase)
        elif c in string.digits:
            charset.update(string.digits)
        elif c in string.punctuation:
            charset.update(string.punctuation)
        else:
            charset.add(c)  # на случай спецсимволов вне ASCII

    charset_size = len(charset)

    if charset_size == 0:
        return 0.0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)


def detect_template_structure(password: str) -> bool:
    common_templates = [
        "123456", "password", "qwerty", "admin", "iloveyou",
        "abc123", "welcome", "1q2w3e", "password1", "qwe123"
    ]
    return password.lower() in common_templates
