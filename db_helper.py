"""
商業資料庫查詢工具 (Shared DB Helper)
供 Agent 自動生成的技能直接 import 使用，不依賴 Agent 層級的 SQLTools。

使用方式 (在技能中)：
    from db_helper import query, query_df

    # 取得 list[dict]
    rows = query("SELECT * FROM products WHERE category = '手機'")

    # 取得 pandas DataFrame
    df = query_df("SELECT * FROM products")
"""

import sqlite3
from pathlib import Path
from typing import Optional


# 商業資料庫路徑
BIZ_DB_PATH = Path(__file__).parent / "data" / "business.db"


def query(sql: str, params: tuple = ()) -> list[dict]:
    """
    執行 SQL 查詢，回傳 list[dict]。

    Args:
        sql: SQL SELECT 語句
        params: 查詢參數（防注入）

    Returns:
        查詢結果，每列為一個 dict
    """
    conn = sqlite3.connect(str(BIZ_DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def query_df(sql: str, params: tuple = ()):
    """
    執行 SQL 查詢，回傳 pandas DataFrame。

    Args:
        sql: SQL SELECT 語句
        params: 查詢參數

    Returns:
        pandas.DataFrame
    """
    import pandas as pd
    conn = sqlite3.connect(str(BIZ_DB_PATH))
    try:
        return pd.read_sql_query(sql, conn, params=params)
    finally:
        conn.close()
