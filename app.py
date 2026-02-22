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

# 建立 Agent 實例 (支援三種模型)
agent_gpt5 = create_agent(
    agent_name="Self-Evolving Agent (GPT-4o-mini)", 
    agent_id="self-evolving-agent-gpt-5-mini", 
    model_id="gpt-5-mini" # 或您的 provider 對應 id
)

agent_r1 = create_agent(
    agent_name="Self-Evolving Agent (DeepSeek Reasoner)", 
    agent_id="self-evolving-agent-deepseek-reasoner", 
    model_id="deepseek-reasoner"
)

agent_v3 = create_agent(
    agent_name="Self-Evolving Agent (DeepSeek Chat)", 
    agent_id="self-evolving-agent-deepseek-chat", 
    model_id="deepseek-chat"
)

# 建立 AgentOS 並掛載 AGUI 介面
agent_os = AgentOS(
    agents=[agent_gpt5, agent_r1, agent_v3],
    interfaces=[AGUI(agent=agent_gpt5)], # AGUI 需要一個預設 agent
)

# 取得 FastAPI app 實例
app = agent_os.get_app()

from fastapi.middleware.cors import CORSMiddleware

# 掛載 charts/ 靜態目錄，讓 Plotly HTML 圖表可透過 /charts/ 路徑存取
app.mount("/charts", StaticFiles(directory=str(CHARTS_DIR), html=True), name="charts")

# 允許前端 (Vite) 的跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("🌐 啟動 AGUI Web 介面...")
    print("📍 Agent 介面: http://localhost:7777")
    print("📊 圖表目錄:   http://localhost:7777/charts/")
    print("按 Ctrl+C 停止伺服器\n")
    agent_os.serve(app="app:app", host="localhost", port=7777, reload=True)
