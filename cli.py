"""
互動式 CLI 入口
提供 REPL 風格的對話介面來與 Self-Evolving Agent 互動。
"""

import sys
from agent_core import create_agent
from capability_manager import CapabilityManager


def print_banner() -> None:
    """顯示程式啟動橫幅。"""
    print("\n" + "=" * 60)
    print("🧠 Self-Evolving Agent — 互動式 CLI")
    print("=" * 60)
    print("指令：")
    print("  /skills   — 查看已習得技能")
    print("  /reload   — 重新載入技能清單")
    print("  /quit     — 退出程式")
    print("=" * 60 + "\n")


def handle_command(command: str, cap_manager: CapabilityManager) -> bool:
    """
    處理特殊指令。

    Args:
        command: 使用者輸入的指令
        cap_manager: 技能管理器

    Returns:
        True 表示已處理，False 表示非特殊指令
    """
    cmd = command.strip().lower()

    if cmd == "/quit":
        print("\n👋 再見！")
        sys.exit(0)

    if cmd == "/skills":
        skills = cap_manager.list_skills()
        if not skills:
            print("📭 目前尚無已儲存的技能。")
        else:
            print("\n📚 已習得技能清單：")
            for s in skills:
                print(f"  - {s['name']}: {s.get('description', '無描述')}")
        print()
        return True

    if cmd == "/reload":
        cap_manager._load_capabilities()
        print("🔄 技能清單已重新載入。\n")
        return True

    return False


def main() -> None:
    """CLI 主迴圈。"""
    print_banner()

    print("🚀 正在初始化 Agent...")
    agent = create_agent()
    cap_manager = CapabilityManager()
    print("✅ Agent 已就緒！\n")

    while True:
        try:
            user_input = input("👤 你: ").strip()

            if not user_input:
                continue

            # 處理特殊指令
            if user_input.startswith("/"):
                if handle_command(user_input, cap_manager):
                    continue

            # 發送給 Agent 處理
            print("\n🤖 Agent:")
            agent.print_response(user_input, stream=True)
            print()

        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤: {e}\n")


if __name__ == "__main__":
    main()
