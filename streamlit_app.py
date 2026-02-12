"""
塔罗牌每日运势 - Streamlit 网页版
可部署到 Streamlit Cloud 分享给朋友
"""

import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta
import json
from pathlib import Path
import os

# ========== 页面配置 ==========
st.set_page_config(
    page_title="塔罗牌每日运势",
    page_icon="🔮",
    layout="centered",
)

# ========== 样式 ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

.main {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2b 100%);
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2b 100%);
}

h1, h2, h3 {
    font-family: 'Noto Serif SC', serif !important;
    color: #f0d890 !important;
}

.card-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.tarot-card {
    text-align: center;
    padding: 15px;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    border: 1px solid rgba(240, 216, 144, 0.2);
}

.tarot-card img {
    width: 150px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.tarot-card.reversed img {
    transform: rotate(180deg);
}

.card-name {
    color: #f0d890;
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 10px;
}

.card-position {
    color: #a098b0;
    font-size: 0.9em;
    margin-bottom: 5px;
}

.orientation-up {
    color: #90e0a0;
    font-size: 0.85em;
}

.orientation-down {
    color: #e0a090;
    font-size: 0.85em;
}

.keywords {
    color: #b0a8c0;
    font-size: 0.8em;
    margin-top: 8px;
}

.reading-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(240, 216, 144, 0.15);
    border-radius: 16px;
    padding: 25px;
    margin-top: 30px;
    color: #d8d0c0;
    line-height: 1.8;
}

