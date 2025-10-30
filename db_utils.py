# db_utils.py
import mysql.connector
from mysql.connector import pooling
import logging
import config  # ما از config برای خواندن تنظیمات دیتابیس (که از .env آمده) استفاده می‌کنیم

# تنظیمات لاگ‌گیری
logging.basicConfig(level=config.BOT["LOG_LEVEL"], format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# --- ۱. ایجاد استخر کانکشن (Connection Pool) ---
# این استخر به صورت گلوبال در این ماژول ساخته می‌شود و فقط یک بار اجرا می‌شود
try:
    if not config.DATABASE.get("user") or not config.DATABASE.get("password"):
        logging.critical("اطلاعات کاربر یا پسورد دیتابیس در .env یافت نشد.")
        db_pool = None
    else:
        db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="tradebot_pool",
            pool_size=5,  # تعداد کانکشن‌هایی که باز نگه داشته می‌شوند
            pool_reset_session=True,
            **config.DATABASE
        )
        logging.info("استخر کانکشن دیتابیس (Connection Pool) با موفقیت ایجاد شد.")
except mysql.connector.Error as e:
    logging.critical(f"خطای بحرانی در ایجاد Connection Pool: {e}")
    db_pool = None

def get_db_connection():
    """یک کانکشن از استخر دریافت می‌کند."""
    if not db_pool:
        logging.error("Connection Pool در دسترس نیست. آیا دیتابیس روشن است؟")
        return None
    try:
        # get_connection() به صورت خودکار یک کانکشن آزاد از استخر برمی‌دارد
        return db_pool.get_connection()
    except mysql.connector.Error as e:
        logging.error(f"خطا در دریافت کانکشن از استخر: {e}")
        return None

def query_db(query, params=None, fetch=None):
    """
    تابع عمومی اجرای کوئری، اکنون با استفاده از Connection Pool.
    
    :param query: رشته کوئری SQL
    :param params: پارامترهای جایگزین در کوئری (برای جلوگیری از SQL Injection)
    :param fetch: 'one' (برای یک ردیف)، 'all' (برای همه ردیف‌ها)، None (برای INSERT/UPDATE/DELETE)
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = None
    try:
        # dictionary=True باعث می‌شود نتایج به صورت دیکشنری (dict) برگردند
        cursor = connection.cursor(dictionary=(fetch is not None))
        
        # params or () یک ترفند پایتون برای اطمینان از ارسال تاپل خالی است اگر params=None باشد
        cursor.execute(query, params or ())
        
        if fetch == 'one':
            result = cursor.fetchone()
        elif fetch == 'all':
            result = cursor.fetchall()
        else:
            # این برای INSERT, UPDATE, DELETE است
            connection.commit() 
            result = True
            
        return result
    
    except mysql.connector.Error as e:
        logging.error(f"خطای کوئری پایگاه داده: {e} | کوئری: {query} | پارامترها: {params}")
        # در صورت خطا در تراکنش، تغییرات را بازگردانی (rollback) می‌کنیم
        if fetch is None:
             try:
                 connection.rollback()
                 logging.warning("تراکنش دیتابیس به دلیل خطا Rollback شد.")
             except Exception as rb_e:
                 logging.error(f"خطا در زمان Rollback کردن: {rb_e}")
        return None
    
    finally:
        # --- ۲. بازگرداندن کانکشن به استخر ---
        # این بخش بسیار حیاتی است
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            # در pooling، connection.close() کانکشن را نمی‌بندد
            # بلکه آن را به استخر "پس" می‌دهد تا برای کوئری بعدی آماده باشد.
            connection.close()
