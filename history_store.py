"""
历史记录存储 - 保存每日塔罗抽牌结果用于运势流动分析
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


HISTORY_FILE = Path(__file__).parent / "tarot_history.json"
MAX_HISTORY_DAYS = 30  # 最多保留30天记录


def load_history() -> Dict:
    """加载历史记录"""
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_today(date: str, cards: List[Dict]):
    """保存今日抽牌结果"""
    history = load_history()

    # 保存今日数据
    history[date] = {
        "cards": [
            {
                "name_cn": c["card"].name_cn,
                "name_en": c["card"].name_en,
                "category": c["card"].category,
                "suit": c["card"].suit,
                "orientation": c["orientation"],
                "position": c["position"],
                "keywords": c["keywords"],
            }
            for c in cards
        ],
    }

    # 清理超过30天的旧记录
    cutoff = (datetime.now() - timedelta(days=MAX_HISTORY_DAYS)).strftime("%Y-%m-%d")
    history = {k: v for k, v in history.items() if k >= cutoff}

    HISTORY_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_recent_history(today: str, days: int = 3) -> List[Dict]:
    """获取最近几天的历史记录（不含今天）"""
    history = load_history()
    recent = []

    for i in range(1, days + 1):
        past_date = (
            datetime.strptime(today, "%Y-%m-%d") - timedelta(days=i)
        ).strftime("%Y-%m-%d")
        if past_date in history:
            recent.append({"date": past_date, **history[past_date]})

    return recent  # 按时间倒序（最近的在前）
