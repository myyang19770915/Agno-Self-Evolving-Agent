# SDD: Self-Evolving Agent (Agno Framework)

## 專案目標
打造一個基於 Agno 框架，具備「自我擴充能力」、「錯誤自癒」與「技能記憶」的 AI Agent 系統。

## 核心需求
1. **自我擴充 (Self-Extension)**：當任務需要額外功能或 Python 套件時，Agent 能主動執行 `pip install` 並撰寫所需的腳本。
2. **錯誤自癒 (Error Healing)**：執行代碼報錯時，Agent 必須讀取錯誤日誌（Traceback），自行修復代碼並重新執行，不應輕易終止任務。
3. **技能記憶 (Capability Memory)**：
   - Agent 寫出的實用函數應存放在 `tools/` 目錄。
   - 使用 `tools/capabilities.json` 維護一份技能清單。
   - 每次啟動任務前，Agent 會自動掃描清單，避免重複開發並能直接調用既有技能。
4. **雲端備份**：專案內容需定期同步至 Google Drive (`OpenClaw_Projects/agno_project/`)。

## 專案結構
- `agno/`
  - `agno_ultra.py`: 具備記憶與自癒能力的最新核心腳本。
  - `agno_demo.py`: 基礎擴充能力展示腳本。
  - `dynamic_manager.py`: (預留) 動態工具載入管理器。
  - `tools/`:
    - `__init__.py`: 使其成為 Python Package。
    - `capabilities.json`: 記錄 Agent 已習得的技能與用法。
    - `*.py`: Agent 自主生成的技能檔案（例如 `crypto.py`）。

## 執行流程
1. **初始化**：檢查目錄結構，確保 `tools/` 與 `capabilities.json` 存在。
2. **環境確認**：確保 `agno` 與 `google-genai` 已安裝。
3. **讀取清單**：Agent 載入 `capabilities.json`。
4. **任務執行**：
   - 判斷是否需要新技能。
   - 若需要，撰寫並存檔。
   - 更新 `capabilities.json`。
5. **備份**：完成任務後同步至雲端。

## 開發紀錄 (2026-02-19)
- 解決了 Debian 環境下 Python `externally-managed-environment` 的安裝問題（使用 `--break-system-packages`）。
- 修復了 Agno `Agent` 初始化參數 `show_tool_calls` 的相容性問題（在最新版本中移除或更換名稱）。
- 完成了第一版自我記憶指令集。
