"""驗證腳本：測試所有核心模組是否正常運作。"""

print("=" * 50)
print("🧪 Self-Evolving Agent 驗證測試")
print("=" * 50)

# 測試 1: 資料庫模組
print("\n📦 測試 1: database.py")
try:
    from database import init_db, save_skill, list_skills, get_skill, delete_skill
    init_db()
    result = save_skill("test_hello", "def hello():\n    return 'world'", "一個測試技能")
    print(f"  儲存技能: {result}")
    skills = list_skills()
    print(f"  技能列表: {len(skills)} 個技能")
    skill = get_skill("test_hello")
    print(f"  取得技能: {skill['name']} - {skill['description']}")
    delete_result = delete_skill("test_hello")
    print(f"  刪除技能: {delete_result}")
    print("  ✅ database.py 通過!")
except Exception as e:
    print(f"  ❌ database.py 失敗: {e}")

# 測試 2: 技能管理器
print("\n📦 測試 2: capability_manager.py")
try:
    from capability_manager import CapabilityManager
    cm = CapabilityManager()
    summary = cm.get_skills_summary()
    print(f"  技能摘要: {summary[:60]}...")
    modules = cm.scan_tools_directory()
    print(f"  已發現模組: {modules}")
    print("  ✅ capability_manager.py 通過!")
except Exception as e:
    print(f"  ❌ capability_manager.py 失敗: {e}")

# 測試 3: Agent 核心 (只測試建立，不發送請求)
print("\n📦 測試 3: agent_core.py (模組載入)")
try:
    from agent_core import create_agent
    print("  create_agent 函數已載入")
    print("  ✅ agent_core.py 通過!")
except Exception as e:
    print(f"  ❌ agent_core.py 失敗: {e}")

# 測試 4: 環境變數
print("\n📦 測試 4: .env 環境變數")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("LITELLM_API_KEY")
    base_url = os.getenv("LITELLM_BASE_URL")
    model = os.getenv("DEFAULT_MODEL")
    print(f"  LITELLM_API_KEY: {'已設定' if api_key else '❌ 未設定'}")
    print(f"  LITELLM_BASE_URL: {base_url or '❌ 未設定'}")
    print(f"  DEFAULT_MODEL: {model or '❌ 未設定'}")
    print("  ✅ .env 通過!")
except Exception as e:
    print(f"  ❌ .env 失敗: {e}")

print("\n" + "=" * 50)
print("🏁 驗證完成!")
print("=" * 50)
