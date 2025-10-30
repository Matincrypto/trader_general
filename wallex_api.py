# wallex_api.py
import requests
import json
import logging
import math
import config
from decimal import Decimal

# دیکشنری برای ذخیره قوانین دقت اعشار
market_precisions = {}

# --------------------------------------------------------------------------
# توابع عمومی (بدون نیاز به API Key - بدون تغییر)
# --------------------------------------------------------------------------

def load_market_precisions():
    """
    قوانین دقت اعشار (amount_precision) را از والکس بارگذاری کرده 
    و در متغیر گلوبال market_precisions ذخیره می‌کند.
    """
    global market_precisions
    if market_precisions: # اگر قبلا بارگذاری شده، دوباره انجام نده
        return True
        
    logging.info("در حال بارگذاری قوانین دقت اعشار بازارها از والکس...")
    url = config.WALLEX_API["BASE_URL"] + config.WALLEX_API["ENDPOINTS"]["ALL_MARKETS"]
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            markets = response.json().get("result", {}).get("markets", [])
            for market in markets:
                symbol = market.get("symbol")
                precision = market.get("amount_precision")
                if symbol and precision is not None:
                    market_precisions[symbol] = int(precision)
            logging.info(f"قوانین دقت اعشار برای {len(market_precisions)} بازار با موفقیت بارگذاری شد.")
            return True
        else:
            logging.error(f"خطا در بارگذاری قوانین دقت اعشار بازارها. وضعیت: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در ارتباط برای دریافت قوانین بازار: {e}")
        return False

def format_quantity(quantity, precision):
    """
    مقدار (Quantity) را بر اساس دقت اعشار مجاز بازار، به پایین گرد می‌کند (Floor).
    """
    factor = Decimal(10) ** precision
    return math.floor(Decimal(quantity) * factor) / factor

# --------------------------------------------------------------------------
# توابع خصوصی (نیاز به API Key - تغییر یافته)
# --------------------------------------------------------------------------

def place_wallex_order(symbol, price, quantity, side, api_key_string: str):
    """
    یک سفارش جدید (خرید یا فروش) در صرافی والکس ثبت می‌کند.
    *** تغییر: api_key_string را به عنوان آرگومان دریافت می‌کند ***
    """
    if not api_key_string:
        logging.error("خطای API: تابع place_wallex_order بدون api_key_string فراخوانی شد.")
        return None

    url = config.WALLEX_API["BASE_URL"] + config.WALLEX_API["ENDPOINTS"]["ORDERS"]
    
    # === تغییر کلیدی در اینجا ===
    headers = {"Content-Type": "application/json", "x-api-key": api_key_string}
    
    payload = {
        "symbol": symbol, 
        "price": str(price), 
        "quantity": str(quantity), 
        "side": side.lower(), # 'buy' or 'sell'
        "type": "limit"
    }
    
    logging.info(f"در حال ثبت سفارش: {side.upper()} {quantity} {symbol} @ {price}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        response_data = response.json()
        
        if response.status_code == 201 and response_data.get("success"):
            order_id = response_data.get("result", {}).get("clientOrderId")
            logging.info(f"سفارش با موفقیت ثبت شد! شناسه سفارش: {order_id}")
            return response_data
        else:
            logging.error(f"خطا در ثبت سفارش. وضعیت: {response.status_code}, پاسخ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در زمان ثبت سفارش در والکس: {e}")
        return None

def get_wallex_order_status(client_order_id: str, api_key_string: str):
    """
    جزئیات کامل و وضعیت یک سفارش مشخص را از والکس دریافت می‌کند.
    *** تغییر: api_key_string را به عنوان آرگومان دریافت می‌کند ***
    """
    if not api_key_string:
        logging.error("خطای API: تابع get_wallex_order_status بدون api_key_string فراخوانی شد.")
        return None

    url = config.WALLEX_API["BASE_URL"] + config.WALLEX_API["ENDPOINTS"]["GET_ORDER"] + client_order_id
    
    # === تغییر کلیدی در اینجا ===
    headers = {"x-api-key": api_key_string}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("success"):
            return response_data.get("result") # بازگرداندن آبجکت کامل سفارش
        else:
            logging.warning(f"عدم موفقیت در دریافت وضعیت سفارش {client_order_id}. پاسخ: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در ارتباط برای دریافت وضعیت سفارش {client_order_id}: {e}")
        return None

def cancel_wallex_order(client_order_id: str, api_key_string: str):
    """
    یک سفارش باز را در والکس با استفاده از client_order_id لغو می‌کند.
    *** تغییر: api_key_string را به عنوان آرگومان دریافت می‌کند ***
    """
    if not api_key_string:
        logging.error("خطای API: تابع cancel_wallex_order بدون api_key_string فراخوانی شد.")
        return None

    url = config.WALLEX_API["BASE_URL"] + config.WALLEX_API["ENDPOINTS"]["ORDERS"]
    
    # === تغییر کلیدی در اینجا ===
    headers = {"Content-Type": "application/json", "x-api-key": api_key_string}
    
    payload = {"clientOrderId": client_order_id}
    
    logging.info(f"در حال تلاش برای لغو سفارش {client_order_id} در والکس...")
    try:
        response = requests.delete(url, headers=headers, data=json.dumps(payload), timeout=15)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("success"):
            logging.info(f"سفارش {client_order_id} با موفقیت در والکس لغو شد.")
            return True
        else:
            logging.error(f"خطا در لغو سفارش {client_order_id}. وضعیت: {response.status_code}, پاسخ: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در زمان لغو سفارش در والکس: {e}")
        return False
