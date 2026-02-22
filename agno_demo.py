from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.shell import ShellTools
from agno.tools.python import PythonTools

# 建立一個具備「自我進化與錯誤修復能力」的 Agent
self_evolving_agent = Agent(
    name="Self-Evolving Agent Pro",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[ShellTools(), PythonTools()],
    instructions=[
        "你是一個具備自我擴充與錯誤自癒能力的 AI 助手。",
        "【自我擴充】如果任務需要外部套件，主動使用 ShellTools 執行 `pip install`。",
        "【知識累積】如果你寫出了一個好用的函數，請將其存入 `tools/` 目錄。例如：`tools/my_custom_tool.py`。",
        "【工具發現】每次開始任務前，請先檢查 `tools/` 目錄下有哪些你之前寫過的 .py 檔案。如果需要，你可以透過 PythonTools 使用 `from tools.my_custom_tool import ...` 來調用它們。",
        "【錯誤修復】如果 Python 代碼執行報錯，必須分析原因，修正後自動重試。",
    ],
    show_tool_calls=True,
    markdown=True,
)

# 測試任務：要求它安裝 qrcode 套件並生成一個 QR Code 檔案
self_evolving_agent.print_response("請幫我安裝 qrcode 套件，並寫一段 Python 代碼生成一個連向 'https://docs.agno.com' 的 QR Code 圖片，存為 agno_qr.png", stream=True)
