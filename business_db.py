"""
商業資料庫模組 (Business Database)
建立虛構的商業資料表並填充模擬資料，供 Agent 以自然語言進行查詢與分析。
"""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


# 商業資料庫路徑（與技能 DB 分開）
BIZ_DB_DIR = Path(__file__).parent / "data"
BIZ_DB_PATH = BIZ_DB_DIR / "business.db"


def _get_connection() -> sqlite3.Connection:
    """取得商業資料庫連線。"""
    BIZ_DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(BIZ_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_business_db() -> None:
    """初始化商業資料庫 Schema。"""
    conn = _get_connection()
    try:
        # 產品表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                unit_price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0
            )
        """)

        # 客戶表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                city TEXT NOT NULL,
                membership_level TEXT DEFAULT 'Bronze',
                join_date TEXT NOT NULL
            )
        """)

        # 訂單表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        # 訂單明細表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # 員工表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL,
                hire_date TEXT NOT NULL
            )
        """)

        conn.commit()
    finally:
        conn.close()


def seed_data() -> str:
    """填充模擬資料（若已存在則跳過）。"""
    conn = _get_connection()
    try:
        # 檢查是否已有資料
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count > 0:
            return "📦 商業資料庫已存在資料，跳過填充。"

        random.seed(42)  # 確保資料可重現

        # === 產品 (20 項) ===
        products = [
            ("MacBook Pro 14吋", "電腦", 59900),
            ("iPhone 16 Pro", "手機", 36900),
            ("iPad Air", "平板", 22900),
            ("AirPods Pro", "配件", 7490),
            ("Apple Watch Ultra", "穿戴", 27900),
            ("Dell XPS 15", "電腦", 52000),
            ("Samsung Galaxy S25", "手機", 31900),
            ("Sony WH-1000XM5", "配件", 10900),
            ("Nintendo Switch 2", "遊戲", 12800),
            ("PS5 Pro", "遊戲", 17980),
            ("LG OLED 65吋電視", "家電", 62900),
            ("Dyson V15 吸塵器", "家電", 24900),
            ("Bose SoundLink Max", "配件", 12800),
            ("ASUS ROG 電競筆電", "電腦", 45900),
            ("Google Pixel 9", "手機", 26900),
            ("Kindle Paperwhite", "閱讀", 4490),
            ("Logitech MX Master 3S", "配件", 3490),
            ("Samsung 49吋曲面螢幕", "電腦", 39900),
            ("GoPro Hero 13", "相機", 13800),
            ("DJI Mini 4 Pro", "相機", 25900),
        ]
        for name, category, price in products:
            stock = random.randint(10, 500)
            conn.execute(
                "INSERT INTO products (name, category, unit_price, stock_quantity) VALUES (?, ?, ?, ?)",
                (name, category, price, stock),
            )

        # === 客戶 (50 位) ===
        cities = ["台北", "新北", "桃園", "台中", "台南", "高雄", "新竹", "嘉義"]
        levels = ["Bronze", "Silver", "Gold", "Platinum"]
        first_names = ["陳", "林", "黃", "張", "李", "王", "吳", "劉", "蔡", "楊"]
        last_names = ["志明", "美玲", "家豪", "淑芬", "建宏", "雅婷", "宗翰", "怡君", "俊傑", "佳慧"]

        for i in range(50):
            name = random.choice(first_names) + random.choice(last_names)
            city = random.choice(cities)
            level = random.choices(levels, weights=[40, 30, 20, 10])[0]
            join_date = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
            email = f"customer{i + 1}@example.com"
            conn.execute(
                "INSERT INTO customers (name, email, city, membership_level, join_date) VALUES (?, ?, ?, ?, ?)",
                (name, email, city, level, join_date),
            )

        # === 訂單 (300 筆，跨 2024-2025) ===
        statuses = ["completed", "completed", "completed", "completed", "cancelled", "refunded"]

        for _ in range(300):
            customer_id = random.randint(1, 50)
            order_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 729))).strftime("%Y-%m-%d")
            status = random.choice(statuses)

            # 每張訂單 1-4 個品項
            num_items = random.randint(1, 4)
            chosen_products = random.sample(range(1, 21), num_items)
            total = 0.0

            conn.execute(
                "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, 0, ?)",
                (customer_id, order_date, status),
            )
            order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            for pid in chosen_products:
                qty = random.randint(1, 3)
                price_row = conn.execute("SELECT unit_price FROM products WHERE id = ?", (pid,)).fetchone()
                unit_price = price_row[0]
                # 隨機折扣 0~15%
                discount = random.uniform(0.85, 1.0)
                actual_price = round(unit_price * discount, 0)
                subtotal = actual_price * qty
                total += subtotal

                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)",
                    (order_id, pid, qty, actual_price, subtotal),
                )

            conn.execute("UPDATE orders SET total_amount = ? WHERE id = ?", (total, order_id))

        # === 員工 (15 位) ===
        departments = [
            ("業務部", ["業務經理", "業務專員", "業務專員"]),
            ("工程部", ["技術主管", "資深工程師", "工程師", "工程師"]),
            ("行銷部", ["行銷經理", "行銷專員"]),
            ("人資部", ["人資主管", "人資專員"]),
            ("財務部", ["財務經理", "會計師", "會計專員"]),
        ]

        emp_names = [
            "趙一明", "錢二華", "孫三強", "李四海", "周五洋",
            "吳六合", "鄭七星", "王八方", "馮九天", "陳十全",
            "褚志高", "衛麗華", "蔣德明", "沈慧君", "韓正義",
        ]

        name_idx = 0
        for dept, positions in departments:
            for pos in positions:
                if name_idx >= len(emp_names):
                    break
                salary = random.randint(35000, 120000)
                hire_date = (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))).strftime("%Y-%m-%d")
                conn.execute(
                    "INSERT INTO employees (name, department, position, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
                    (emp_names[name_idx], dept, pos, salary, hire_date),
                )
                name_idx += 1

        conn.commit()
        return "✅ 商業資料庫已建立並填充模擬資料：20 項產品、50 位客戶、300 筆訂單、15 位員工。"

    finally:
        conn.close()


# 模組載入時自動初始化
init_business_db()
_seed_result = seed_data()
print(_seed_result)

