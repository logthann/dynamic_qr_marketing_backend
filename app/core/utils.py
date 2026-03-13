import string
import random

def generate_short_code(length: int = 6) -> str:
    """Tạo chuỗi ngẫu nhiên gồm chữ cái và số cho short_code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))