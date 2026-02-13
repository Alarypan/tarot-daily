"""
通义千问塔罗解读模块 - 调用AI生成温暖的运势解读
"""

import aiohttp
from typing import List, Dict


class TongyiDivination:
    """通义千问塔罗解读"""

    def __init__(self, api_key: str, model: str = "qwen-plus"):
        self.api_key = api_key
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = model

    async def generate_reading(self, cards: List[Dict], user_date: str,
                               history: List[Dict] = None) -> str:
        """生成AI塔罗解读"""
        prompt = self._build_prompt(cards, user_date, history)

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.85,
        }

        try:
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=headers, json=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error_text = await resp.text()
                        raise Exception(f"API调用失败 ({resp.status}): {error_text}")
        except Exception as e:
            # 降级：返回基于关键词的简单解读
            return self._fallback_reading(cards, str(e))

    def _build_prompt(self, cards: List[Dict], user_date: str,
                      history: List[Dict] = None) -> str:
        """构建解读Prompt"""
        card_summaries = []
        for card_info in cards:
            card = card_info["card"]
            ori = card_info["orientation"]
            pos = card_info["position"]
            keywords = " / ".join(card_info["keywords"])
            meaning = card_info["meaning"]

            card_summaries.append(
                f"【{pos}】{card.name_cn}（{card.name_en}）- {ori}\n"
                f"  关键词：{keywords}\n"
                f"  含义：{meaning}"
            )

        cards_text = "\n\n".join(card_summaries)

        # 构建历史记录部分
        history_section = ""
        if history:
            history_lines = []
            for day in history:
                date = day["date"]
                day_cards = day["cards"]
                card_strs = [
                    f"{c['name_cn']}（{c['orientation']}）[{c['position']}]"
                    for c in day_cards
                ]
                history_lines.append(f"  {date}：{' | '.join(card_strs)}")

            history_text = "\n".join(history_lines)
            history_section = f"""

【近期抽牌历史】
{history_text}

请在解读中增加一个段落：
   - 【运势流动】（100-150字）
     结合近几天的牌面变化趋势，分析运势的整体走向
     指出能量的转变方向（如：从低谷走向恢复、从迷茫到清晰等）
     给出顺应趋势的建议"""

        prompt = f"""你是一位温暖、富有人文关怀的塔罗师，擅长用生活化的语言为人们解读塔罗牌。

今天是 {user_date}，有人向你抽取了每日塔罗牌，希望了解今天的运势指引。

【抽取的三张牌】
{cards_text}
{history_section}

【解读要求】
1. 语气风格：
   - 温暖陪伴者的口吻，像朋友在关心你
   - 避免"您"等疏离称呼，直接用"你"
   - 语言自然流畅，避免"首先、其次、综上所述"等AI句式
   - 用"也许""不妨""说不定"等柔和表达

2. 内容结构（约400-600字，有历史记录时约500-700字）：
   - 【今日整体运势】（100-150字）
     基于三张牌的组合，给出今天的整体能量走向
     用"过去-现在-未来"的时间线串联三张牌

   - 【事业与财运】（80-120字）
     工作/学习/金钱相关的具体指引
     给出可落地的行动建议

   - 【情感与人际】（80-120字）
     关系、沟通、情绪相关的提醒

   - 【今日温馨提示】（50-80字）
     一句温暖的鼓励，体现生命的温度

3. 禁止事项：
   - 不要使用"综上所述""总而言之"等总结词
   - 不要机械罗列"第一、第二、第三"
   - 不要说"愿您""祝您"，直接说"希望你"
   - 不要过度玄学化或神秘化
   - 不要给出绝对化预言

4. 输出格式：直接输出解读内容，用空行分隔段落，每段标题用【】标记。"""

        return prompt

    def _fallback_reading(self, cards: List[Dict], error_msg: str) -> str:
        """API失败时的降级解读"""
        # 只保留简洁的错误提示
        short_error = error_msg.split(":")[0] if ":" in error_msg else error_msg
        if "Arrearage" in error_msg:
            short_error = "通义千问账户需要充值"
        lines = [f"（AI解读暂时不可用：{short_error}，以下为牌面基础解读）\n"]

        for card_info in cards:
            card = card_info["card"]
            ori = card_info["orientation"]
            pos = card_info["position"]

            lines.append(f"【{pos} - {card.name_cn}（{ori}）】")
            lines.append(f"{card_info['meaning']}\n")

        return "\n".join(lines)
