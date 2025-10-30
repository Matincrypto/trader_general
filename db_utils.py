-- برای جلوگیری از خطاهای کلید خارجی، جداول را به ترتیب وابستگی معکوس حذف می‌کنیم
DROP TABLE IF EXISTS trade_signals;
DROP TABLE IF EXISTS api_accounts;
DROP TABLE IF EXISTS bot_users;

-- ۱. جدول کاربران تلگرام
CREATE TABLE bot_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ۲. جدول اکانت‌های صرافی (متصل به کاربران)
CREATE TABLE api_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_user_id INT NOT NULL,              -- این به bot_users.id اشاره دارد
    account_name VARCHAR(100) NOT NULL,
    api_key TEXT NOT NULL,                   -- کلید API رمزنگاری شده
    trade_amount_tmn DECIMAL(15, 2) NOT NULL DEFAULT 500000.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (owner_user_id) REFERENCES bot_users(id) ON DELETE CASCADE,
    -- یک کاربر نمی‌تواند دو اکانت هم‌نام داشته باشد
    UNIQUE KEY uk_owner_account_name (owner_user_id, account_name) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ۳. جدول سیگنال‌های ترید (با ساختار کامل و متصل به اکانت‌ها)
CREATE TABLE trade_signals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_name VARCHAR(20) NOT NULL,
    pair VARCHAR(50),
    entry_price DECIMAL(20, 10),
    exit_price DECIMAL(20, 10),
    strategy_name VARCHAR(100),
    
    -- === ستون کلیدی جدید ===
    account_id INT NOT NULL, 
    
    status VARCHAR(50) NOT NULL DEFAULT 'NEW_SIGNAL',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- ستون‌های مربوط به سفارش خرید
    buy_client_order_id VARCHAR(100),
    buy_quantity_raw DECIMAL(30, 20),
    buy_quantity_formatted DECIMAL(30, 20),
    buy_executed_quantity DECIMAL(30, 20),
    buy_fee DECIMAL(20, 10),
    
    -- ستون‌های مربوط به سفارش فروش
    sell_client_order_id VARCHAR(100),
    sell_executed_quantity DECIMAL(30, 20),
    sell_fee DECIMAL(20, 10),
    
    -- === اتصال کلیدی جدید ===
    FOREIGN KEY (account_id) REFERENCES api_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
