"""
技能管理器 (CapabilityManager)
負責技能的檔案管理、動態載入、JSON 索引維護，以及與資料庫的同步。
"""

import os
import json
import importlib
import importlib.util
from pathlib import Path
from typing import Any

import database as db


# 預設路徑
TOOLS_DIR = Path(__file__).parent / "tools"
CAPABILITIES_FILE = TOOLS_DIR / "capabilities.json"


class CapabilityManager:
    """管理 Agent 的技能生命週期：建立、載入、索引、注入。"""

    def __init__(self, tools_dir: Path = TOOLS_DIR):
        self.tools_dir = tools_dir
        self.capabilities: dict[str, dict] = {}
        self._ensure_structure()
        self._load_capabilities()

    def _ensure_structure(self) -> None:
        """確保 tools/ 目錄和基礎檔案存在。"""
        self.tools_dir.mkdir(parents=True, exist_ok=True)

        init_file = self.tools_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")

        if not CAPABILITIES_FILE.exists():
            CAPABILITIES_FILE.write_text("{}", encoding="utf-8")

    def _load_capabilities(self) -> None:
        """從 capabilities.json 載入技能索引。"""
        try:
            text = CAPABILITIES_FILE.read_text(encoding="utf-8")
            self.capabilities = json.loads(text) if text.strip() else {}
        except (json.JSONDecodeError, FileNotFoundError):
            self.capabilities = {}

    def _save_capabilities(self) -> None:
        """將技能索引寫回 capabilities.json。"""
        CAPABILITIES_FILE.write_text(
            json.dumps(self.capabilities, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def save_skill(
        self,
        name: str,
        description: str,
        code: str,
        filename: str = "",
    ) -> str:
        """
        儲存一個新技能：寫入檔案、更新 JSON 索引、同步到資料庫。

        Args:
            name: 技能名稱（也是函數名稱）
            description: 技能功能描述
            code: Python 程式碼內容
            filename: 檔案名稱（不含 .py），預設使用 name

        Returns:
            操作結果訊息
        """
        if not filename:
            filename = name

        # 寫入 .py 檔案
        file_path = self.tools_dir / f"{filename}.py"
        file_path.write_text(code, encoding="utf-8")

        # 更新 capabilities.json
        self.capabilities[name] = {
            "description": description,
            "file": f"{filename}.py",
            "usage": f"from tools.{filename} import {name}",
        }
        self._save_capabilities()

        # 同步到資料庫
        db.save_skill(
            name=name,
            code_content=code,
            description=description,
            file_path=str(file_path),
        )

        return f"✅ 技能 '{name}' 已儲存到 tools/{filename}.py 並更新索引。"

    def load_module(self, module_name: str) -> Any:
        """
        動態載入 tools/ 目錄下的模組（支援 Hot Reload）。

        Args:
            module_name: 模組名稱（不含 .py）

        Returns:
            載入的模組物件
        """
        module_path = self.tools_dir / f"{module_name}.py"
        if not module_path.exists():
            raise FileNotFoundError(f"模組 tools/{module_name}.py 不存在")

        full_module_name = f"tools.{module_name}"

        # 若已載入則 reload，否則初次載入
        if full_module_name in importlib.util._cache if hasattr(importlib.util, '_cache') else False:
            module = importlib.import_module(full_module_name)
            return importlib.reload(module)

        spec = importlib.util.spec_from_file_location(
            full_module_name, str(module_path)
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        raise ImportError(f"無法載入模組: {full_module_name}")

    def get_skills_summary(self) -> str:
        """
        生成技能摘要文字，用於注入 Agent 的 System Prompt。

        Returns:
            格式化的技能清單字串
        """
        self._load_capabilities()  # 重新讀取最新狀態

        if not self.capabilities:
            return "【已習得技能】目前尚無已記錄的技能。"

        lines = ["【已習得技能清單】以下是你已經開發並儲存的技能："]
        for name, info in self.capabilities.items():
            lines.append(
                f"  - {name}: {info.get('description', '無描述')} "
                f"（使用方式: {info.get('usage', 'N/A')}）"
            )
        return "\n".join(lines)

    def list_skills(self) -> list[dict]:
        """列出所有技能（優先從資料庫讀取）。"""
        db_skills = db.list_skills()
        if db_skills:
            return db_skills

        # 回退到 JSON 索引
        self._load_capabilities()
        return [
            {"name": name, "description": info.get("description", ""), "file_path": info.get("file", "")}
            for name, info in self.capabilities.items()
        ]

    def scan_tools_directory(self) -> list[str]:
        """掃描 tools/ 目錄下所有 .py 模組名稱。"""
        modules = []
        for f in self.tools_dir.iterdir():
            if f.suffix == ".py" and f.name != "__init__.py":
                modules.append(f.stem)
        return modules

    @staticmethod
    def compile_skill_function(name: str, code: str) -> Any:
        """
        使用 exec() 從程式碼字串中編譯出函數物件。

        Args:
            name: 要提取的函數名稱
            code: 完整的 Python 程式碼

        Returns:
            編譯後的函數物件，若失敗則返回 None
        """
        try:
            namespace: dict[str, Any] = {}
            exec(code, namespace)
            func = namespace.get(name)
            if callable(func):
                return func
            # 如果指定的 name 找不到，嘗試找第一個可調用的函數
            for key, val in namespace.items():
                if callable(val) and not key.startswith("_"):
                    return val
            return None
        except Exception as e:
            print(f"⚠️ 編譯技能 '{name}' 失敗: {e}")
            return None

    def load_all_skill_functions(self) -> list[tuple[str, Any]]:
        """
        從資料庫載入所有技能，編譯為可調用的函數物件。

        Returns:
            (技能名稱, 函數物件) 的列表
        """
        results = []
        skills = db.list_skills()

        for skill_info in skills:
            skill_data = db.get_skill(skill_info["name"])
            if not skill_data:
                continue

            func = self.compile_skill_function(
                skill_data["name"], skill_data["code_content"]
            )
            if func:
                results.append((skill_data["name"], func))
                print(f"  🔧 已從 DB 載入技能: {skill_data['name']}")
            else:
                print(f"  ⚠️ 無法編譯技能: {skill_data['name']}")

        return results
