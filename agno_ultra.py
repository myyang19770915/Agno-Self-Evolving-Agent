import os
import json
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.shell import ShellTools
from agno.tools.python import PythonTools

# 確保目錄存在
os.makedirs("tools", exist_ok=True)
if not os.path.exists("tools/__init__.py"):
    with open("tools/__init__.py", "w") as f:
        pass

# 建立一個具備「能力清單管理」的 Agent
self_evolving_agent = Agent(
    name="Self-Evolving Agent Ultra",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[ShellTools(), PythonTools()],
    instructions=[
        "你是一個具備自我擴充、錯誤自癒與能力記憶能力的 AI 助手。",
        "【能力清單】你有一份能力清單存放在 `tools/capabilities.json`。每次任務開始前，請讀取它以了解你已具備的技能。",
        "【技能開發】如果你寫出了一個具備重複使用價值的函數，請執行以下步驟：",
        "  1. 將函數寫入 `tools/` 目錄下的 .py 檔案。",
        "  2. 更新 `tools/capabilities.json`，記錄檔案名稱、函數名稱與功能描述。",
        "【能力調用】如果清單中已存在所需技能，請直接使用 `from tools.檔案名稱 import 函數名` 來調用。",
        "【自我擴充】如果缺套件，請用 ShellTools 執行 `pip install`。",
        "【錯誤修復】執行報錯時，分析原因並修正，直到任務成功。",
    ],
    markdown=True,
)

# 執行一個會觸發「新技能開發」的任務
task = "請幫我開發一個名為 'text_to_sha256' 的技能，將字串轉為 SHA256 哈希值。請將它存入 tools/crypto.py，並更新 capabilities.json 清單。最後，使用這個新技能幫我計算 'Hello Agno' 的哈希值。"

print(f"🚀 開始執行任務: {task}")
self_evolving_agent.print_response(task, stream=True)
