"""
命令行展示美化模块
"""

import textwrap
from datetime import datetime
from typing import List, Dict


WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 大阿卡纳专属符号
MAJOR_SYMBOLS = {
    "愚者": "🃏", "魔术师": "🎩", "女祭司": "🌙", "皇后": "👑",
    "皇帝": "⚜️", "教皇": "📿", "恋人": "💕", "战车": "🏇",
    "力量": "🦁", "隐士": "🕯️", "命运之轮": "🎡", "正义": "⚖️",
    "倒吊人": "🙃", "死神": "💀", "节制": "🍷", "恶魔": "😈",
    "高塔": "⚡", "星星": "⭐", "月亮": "🌛", "太阳": "☀️",
    "审判": "📯", "世界": "🌍",
}

# 小阿卡纳花色符号
SUIT_SYMBOLS = {
    "权杖": "🔥", "圣杯": "💧", "宝剑": "⚔️", "星币": "💰",
}


def print_banner(date: str):
    """打印欢迎横幅"""
    day_of_week = WEEKDAYS[datetime.strptime(date, "%Y-%m-%d").weekday()]

    print("\n" + "=" * 56)
    print("          ✨  塔罗牌每日运势  ✨")
    print("=" * 56)
    print(f"  📅  {date}  {day_of_week}")
    print("=" * 56 + "\n")


def show_cards(cards: List[Dict]):
    """展示抽取的三张牌"""
    print("  🔮  今日抽取的塔罗牌：\n")

    for card_info in cards:
        card = card_info["card"]
        orientation = card_info["orientation"]
        position = card_info["position"]

        # 选择合适的符号
        if card.category == "大阿卡纳":
            symbol = MAJOR_SYMBOLS.get(card.name_cn, "🌟")
        else:
            symbol = SUIT_SYMBOLS.get(card.suit, "✦")

        # 逆位用特殊标记
        ori_mark = "↑" if orientation == "正位" else "↓"

        keywords_str = " / ".join(card_info["keywords"])

        print(f"  {symbol}  【{position}】 {card.name_cn} — {orientation} {ori_mark}")
        print(f"        关键词：{keywords_str}")
        print()


def show_reading(reading_text: str):
    """展示AI解读"""
    print("-" * 56)
    print("  💫  今日运势解读")
    print("-" * 56 + "\n")

    paragraphs = reading_text.split("\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            print()
            continue
        # 标题行不换行
        if para.startswith("【"):
            print(f"  {para}")
        else:
            wrapped = textwrap.fill(para, width=52, initial_indent="  ", subsequent_indent="  ")
            print(wrapped)

    print()


def print_footer():
    """打印结尾"""
    print("-" * 56)
    print("          ✨  愿你今天平安喜乐  ✨")
    print("-" * 56 + "\n")
