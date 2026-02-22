"""
AGUI Web 介面入口
使用 Agno 內建的 AgentOS + AGUI 提供瀏覽器互動介面。
同時掛載 charts/ 靜態目錄供 Plotly 圖表存取。
"""

from pathlib import Path
from fastapi.staticfiles import StaticFiles

from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

from agent_core import create_agent

# 確保 charts 目錄存在
CHARTS_DIR = Path(__file__).parent / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# 建立 Agent 實例
agent = create_agent()

# 建立 AgentOS 並掛載 AGUI 介面
agent_os = AgentOS(
    agents=[agent],
    interfaces=[AGUI(agent=agent)],
)

# 取得 FastAPI app 實例
app = agent_os.get_app()

# 掛載 charts/ 靜態目錄，讓 Plotly HTML 圖表可透過 /charts/ 路徑存取
app.mount("/charts", StaticFiles(directory=str(CHARTS_DIR), html=True), name="charts")

if __name__ == "__main__":
    print("🌐 啟動 AGUI Web 介面...")
    print("📍 Agent 介面: http://localhost:7777")
    print("📊 圖表目錄:   http://localhost:7777/charts/")
    print("按 Ctrl+C 停止伺服器\n")
    agent_os.serve(app="app:app", host="localhost", port=7777, reload=True)
