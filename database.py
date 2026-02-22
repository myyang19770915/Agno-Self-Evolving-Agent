"""
SQLite 資料庫管理模組
負責 Agent 技能（Skills）的持久化存儲與 CRUD 操作。
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional


# 資料庫檔案路徑
DB_DIR = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "agent.db"


def _get_connection() -> sqlite3.Connection:
    """取得資料庫連線，啟用 WAL 模式以支援並發讀取。"""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """初始化資料庫，建立 agent_skills 表（若尚未存在）。"""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT DEFAULT '',
                code_content TEXT NOT NULL,
                file_path TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_skill(
    name: str,
    code_content: str,
    description: str = "",
    file_path: str = "",
) -> str:
    """
    儲存或更新一個技能（UPSERT 邏輯）。

    Args:
        name: 技能名稱（唯一鍵）
        code_content: 技能的 Python 程式碼
        description: 技能描述
        file_path: 對應的檔案路徑（若有寫入 tools/ 目錄）

    Returns:
        操作結果訊息
    """
    conn = _get_connection()
    try:
        now = datetime.now().isoformat()
        conn.execute("""
            INSERT INTO agent_skills (name, description, code_content, file_path, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                description = excluded.description,
                code_content = excluded.code_content,
                file_path = excluded.file_path,
                updated_at = excluded.updated_at
        """, (name, description, code_content, file_path, now, now))
        conn.commit()
        return f"✅ 技能 '{name}' 已成功儲存到資料庫。"
    except Exception as e:
        return f"❌ 儲存技能失敗: {e}"
    finally:
        conn.close()


def get_skill(name: str) -> Optional[dict]:
    """
    依名稱取得單一技能。

    Args:
        name: 技能名稱

    Returns:
        技能資料字典，若不存在則返回 None
    """
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM agent_skills WHERE name = ?", (name,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_skills() -> list[dict]:
    """
    列出所有已儲存的技能。

    Returns:
        技能資料字典列表
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT name, description, file_path, updated_at FROM agent_skills ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def delete_skill(name: str) -> str:
    """
    刪除指定名稱的技能。

    Args:
        name: 技能名稱

    Returns:
        操作結果訊息
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM agent_skills WHERE name = ?", (name,)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return f"✅ 技能 '{name}' 已刪除。"
        return f"⚠️ 技能 '{name}' 不存在。"
    finally:
        conn.close()


def get_skill_code(name: str) -> Optional[str]:
    """
    取得技能的原始程式碼（用於動態執行）。

    Args:
        name: 技能名稱

    Returns:
        程式碼字串，若不存在則返回 None
    """
    skill = get_skill(name)
    return skill["code_content"] if skill else None


# 模組載入時自動初始化資料庫
init_db()