.blessing {
    text-align: center;
    color: #f0d890;
    font-size: 1.1em;
    margin-top: 30px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ========== 塔罗牌数据（简化版，22张大阿卡纳） ==========
MAJOR_ARCANA = [
    {"id": 0, "name_cn": "愚者", "name_en": "The Fool", "img": "m00",
     "upright": ["新开始", "冒险", "纯真"], "reversed": ["鲁莽", "逃避", "不成熟"],
     "upright_meaning": "一段全新旅程即将开始，怀着纯真的心去探索未知。",
     "reversed_meaning": "可能在没有准备的情况下冲动行事，需要在勇气和理性之间找到平衡。"},
    {"id": 1, "name_cn": "魔术师", "name_en": "The Magician", "img": "m01",
     "upright": ["创造力", "技能", "意志力"], "reversed": ["欺骗", "才能浪费", "缺乏方向"],
     "upright_meaning": "你拥有实现目标所需的一切资源和能力，现在是将想法变为现实的好时机。",
     "reversed_meaning": "可能在浪费天赋或迷失方向，需要重新聚焦目标。"},
    {"id": 2, "name_cn": "女祭司", "name_en": "The High Priestess", "img": "m02",
     "upright": ["直觉", "潜意识", "内在智慧"], "reversed": ["忽视直觉", "表面化", "过度理性"],
     "upright_meaning": "此刻需要倾听内心的声音，答案就藏在你的直觉里。",
     "reversed_meaning": "你可能过于依赖逻辑而忽略了内心的感受。"},
    {"id": 3, "name_cn": "皇后", "name_en": "The Empress", "img": "m03",
     "upright": ["丰盛", "滋养", "创造", "美感"], "reversed": ["过度依赖", "创造力受阻", "匮乏感"],
     "upright_meaning": "生活中充满丰盛和温柔的能量，适合去创造、去感受美好。",
     "reversed_meaning": "可能过度照顾他人而忽略了自己的需求。"},
    {"id": 4, "name_cn": "皇帝", "name_en": "The Emperor", "img": "m04",
     "upright": ["权威", "结构", "稳定", "纪律"], "reversed": ["专制", "僵化", "控制欲"],
     "upright_meaning": "现在需要用理性和纪律来构建秩序，稳步前行。",
     "reversed_meaning": "可能过于执着于控制一切，反而失去了灵活性。"},
    {"id": 5, "name_cn": "教皇", "name_en": "The Hierophant", "img": "m05",
     "upright": ["传统", "指引", "信仰", "教育"], "reversed": ["打破常规", "挑战权威", "自由思考"],
     "upright_meaning": "适合向有经验的人请教或学习，遵循成熟的方法论。",
     "reversed_meaning": "你可能对既定规则感到不满，想要走出自己的路。"},
    {"id": 6, "name_cn": "恋人", "name_en": "The Lovers", "img": "m06",
     "upright": ["爱情", "选择", "和谐", "连接"], "reversed": ["价值观冲突", "关系不和", "犹豫不决"],
     "upright_meaning": "面临重要的选择，需要跟随内心的价值观做决定。",
     "reversed_meaning": "可能在某个选择上左右为难，需要正视内心真正的需求。"},
    {"id": 7, "name_cn": "战车", "name_en": "The Chariot", "img": "m07",
     "upright": ["胜利", "意志力", "决心", "前进"], "reversed": ["失控", "方向迷失", "挫败"],
     "upright_meaning": "凭借坚定的意志力和决心，你能克服眼前的困难。",
     "reversed_meaning": "感觉事情脱离了掌控，也许需要重新调整策略。"},
    {"id": 8, "name_cn": "力量", "name_en": "Strength", "img": "m08",
     "upright": ["内在力量", "勇气", "耐心", "温柔"], "reversed": ["自我怀疑", "脆弱", "缺乏自信"],
     "upright_meaning": "真正的力量来自内心的温柔与坚韧，以柔克刚更有效。",
     "reversed_meaning": "可能正在经历自我怀疑，允许脆弱的存在，重新找回平衡。"},
    {"id": 9, "name_cn": "隐士", "name_en": "The Hermit", "img": "m09",
     "upright": ["内省", "独处", "寻找真相", "智慧"], "reversed": ["孤僻", "逃避社交", "过度封闭"],
     "upright_meaning": "现在适合给自己一些独处和思考的时间，向内探索会带来领悟。",
     "reversed_meaning": "独处太久可能变成逃避，是时候走出来和外界建立连接。"},
    {"id": 10, "name_cn": "命运之轮", "name_en": "Wheel of Fortune", "img": "m10",
     "upright": ["转折", "好运", "命运", "机遇"], "reversed": ["厄运", "抗拒变化", "失控"],
     "upright_meaning": "命运的齿轮正在转动，这是一个充满机遇的转折点。",
     "reversed_meaning": "生活中似乎出现了一些不如意的变化，记住低谷是暂时的。"},
    {"id": 11, "name_cn": "正义", "name_en": "Justice", "img": "m11",
     "upright": ["公正", "因果", "真相", "责任"], "reversed": ["不公", "逃避责任", "偏见"],
     "upright_meaning": "因果法则正在运作，需要诚实面对自己，承担应有的责任。",
     "reversed_meaning": "可能感受到某种不公正，或者在逃避某些责任。"},
    {"id": 12, "name_cn": "倒吊人", "name_en": "The Hanged Man", "img": "m12",
     "upright": ["暂停", "牺牲", "换角度", "等待"], "reversed": ["拖延", "无谓牺牲", "固执"],
     "upright_meaning": "有时候停下来不是退步，换一个角度看问题会发现答案一直在那里。",
     "reversed_meaning": "可能一直在原地打转，不愿意做出必要的改变。"},
    {"id": 13, "name_cn": "死神", "name_en": "Death", "img": "m13",
     "upright": ["结束", "转变", "新生", "蜕变"], "reversed": ["抗拒结束", "恐惧改变", "停滞"],
     "upright_meaning": "某个阶段正在走向终结，但结束意味着新的开始，这是深层的蜕变。",
     "reversed_meaning": "你可能紧紧抓着不该留的东西不放，学会优雅地告别。"},
    {"id": 14, "name_cn": "节制", "name_en": "Temperance", "img": "m14",
     "upright": ["平衡", "调和", "耐心", "适度"], "reversed": ["失衡", "过度", "急躁"],
     "upright_meaning": "现在最需要的是平衡与适度，耐心地调和矛盾。",
     "reversed_meaning": "生活的某个方面可能失去了平衡，需要重新校准节奏。"},
    {"id": 15, "name_cn": "恶魔", "name_en": "The Devil", "img": "m15",
     "upright": ["束缚", "欲望", "诱惑", "阴暗面"], "reversed": ["解脱", "打破束缚", "觉醒"],
     "upright_meaning": "可能被某种欲望或不健康的模式所束缚，但锁链其实很松。",
     "reversed_meaning": "正在从某种束缚中挣脱出来，这是觉醒和释放的好兆头。"},
    {"id": 16, "name_cn": "高塔", "name_en": "The Tower", "img": "m16",
     "upright": ["突变", "崩塌", "颠覆", "真相揭露"], "reversed": ["恐惧变化", "勉强维持", "内在危机"],
     "upright_meaning": "一些看似稳固的东西可能突然被打破，重建需要从真实开始。",
     "reversed_meaning": "你感觉到变化即将来临却在抗拒它，不如主动做出调整。"},
    {"id": 17, "name_cn": "星星", "name_en": "The Star", "img": "m17",
     "upright": ["希望", "疗愈", "灵感", "平静"], "reversed": ["失望", "缺乏信心", "迷茫"],
     "upright_meaning": "经历风雨之后，希望的光芒正在照耀你，这是疗愈和恢复的时期。",
     "reversed_meaning": "可能暂时看不到希望的光，给自己一些时间，阴霾终会散去。"},
    {"id": 18, "name_cn": "月亮", "name_en": "The Moon", "img": "m18",
     "upright": ["幻觉", "不安", "直觉", "恐惧"], "reversed": ["走出迷惑", "真相浮现", "克服恐惧"],
     "upright_meaning": "事情可能不像表面看起来那样，等迷雾散去后再看清全貌。",
     "reversed_meaning": "之前困扰你的迷惑正在消散，你开始看清事情的真相。"},
    {"id": 19, "name_cn": "太阳", "name_en": "The Sun", "img": "m19",
     "upright": ["成功", "快乐", "活力", "乐观"], "reversed": ["暂时受阻", "过度乐观", "延迟的快乐"],
     "upright_meaning": "阳光普照的好日子！充满活力和正面的能量，一切都在往好的方向发展。",
     "reversed_meaning": "好事可能来得比预期慢一些，阳光还在，只是需要多一点耐心。"},
    {"id": 20, "name_cn": "审判", "name_en": "Judgement", "img": "m20",
     "upright": ["觉醒", "重生", "反思", "召唤"], "reversed": ["自我怀疑", "逃避审视", "害怕评价"],
     "upright_meaning": "一个深刻的内在觉醒正在发生，这是重新审视自己、做出重大决定的时刻。",
     "reversed_meaning": "可能在逃避面对自己内心深处的声音，成长需要勇气正视过去。"},
    {"id": 21, "name_cn": "世界", "name_en": "The World", "img": "m21",
     "upright": ["圆满", "完成", "成就", "整合"], "reversed": ["未完成", "缺乏闭合", "不圆满"],
     "upright_meaning": "一个重要的阶段正在圆满结束，所有的努力终于有了成果。",
     "reversed_meaning": "可能还有一些事情没有完全了结，补上缺失的那一块就圆满了。"},
]

IMG_BASE = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards"


def get_image_url(img_code: str) -> str:
    return f"{IMG_BASE}/{img_code}.jpg"


def draw_cards(date_str: str):
    """根据日期抽取3张牌"""
    seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    
    selected = rng.sample(MAJOR_ARCANA, 3)
    positions = ["过去", "现在", "未来"]
    
    results = []
    for i, card in enumerate(selected):
        is_upright = rng.choice([True, False])
        results.append({
            "card": card,
            "position": positions[i],
            "is_upright": is_upright,
            "orientation": "正位" if is_upright else "逆位",
            "keywords": card["upright"] if is_upright else card["reversed"],
            "meaning": card["upright_meaning"] if is_upright else card["reversed_meaning"],
        })
    return results


def call_ai_reading(cards, date_str, api_key):
    """调用通义千问生成解读"""
    import requests
    
    card_summaries = []
    for c in cards:
        card = c["card"]
        card_summaries.append(
            f"【{c['position']}】{card['name_cn']} - {c['orientation']}\n"
            f"  关键词：{' / '.join(c['keywords'])}\n"
            f"  含义：{c['meaning']}"
        )
    cards_text = "\n\n".join(card_summaries)
    
    prompt = f"""你是一位温暖、富有人文关怀的塔罗师。

今天是 {date_str}，有人抽取了每日塔罗牌：

{cards_text}

请用温暖的口吻生成约400字的解读，包含：
- 【今日整体运势】用"过去-现在-未来"串联三张牌
- 【事业与财运】具体指引和建议
- 【情感与人际】关系和沟通提醒
- 【今日温馨提示】一句温暖的鼓励

要求：语言自然，像朋友聊天，避免AI套话。"""

    try:
        resp = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "qwen-plus",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1200,
                "temperature": 0.85,
            },
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return None
    except Exception as e:
        return None


