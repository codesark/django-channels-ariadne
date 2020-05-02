import random
import string

def random_string_generator(numbers_only=True, length=5):
    if numbers_only is True:
        return ''.join(random.choice(string.digits) for i in range(length))
    else:
        return ''.join(random.choice([string.digits, string.ascii_lowercase]) for i in range(length))