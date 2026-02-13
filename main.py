"""
塔罗牌每日运势 - 主程序入口（网页版）
双击运行后自动在浏览器中打开塔罗解读页面
"""

import sys
import os
import asyncio
import webbrowser
from datetime import datetime
from pathlib import Path

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def check_dependencies():
    """检查并安装依赖"""
    print("  🔍  检查运行环境...")

    required = {"aiohttp": "aiohttp", "dotenv": "python-dotenv"}
    missing = []

    for import_name, pip_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f"  📦  正在安装组件: {', '.join(missing)}")
        import subprocess
        for pkg in missing:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        print("  ✅  组件安装完成")
    else:
        print("  ✅  环境检查通过")


def load_api_key() -> str:
    """加载API Key"""
    from dotenv import load_dotenv

    script_dir = Path(__file__).parent
    env_paths = [
        script_dir / ".env",
        Path.home() / "Desktop" / "潘冰清内容工作台" / ".env",
        Path.home() / "Desktop" / "hotspot-content-agent" / ".env",
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

    api_key = os.environ.get("TONGYI_API_KEY")
    if not api_key:
        print("  ❌  未找到 TONGYI_API_KEY，请在 .env 文件中配置")
        print(f"     .env 文件位置：{script_dir / '.env'}")
        print("     格式：TONGYI_API_KEY=你的API密钥\n")
        input("按回车键关闭...")
        sys.exit(1)

    return api_key


async def main():
    """主流程"""
    from tarot_reader import TarotReader
    from tongyi_divination import TongyiDivination
    from web_template import generate_html
    from history_store import save_today, get_recent_history

    today = datetime.now().strftime("%Y-%m-%d")
    weekday = WEEKDAYS[datetime.now().weekday()]
    script_dir = Path(__file__).parent
    output_path = script_dir / "tarot_reading.html"

    print(f"\n  ✨  塔罗牌每日运势  ✨")
    print(f"  📅  {today}  {weekday}\n")

    # 1. 抽牌
    reader = TarotReader()
    cards = reader.draw_daily_cards(today)
    for card_info in cards:
        card = card_info["card"]
        print(f"  🔮  【{card_info['position']}】{card.name_cn} — {card_info['orientation']}")
    print()

    # 2. 获取历史记录
    history = get_recent_history(today, days=3)
    if history:
        print(f"  📜  找到 {len(history)} 天的历史记录，将进行运势流动分析")
    else:
        print("  📜  首次使用，暂无历史记录")

    # 3. AI解读
    print("  🌟  正在为你解读今日运势...")
    api_key = load_api_key()
    model = os.environ.get("TONGYI_MODEL", "qwen-plus")
    divination = TongyiDivination(api_key, model)
    reading = await divination.generate_reading(cards, today, history)
    print("  ✅  解读完成")

    # 4. 保存今日记录
    save_today(today, cards)
    print("  💾  今日牌面已保存")

    # 5. 生成HTML页面
    html = generate_html(today, weekday, cards, reading, history)
    output_path.write_text(html, encoding="utf-8")
    print(f"  📄  页面已生成：{output_path.name}")

    # 4. 打开浏览器
    file_url = output_path.as_uri()
    webbrowser.open(file_url)
    print("  🌐  已在浏览器中打开\n")
    print("  ✨  愿你今天平安喜乐  ✨\n")


if __name__ == "__main__":
    try:
        check_dependencies()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  👋  再见！\n")
    except Exception as e:
        print(f"\n  ❌  运行出错：{e}\n")

    input("按回车键关闭窗口...")