# ========== 主界面 ==========
st.markdown("<h1 style='text-align:center;'>🔮 塔罗牌每日运势</h1>", unsafe_allow_html=True)

today = datetime.now().strftime("%Y-%m-%d")
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
st.markdown(f"<p style='text-align:center; color:#a098b0;'>📅 {today} {weekday}</p>", unsafe_allow_html=True)

# 抽牌按钮
if st.button("✨ 抽取今日塔罗牌", use_container_width=True):
    st.session_state.cards = draw_cards(today)
    st.session_state.reading = None

# 显示牌面
if "cards" in st.session_state and st.session_state.cards:
    cards = st.session_state.cards
    
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>今日牌面</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, c in enumerate(cards):
        card = c["card"]
        with cols[i]:
            st.markdown(f"<p class='card-position' style='text-align:center; color:#a098b0;'>{c['position']}</p>", unsafe_allow_html=True)
            
            img_url = get_image_url(card["img"])
            if c["is_upright"]:
                st.image(img_url, use_container_width=True)
            else:
                st.markdown(f"<img src='{img_url}' style='width:100%; transform:rotate(180deg);'>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='text-align:center; color:#f0d890; font-weight:bold;'>{card['name_cn']}</p>", unsafe_allow_html=True)
            
            ori_color = "#90e0a0" if c["is_upright"] else "#e0a090"
            st.markdown(f"<p style='text-align:center; color:{ori_color}; font-size:0.9em;'>{'↑ 正位' if c['is_upright'] else '↓ 逆位'}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='text-align:center; color:#b0a8c0; font-size:0.8em;'>{' / '.join(c['keywords'])}</p>", unsafe_allow_html=True)
    
    # AI解读
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>✨ 运势解读</h3>", unsafe_allow_html=True)
    
    # 从环境变量或secrets获取API Key
    api_key = os.environ.get("TONGYI_API_KEY") or st.secrets.get("TONGYI_API_KEY", "")
    
    if api_key:
        if st.session_state.get("reading") is None:
            with st.spinner("正在为你解读今日运势..."):
                reading = call_ai_reading(cards, today, api_key)
                if reading:
                    st.session_state.reading = reading
                else:
                    st.session_state.reading = "fallback"
        
        if st.session_state.reading and st.session_state.reading != "fallback":
            st.markdown(f"<div class='reading-section'>{st.session_state.reading}</div>", unsafe_allow_html=True)
        else:
            # 降级显示
            for c in cards:
                st.markdown(f"**【{c['position']} - {c['card']['name_cn']}（{c['orientation']}）】**")
                st.write(c["meaning"])
    else:
        # 无API Key时显示基础解读
        for c in cards:
            st.markdown(f"**【{c['position']} - {c['card']['name_cn']}（{c['orientation']}）】**")
            st.write(c["meaning"])
    
    # 祝福语
    st.markdown("<div class='blessing'>✨ 愿你今天平安喜乐 ✨</div>", unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("<p style='text-align:center; color:#605878; font-size:0.8em;'>Rider-Waite Tarot · AI Powered</p>", unsafe_allow_html=True)
