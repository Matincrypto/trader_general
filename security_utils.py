# security_utils.py
import os
import bcrypt
from cryptography.fernet import Fernet
import base64
import logging
import config  # ما کانفیگ را ایمپورت می‌کنیم تا مطمئن شویم لاگ‌گیری تنظیم شده است

# تنظیمات لاگ‌گیری
logging.basicConfig(level=config.BOT["LOG_LEVEL"], format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# --- بارگذاری کلید رمزنگاری از .env ---
try:
    SECRET_KEY = os.getenv("ENCRYPTION_KEY")
    if not SECRET_KEY:
        raise ValueError("ENCRYPTION_KEY در فایل .env یافت نشد.")
    
    # Fernet به کلید 32 بایتی و base64-encoded نیاز دارد.
    # ما کلید خام شما (که توصیه کردیم 32 بایت باشد) را به base64 تبدیل می‌کنیم.
    
    key_bytes = SECRET_KEY.encode('utf-8')
    
    # اطمینان از 32 بایت بودن کلید
    if len(key_bytes) > 32:
        key_bytes = key_bytes[:32] # بریدن کلید اگر طولانی‌تر است
    elif len(key_bytes) < 32:
        key_bytes = key_bytes.ljust(32, b'\0') # پد کردن کلید اگر کوتاه‌تر است

    FERNET_KEY = base64.urlsafe_b64encode(key_bytes)
    cipher_suite = Fernet(FERNET_KEY)
    logging.info("ماژول امنیتی (Security) با موفقیت بارگذاری شد.")

except Exception as e:
    logging.critical(f"خطای بحرانی در بارگذاری کلید رمزنگاری: {e}")
    cipher_suite = None

# --- توابع مربوط به پسورد (Hashing) ---

def hash_password(plain_password: str) -> str:
    """پسورد متن ساده را به هش bcrypt تبدیل می‌کند."""
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    """بررسی می‌کند آیا پسورد ساده با هش ذخیره شده مطابقت دارد یا خیر."""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logging.error(f"خطا در بررسی پسورد: {e}")
        return False

# --- توابع مربوط به API Keys (Encryption/Decryption) ---

def encrypt_data(data_str: str) -> str | None:
    """یک رشته (مثل API Key) را رمزنگاری می‌کند."""
    if not cipher_suite:
        logging.error("امکان رمزنگاری وجود ندارد. کلید بارگذاری نشده است.")
        return None
    try:
        encrypted_bytes = cipher_suite.encrypt(data_str.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"خطا در زمان رمزنگاری: {e}")
        return None

def decrypt_data(encrypted_str: str) -> str | None:
    """یک رشته رمزنگاری شده را به حالت ساده بازمی‌گرداند."""
    if not cipher_suite:
        logging.error("امکان رمزگشایی وجود ندارد. کلید بارگذاری نشده است.")
        return None
    try:
        # برخی رشته‌های ذخیره شده در دیتابیس ممکن است فضای خالی اضافه داشته باشند
        encrypted_bytes_clean = encrypted_str.strip().encode('utf-8')
        decrypted_bytes = cipher_suite.decrypt(encrypted_bytes_clean)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        # این خطا معمولاً اگر کلید عوض شود یا داده خراب باشد رخ می‌دهد
        logging.error(f"خطا در زمان رمزگشایی (داده نامعتبر یا کلید اشتباه؟): {e}")
        return None
