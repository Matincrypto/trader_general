# config.py
import logging
import os
from dotenv import load_dotenv

# --- مهم: بارگذاری متغیرهای محیطی از .env ---
# این دستور باید قبل از هرچیز دیگری اجرا شود
load_dotenv()

# ==============================================================================
# 1. STRATEGY API CONFIGURATION
# ==============================================================================
STRATEGY_API = {
    "SOURCES": {
        "Internal_Arbitrage": "http://103.75.198.172:5005/Internal/arbitrage"
    }
}

# ==============================================================================
# 2. WALLEX EXCHANGE API CONFIGURATION
# ==============================================================================
WALLEX_API = {
    # API_KEY از اینجا حذف شد و به دیتابیس منتقل گردید
    "BASE_URL": "https://api.wallex.ir",
    "ENDPOINTS": {
        "ALL_MARKETS": "/hector/web/v1/markets",
        "ACCOUNT_BALANCES": "/v1/account/balances",
        "ORDERS": "/v1/account/orders",          # POST (New Order), DELETE (Cancel Order)
        "GET_ORDER": "/v1/account/orders/"  # GET (Get Order Status)
    }
}

# ==============================================================================
# 3. TRADING PARAMETERS
# ==============================================================================
TRADING = {
    # TRADE_AMOUNT_TMN از اینجا حذف شد و به دیتابیس منتقل گردید
    "QUOTE_ASSET": "TMN",           # بازار پایه ما (تومان)
}

# ==============================================================================
# 4. BOT SETTINGS
# ==============================================================================
BOT = {
    "SIGNAL_CHECK_INTERVAL_SECONDS": 60,
    "ORDER_MANAGEMENT_INTERVAL_SECONDS": 30,
    "CLEANUP_INTERVAL_SECONDS": 60,
    "LOG_LEVEL": logging.INFO,
    "STALE_ORDER_TIMEOUT_MINUTES": 5
}

# ==============================================================================
# 5. DATABASE CONFIGURATION (Loaded from .env)
# ==============================================================================
DATABASE = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# --- بررسی‌های حیاتی ---
if not DATABASE["password"]:
    logging.critical("FATAL ERROR: DB_PASSWORD در فایل .env یافت نشد.")
    # raise ValueError("DB_PASSWORD یافت نشد. فایل .env خود را بررسی کنید.")
    
if not os.getenv("ENCRYPTION_KEY"):
    logging.critical("FATAL ERROR: ENCRYPTION_KEY در فایل .env یافت نشد.")

if not os.getenv("TELEGRAM_BOT_TOKEN"):
    logging.critical("FATAL ERROR: TELEGRAM_BOT_TOKEN در فایل .env یافت نشد.")# config.py
import logging
import os
from dotenv import load_dotenv

# --- مهم: بارگذاری متغیرهای محیطی از .env ---
# این دستور باید قبل از هرچیز دیگری اجرا شود
load_dotenv()

# ==============================================================================
# 1. STRATEGY API CONFIGURATION
# ==============================================================================
STRATEGY_API = {
    "SOURCES": {
        "Internal_Arbitrage": "http://103.75.198.172:5005/Internal/arbitrage"
    }
}

# ==============================================================================
# 2. WALLEX EXCHANGE API CONFIGURATION
# ==============================================================================
WALLEX_API = {
    # API_KEY از اینجا حذف شد و به دیتابیس منتقل گردید
    "BASE_URL": "https://api.wallex.ir",
    "ENDPOINTS": {
        "ALL_MARKETS": "/hector/web/v1/markets",
        "ACCOUNT_BALANCES": "/v1/account/balances",
        "ORDERS": "/v1/account/orders",          # POST (New Order), DELETE (Cancel Order)
        "GET_ORDER": "/v1/account/orders/"  # GET (Get Order Status)
    }
}

# ==============================================================================
# 3. TRADING PARAMETERS
# ==============================================================================
TRADING = {
    # TRADE_AMOUNT_TMN از اینجا حذف شد و به دیتابیس منتقل گردید
    "QUOTE_ASSET": "TMN",           # بازار پایه ما (تومان)
}

# ==============================================================================
# 4. BOT SETTINGS
# ==============================================================================
BOT = {
    "SIGNAL_CHECK_INTERVAL_SECONDS": 60,
    "ORDER_MANAGEMENT_INTERVAL_SECONDS": 30,
    "CLEANUP_INTERVAL_SECONDS": 60,
    "LOG_LEVEL": logging.INFO,
    "STALE_ORDER_TIMEOUT_MINUTES": 5
}

# ==============================================================================
# 5. DATABASE CONFIGURATION (Loaded from .env)
# ==============================================================================
DATABASE = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# --- بررسی‌های حیاتی ---
if not DATABASE["password"]:
    logging.critical("FATAL ERROR: DB_PASSWORD در فایل .env یافت نشد.")
    # raise ValueError("DB_PASSWORD یافت نشد. فایل .env خود را بررسی کنید.")
    
if not os.getenv("ENCRYPTION_KEY"):
    logging.critical("FATAL ERROR: ENCRYPTION_KEY در فایل .env یافت نشد.")

if not os.getenv("TELEGRAM_BOT_TOKEN"):
    logging.critical("FATAL ERROR: TELEGRAM_BOT_TOKEN در فایل .env یافت نشد.")
