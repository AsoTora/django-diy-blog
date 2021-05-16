import random
import string
from lorem_text import lorem


def random_hash(length: int = 16):
    letters = string.ascii_letters + string.digits + r"!#$*+./:<=>?@[]()^_~"
    return "".join(random.choice(letters) for i in range(length))


def random_string(length: int = 10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(length))


def random_name():
    return f"{lorem.words(3)}"


def random_descr():
    return f"{lorem.paragraph()}"


def random_number(length: int = 100):
    letters = string.digits
    return "".join(random.choice(letters) for i in range(length))
