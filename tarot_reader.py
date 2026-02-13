"""
塔罗牌抽牌逻辑 - 基于日期种子的随机抽牌
"""

import hashlib
import random
from datetime import datetime
from typing import List, Dict
from tarot_data import TAROT_DECK, TarotCard


class TarotReader:
    """塔罗牌抽牌器"""

    POSITIONS = ["过去", "现在", "未来"]

    def __init__(self):
        self.deck = TAROT_DECK

    def draw_daily_cards(self, date: str = None) -> List[Dict]:
        """
        抽取每日三张牌

        Args:
            date: 日期字符串（YYYY-MM-DD），默认今天

        Returns:
            三张牌的信息列表
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # 基于日期生成随机种子，确保同一天结果一致
        seed = int(hashlib.md5(date.encode("utf-8")).hexdigest()[:8], 16)
        rng = random.Random(seed)

        # 抽取3张不重复的牌
        selected_indices = rng.sample(range(len(self.deck)), 3)

        results = []
        for i, idx in enumerate(selected_indices):
            card = self.deck[idx]
            orientation = rng.choice(["正位", "逆位"])

            is_upright = orientation == "正位"
            results.append({
                "card": card,
                "orientation": orientation,
                "position": self.POSITIONS[i],
                "keywords": card.upright_keywords if is_upright else card.reversed_keywords,
                "meaning": card.upright_meaning if is_upright else card.reversed_meaning,
            })

        return results
