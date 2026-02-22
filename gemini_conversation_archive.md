# Gemini 對話紀錄：AI Agent 設計與開發分析

> **來源**: [Gemini 分享連結](https://gemini.google.com/share/8cdc51a9d12f)
> **日期**: 2026-02-19
> **主題**: Self-Evolving Agent (基於 Agno 框架) 設計與開發

---

## 使用者提問

> 分析此附件內容

附件：`sdd.md`（軟體設計文件）

---

## Gemini AI 回應

### 一、核心架構分析

這份附件是關於 **Self-Evolving Agent (基於 Agno 框架)** 的軟體設計文件 (SDD)，目標是打造一個具備自我進化、錯誤自癒與技能記憶能力的 AI Agent。

#### 核心能力分析

1. **自我擴充 (Self-Extension)**：Agent 不僅能執行代碼，還具備管理自身環境的能力。當遇到缺失的依賴時，它能主動執行 `pip install` 並撰寫新腳本。
2. **錯誤自癒 (Error Healing)**：這是一種閉環控制邏輯。當執行報錯時，Agent 會讀取 Traceback 資訊，將錯誤作為輸入重新修正代碼，直到任務成功。
3. **技能記憶 (Capability Memory)**：透過 `tools/capabilities.json` 維護技能清單，Agent 撰寫的實用函數會被持久化，避免重複開發。
4. **雲端備份**：整合 Google Drive 同步功能，確保智慧資產具備異地備援能力。

#### 專案結構與流程

- **agno_ultra.py**：核心大腦，負責自癒與記憶整合。
- **tools/**：存放 Agent 自主生成的 `.py` 技能檔。
- **capabilities.json**：技能索引清單。

#### 開發進度與挑戰 (2026-02-19)

- 解決了 Debian 系統中 `externally-managed-environment` 的 pip 安裝限制（使用 `--break-system-packages`）。
- 修復了 Agno 框架版本更新導致的 `show_tool_calls` 參數相容性問題。

---

### 二、實作建議

#### 1. 基礎概念版 `agno_ultra.py`

包含兩個核心工具：
- **`run_python_code`**：執行 Python 代碼並自動處理錯誤（自癒邏輯）
- **`save_new_skill`**：將新技能存入 `tools/` 目錄，並更新 `capabilities.json`

#### 2. 技能清單結構 `capabilities.json`

建議採用包含 `description`, `file`, 和 `usage` 的 JSON 格式：

```json
{
  "text_to_sha256": {
    "description": "將字串轉為 SHA256 哈希值",
    "file": "crypto.py",
    "usage": "from tools.crypto import text_to_sha256"
  }
}
```

#### 3. 優化版 `agno_ultra.py` (引入 CapabilityManager)

- 使用 `importlib` 動態載入 `tools/` 目錄下的所有技能。
- **Prompt Injection**：將已習得的技能動態注入到 System Prompt 中，讓 Agent 知道它「已經會了什麼」。

---

### 三、技術深究與架構升級

#### Hot Reload (熱重載)

使用 `importlib.reload()` 確保 Agent 在同一個會話中寫入新技能後能立即使用，無需重啟程式。

#### 資料庫化 (PostgreSQL/SQLite)

將技能從實體 `.py` 檔案遷移到資料庫，實現「蜂群思維 (Hive Mind)」，讓多個 Agent 實例共享技能庫。使用 `exec()` 進行動態編譯。

**資料庫 Schema**:

```sql
CREATE TABLE agent_skills (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  code_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 安全性 (Sandboxing)

強烈建議使用 **Docker 拋棄式沙盒**（如 `python:3.10-slim` 容器）來執行 Agent 撰寫的代碼，防止危險操作（如 `rm -rf /`）。

#### 並發處理

使用 **File Locks** 或 **Session Isolation** 來防止 Race Conditions，避免多個 Agent 同時更新同一份技能記憶。

#### 資料處理優化

針對 Agent 容易產生冗餘 SQL 寫入的問題，實作 Aggregation/Limit 邏輯。

---

### 四、全端實作方案

#### Backend (FastAPI)

- Session 管理
- 動態工具編譯與執行 (`exec()`)
- 資料庫 UPSERT 邏輯
- Agent 會話管理

#### Frontend (React)

- 互動式聊天介面
- 顯示 Agent 思考過程
- 執行狀態即時更新
- 技能庫瀏覽

---

## 架構演進路線

```
Phase 1: 檔案式工具 (tools/ 目錄)
    ↓
Phase 2: 動態載入 (importlib + CapabilityManager)
    ↓
Phase 3: 資料庫化 (SQLite → Hive Mind)
    ↓
Phase 4: Docker 沙盒 + 全端介面
```
