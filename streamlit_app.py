"""
塔罗牌灵感指引 - Streamlit 网页版
支持多种牌阵，可部署到 Streamlit Cloud 分享给朋友
"""

import streamlit as st
import random
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import os
from io import BytesIO

# ========== 页面配置 ==========
st.set_page_config(
    page_title="塔罗牌灵感指引",
    page_icon="🔮",
    layout="centered",
)

# ========== PWA 支持 ==========
st.markdown("""
<link rel="manifest" href="./static/manifest.json">
<link rel="apple-touch-icon" href="./static/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="塔罗指引">
<meta name="theme-color" content="#6b5b95">
<meta name="mobile-web-app-capable" content="yes">
""", unsafe_allow_html=True)

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

# ========== 完整塔罗牌数据（78张） ==========

# 22张大阿卡纳
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

# 14张权杖牌
WANDS = [
    {"id": 22, "name_cn": "权杖一", "name_en": "Ace of Wands", "img": "w01",
     "upright": ["灵感", "新机会", "创造力"], "reversed": ["延迟", "缺乏动力", "错失机会"],
     "upright_meaning": "一股新的创造能量正在涌入，趁热情还在赶紧行动。",
     "reversed_meaning": "灵感似乎被堵住了，也许需要清除内心的障碍。"},
    {"id": 23, "name_cn": "权杖二", "name_en": "Two of Wands", "img": "w02",
     "upright": ["规划", "决策", "远见"], "reversed": ["恐惧未知", "计划不周", "安于现状"],
     "upright_meaning": "站在十字路口，需要做出下一步的规划和选择。",
     "reversed_meaning": "可能因为害怕未知而不敢往前走。"},
    {"id": 24, "name_cn": "权杖三", "name_en": "Three of Wands", "img": "w03",
     "upright": ["拓展", "进展", "远方"], "reversed": ["回报延迟", "眼界狭窄", "挫折"],
     "upright_meaning": "前期的投入正在显现成果，视野正在变得开阔。",
     "reversed_meaning": "期待的成果还没有到来，不要急躁。"},
    {"id": 25, "name_cn": "权杖四", "name_en": "Four of Wands", "img": "w04",
     "upright": ["庆祝", "和谐", "里程碑"], "reversed": ["不安定", "缺乏归属", "人际紧张"],
     "upright_meaning": "值得庆祝的好时刻！享受这份喜悦和周围的温暖。",
     "reversed_meaning": "可能在某个环境中感到不太安定。"},
    {"id": 26, "name_cn": "权杖五", "name_en": "Five of Wands", "img": "w05",
     "upright": ["竞争", "冲突", "挑战"], "reversed": ["避免冲突", "内耗", "妥协"],
     "upright_meaning": "可能会遇到一些竞争或意见分歧，健康的竞争能激发潜力。",
     "reversed_meaning": "为了避免冲突而一味退让，反而造成了内耗。"},
    {"id": 27, "name_cn": "权杖六", "name_en": "Six of Wands", "img": "w06",
     "upright": ["胜利", "认可", "成就"], "reversed": ["自负", "名声受损", "缺乏认可"],
     "upright_meaning": "你的努力得到了认可和赞赏，这是值得骄傲的时刻。",
     "reversed_meaning": "可能期待的认可没有到来，真正的自信来自内心。"},
    {"id": 28, "name_cn": "权杖七", "name_en": "Seven of Wands", "img": "w07",
     "upright": ["坚守", "防御", "捍卫立场"], "reversed": ["力不从心", "退让", "被击败"],
     "upright_meaning": "面对压力和挑战需要坚守自己的立场，勇敢地捍卫你所相信的。",
     "reversed_meaning": "也许已经筋疲力尽了，有时候战略性地后退一步也是明智的。"},
    {"id": 29, "name_cn": "权杖八", "name_en": "Eight of Wands", "img": "w08",
     "upright": ["快速行动", "进展", "消息"], "reversed": ["延迟", "混乱", "方向不明"],
     "upright_meaning": "事情突然加速，信息和机会纷至沓来，顺着势头往前冲。",
     "reversed_meaning": "期待的消息迟迟未到，利用等待的时间做好准备。"},
    {"id": 30, "name_cn": "权杖九", "name_en": "Nine of Wands", "img": "w09",
     "upright": ["坚韧", "毅力", "最后一关"], "reversed": ["精疲力竭", "放弃", "偏执"],
     "upright_meaning": "你已经走过了很长的路，再坚持一下，终点就在前方。",
     "reversed_meaning": "已经到了极限，允许自己休息一下并不丢人。"},
    {"id": 31, "name_cn": "权杖十", "name_en": "Ten of Wands", "img": "w10",
     "upright": ["负担", "责任过重", "压力"], "reversed": ["释放负担", "委派任务", "崩溃"],
     "upright_meaning": "背负了太多的责任和压力，学会分担和取舍很重要。",
     "reversed_meaning": "现在最重要的是减轻自己的负荷。"},
    {"id": 32, "name_cn": "权杖侍从", "name_en": "Page of Wands", "img": "w11",
     "upright": ["探索", "热忱", "好消息"], "reversed": ["三分钟热度", "不切实际", "挫败"],
     "upright_meaning": "一个充满好奇心和冒险精神的时刻，去探索新的可能性。",
     "reversed_meaning": "热情来得快去得也快，试着专注在一件事上。"},
    {"id": 33, "name_cn": "权杖骑士", "name_en": "Knight of Wands", "img": "w12",
     "upright": ["冲劲", "冒险", "充满能量"], "reversed": ["冲动", "鲁莽", "半途而废"],
     "upright_meaning": "充满行动力和冒险精神，带着激情和自信出发。",
     "reversed_meaning": "热情有余但耐心不足，做事容易虎头蛇尾。"},
    {"id": 34, "name_cn": "权杖王后", "name_en": "Queen of Wands", "img": "w13",
     "upright": ["自信", "温暖", "魅力"], "reversed": ["嫉妒", "自私", "控制欲"],
     "upright_meaning": "散发着温暖而自信的光芒，用你独特的方式去影响和创造。",
     "reversed_meaning": "可能因为不安全感而变得控制欲强。"},
    {"id": 35, "name_cn": "权杖国王", "name_en": "King of Wands", "img": "w14",
     "upright": ["领导力", "远见", "企业家精神"], "reversed": ["专横", "不切实际", "急功近利"],
     "upright_meaning": "展现出强大的领导力和远见，用你的魄力和热情带领前进。",
     "reversed_meaning": "领导欲过强反而让周围的人感到压力。"},
]

# 14张圣杯牌
CUPS = [
    {"id": 36, "name_cn": "圣杯一", "name_en": "Ace of Cups", "img": "c01",
     "upright": ["新感情", "爱", "直觉"], "reversed": ["情感封闭", "爱被拒绝", "空虚"],
     "upright_meaning": "一份新的情感正在萌芽，打开心扉去接受爱和温暖。",
     "reversed_meaning": "可能在情感上筑起了高墙，试着允许自己去感受。"},
    {"id": 37, "name_cn": "圣杯二", "name_en": "Two of Cups", "img": "c02",
     "upright": ["伙伴", "连接", "互相吸引"], "reversed": ["关系失衡", "误解", "分离"],
     "upright_meaning": "两颗心之间建立了美好的连接，珍惜这份难得的默契。",
     "reversed_meaning": "一段关系中可能出现了不平衡或误解。"},
    {"id": 38, "name_cn": "圣杯三", "name_en": "Three of Cups", "img": "c03",
     "upright": ["友谊", "聚会", "庆祝"], "reversed": ["社交倦怠", "八卦", "孤立"],
     "upright_meaning": "和朋友们在一起的愉快时光！享受这份陪伴带来的幸福感。",
     "reversed_meaning": "也许需要从频繁的社交中退出来喘口气。"},
    {"id": 39, "name_cn": "圣杯四", "name_en": "Four of Cups", "img": "c04",
     "upright": ["冷漠", "内省", "不满足"], "reversed": ["觉醒", "重新发现", "抓住机会"],
     "upright_meaning": "对眼前的一切感到无聊，但别忽略了身边的好机会。",
     "reversed_meaning": "开始从消极的状态中走出来，重新发现生活中的美好。"},
    {"id": 40, "name_cn": "圣杯五", "name_en": "Five of Cups", "img": "c05",
     "upright": ["失落", "遗憾", "悲伤"], "reversed": ["接受", "走出悲伤", "原谅"],
     "upright_meaning": "为失去的东西感到悲伤，但别忘了回头看看还有没倒的杯子。",
     "reversed_meaning": "正在慢慢从悲伤中走出来，开始接受已经发生的事情。"},
    {"id": 41, "name_cn": "圣杯六", "name_en": "Six of Cups", "img": "c06",
     "upright": ["回忆", "纯真", "故人"], "reversed": ["活在过去", "无法放下", "不成熟"],
     "upright_meaning": "美好的回忆涌上心头，那份纯真的快乐提醒你简单的幸福一直都在。",
     "reversed_meaning": "过于沉浸在过去的回忆中，反而影响了现在的生活。"},
    {"id": 42, "name_cn": "圣杯七", "name_en": "Seven of Cups", "img": "c07",
     "upright": ["幻想", "选择太多", "白日梦"], "reversed": ["回归现实", "聚焦", "做出选择"],
     "upright_meaning": "面前有太多选择和可能性，分清幻想和实际，选一个最靠谱的。",
     "reversed_meaning": "开始从幻想中醒来，看清楚什么是真正值得追求的。"},
    {"id": 43, "name_cn": "圣杯八", "name_en": "Eight of Cups", "img": "c08",
     "upright": ["离开", "寻找更多", "精神追求"], "reversed": ["犹豫不走", "害怕改变", "得过且过"],
     "upright_meaning": "有勇气离开不再满足你的东西，去寻找更深层的意义。",
     "reversed_meaning": "知道应该离开却迈不开步，别永远停在不属于你的地方。"},
    {"id": 44, "name_cn": "圣杯九", "name_en": "Nine of Cups", "img": "c09",
     "upright": ["满足", "愿望成真", "幸福"], "reversed": ["贪婪", "不满足", "愿望受阻"],
     "upright_meaning": "这是一张许愿牌！你内心的愿望很可能正在实现。",
     "reversed_meaning": "也许得到了想要的东西却依然不快乐。"},
    {"id": 45, "name_cn": "圣杯十", "name_en": "Ten of Cups", "img": "c10",
     "upright": ["圆满", "家庭幸福", "和谐"], "reversed": ["家庭矛盾", "关系破裂", "不和谐"],
     "upright_meaning": "情感上达到了一种圆满和谐的状态，好好珍惜。",
     "reversed_meaning": "家庭或亲密关系中可能出现了裂痕。"},
    {"id": 46, "name_cn": "圣杯侍从", "name_en": "Page of Cups", "img": "c11",
     "upright": ["浪漫", "直觉", "好消息"], "reversed": ["情绪化", "不切实际", "幼稚"],
     "upright_meaning": "可能会收到一个温暖的消息或惊喜，保持对美好事物的敏感度。",
     "reversed_meaning": "情绪起伏比较大，在做重要决定之前先让自己冷静下来。"},
    {"id": 47, "name_cn": "圣杯骑士", "name_en": "Knight of Cups", "img": "c12",
     "upright": ["浪漫追求", "邀请", "理想主义"], "reversed": ["不切实际", "情感操控", "虚假承诺"],
     "upright_meaning": "一份充满浪漫和理想色彩的邀请可能正在路上。",
     "reversed_meaning": "当心那些听起来太美好的承诺。"},
    {"id": 48, "name_cn": "圣杯王后", "name_en": "Queen of Cups", "img": "c13",
     "upright": ["共情", "温柔", "直觉力"], "reversed": ["过度敏感", "情绪依赖", "牺牲自我"],
     "upright_meaning": "用温柔和理解去感受他人，但也别忘了关照自己的内心。",
     "reversed_meaning": "可能过于沉浸在他人的情绪中，建立健康的情感边界很重要。"},
    {"id": 49, "name_cn": "圣杯国王", "name_en": "King of Cups", "img": "c14",
     "upright": ["情绪稳定", "智慧", "包容"], "reversed": ["情绪压抑", "冷漠", "情绪爆发"],
     "upright_meaning": "能够在感性和理性之间保持平衡，你的沉稳让身边的人感到安心。",
     "reversed_meaning": "可能一直在压抑自己的真实感受，找到安全的方式释放情绪。"},
]

# 14张宝剑牌
SWORDS = [
    {"id": 50, "name_cn": "宝剑一", "name_en": "Ace of Swords", "img": "s01",
     "upright": ["清晰", "真相", "突破"], "reversed": ["混乱", "误导", "思维受阻"],
     "upright_meaning": "思维变得异常清晰，能看透事物的本质，适合做重要的决定。",
     "reversed_meaning": "脑子里一团乱麻，现在不适合做重大决定。"},
    {"id": 51, "name_cn": "宝剑二", "name_en": "Two of Swords", "img": "s02",
     "upright": ["僵局", "两难", "需要平衡"], "reversed": ["做出选择", "真相浮现", "内心冲突"],
     "upright_meaning": "面对一个左右为难的选择，但蒙上眼睛不看不代表问题不存在。",
     "reversed_meaning": "被压抑的信息开始浮出水面，你不得不面对之前回避的问题。"},
    {"id": 52, "name_cn": "宝剑三", "name_en": "Three of Swords", "img": "s03",
     "upright": ["心痛", "悲伤", "失望"], "reversed": ["疗愈中", "释放痛苦", "原谅"],
     "upright_meaning": "内心正在经历一种深刻的痛苦，不必假装没事，允许自己哭一场。",
     "reversed_meaning": "最痛的时刻正在过去，伤口在慢慢愈合。"},
    {"id": 53, "name_cn": "宝剑四", "name_en": "Four of Swords", "img": "s04",
     "upright": ["休息", "恢复", "静养"], "reversed": ["焦虑", "无法放松", "过度疲劳"],
     "upright_meaning": "身心都需要一个暂停键，安静地休息，让思绪沉淀下来。",
     "reversed_meaning": "明明已经很累了却停不下来，你的身体在发出警告。"},
    {"id": 54, "name_cn": "宝剑五", "name_en": "Five of Swords", "img": "s05",
     "upright": ["争斗", "输赢", "自私"], "reversed": ["和解", "认输", "吸取教训"],
     "upright_meaning": "一场争斗中即使赢了也可能感觉失去了什么，不是每场仗都值得打。",
     "reversed_meaning": "意识到争吵没有赢家，开始愿意放下身段去和解。"},
    {"id": 55, "name_cn": "宝剑六", "name_en": "Six of Swords", "img": "s06",
     "upright": ["过渡", "离开困境", "恢复"], "reversed": ["无法离开", "停滞", "抗拒转变"],
     "upright_meaning": "正在从一个困难的处境中慢慢走出来，最艰难的部分已经过去。",
     "reversed_meaning": "想要离开困境却似乎走不掉，有些东西必须彻底放下。"},
    {"id": 56, "name_cn": "宝剑七", "name_en": "Seven of Swords", "img": "s07",
     "upright": ["策略", "隐瞒", "单打独斗"], "reversed": ["真相大白", "计划败露", "回归正道"],
     "upright_meaning": "用智慧和策略来解决问题更聪明，但秘密和隐瞒的代价有时很大。",
     "reversed_meaning": "之前隐瞒的事情可能要被发现了，诚实是更好的选择。"},
    {"id": 57, "name_cn": "宝剑八", "name_en": "Eight of Swords", "img": "s08",
     "upright": ["困境", "自我限制", "无力感"], "reversed": ["解脱", "看到出路", "新视角"],
     "upright_meaning": "感觉被困住了，但很多束缚其实是自己给自己套上的。",
     "reversed_meaning": "开始意识到困住自己的不是环境而是心态。"},
    {"id": 58, "name_cn": "宝剑九", "name_en": "Nine of Swords", "img": "s09",
     "upright": ["焦虑", "噩梦", "失眠"], "reversed": ["走出焦虑", "面对恐惧", "寻求帮助"],
     "upright_meaning": "深夜的焦虑让人难以入眠，但很多恐惧都比现实中的困难要大得多。",
     "reversed_meaning": "焦虑开始慢慢减轻，你正在学着面对那些恐惧。"},
    {"id": 59, "name_cn": "宝剑十", "name_en": "Ten of Swords", "img": "s10",
     "upright": ["结束", "触底", "最低谷"], "reversed": ["复苏", "拒绝放弃", "最坏已过"],
     "upright_meaning": "已经到了最低谷，接下来只有往上走的方向，黎明就在最深的夜之后。",
     "reversed_meaning": "最痛苦的时刻已经过去，你已经开始重新站起来了。"},
    {"id": 60, "name_cn": "宝剑侍从", "name_en": "Page of Swords", "img": "s11",
     "upright": ["好奇心", "新想法", "观察"], "reversed": ["八卦", "草率", "刻薄"],
     "upright_meaning": "头脑特别活跃，对一切都充满好奇，保持敏锐的观察力。",
     "reversed_meaning": "小心说话太快太尖锐而伤到别人。"},
    {"id": 61, "name_cn": "宝剑骑士", "name_en": "Knight of Swords", "img": "s12",
     "upright": ["果断", "快速行动", "思维敏捷"], "reversed": ["鲁莽", "攻击性", "言辞伤人"],
     "upright_meaning": "思维如闪电般敏捷，看准了方向就立即出击。",
     "reversed_meaning": "行动太快反而出了错，慢下来三思而后行。"},
    {"id": 62, "name_cn": "宝剑王后", "name_en": "Queen of Swords", "img": "s13",
     "upright": ["清醒", "独立", "直率"], "reversed": ["冷酷", "偏见", "过度批判"],
     "upright_meaning": "用清醒的头脑和直率的态度去处理问题，你的独立和理性是最大的优势。",
     "reversed_meaning": "理性过了头就变成了冷酷，适当地让温暖回来。"},
    {"id": 63, "name_cn": "宝剑国王", "name_en": "King of Swords", "img": "s14",
     "upright": ["权威", "清晰思维", "公正"], "reversed": ["滥用权力", "冷漠无情", "思维偏执"],
     "upright_meaning": "拥有清晰的逻辑思维和公正的判断力，用专业和客观的态度去引领方向。",
     "reversed_meaning": "可能过于执着于自己的观点而听不进不同的声音。"},
]

# 14张星币牌
PENTACLES = [
    {"id": 64, "name_cn": "星币一", "name_en": "Ace of Pentacles", "img": "p01",
     "upright": ["新财源", "机会", "物质基础"], "reversed": ["错失机会", "财务不稳", "贪婪"],
     "upright_meaning": "一个与物质和金钱相关的新机会出现了，抓住它打好基础。",
     "reversed_meaning": "一个好的财务机会可能因为犹豫而溜走。"},
    {"id": 65, "name_cn": "星币二", "name_en": "Two of Pentacles", "img": "p02",
     "upright": ["平衡", "适应", "多任务"], "reversed": ["失衡", "应接不暇", "财务混乱"],
     "upright_meaning": "同时在处理多件事情，需要灵活地调配时间和精力。",
     "reversed_meaning": "同时要做的事情太多，已经开始顾不过来了。"},
    {"id": 66, "name_cn": "星币三", "name_en": "Three of Pentacles", "img": "p03",
     "upright": ["团队合作", "技能", "学习"], "reversed": ["配合不佳", "水平不够", "不受重视"],
     "upright_meaning": "通过团队合作和专业技能取得进展，质量比速度更重要。",
     "reversed_meaning": "团队中的配合出了问题，主动沟通比默默抱怨更有效。"},
    {"id": 67, "name_cn": "星币四", "name_en": "Four of Pentacles", "img": "p04",
     "upright": ["守财", "安全感", "保守"], "reversed": ["放手", "过度消费", "财务不安"],
     "upright_meaning": "对现有的东西抓得很紧，但过度执着反而会限制成长。",
     "reversed_meaning": "钱是流动的能量，过度执着反而会堵塞它的流通。"},
    {"id": 68, "name_cn": "星币五", "name_en": "Five of Pentacles", "img": "p05",
     "upright": ["困难", "财务危机", "孤立"], "reversed": ["走出困境", "获得帮助", "转机"],
     "upright_meaning": "正在经历一段物质或精神上的困难时期，帮助其实就在身边。",
     "reversed_meaning": "最困难的时期正在过去，情况都在慢慢好转。"},
    {"id": 69, "name_cn": "星币六", "name_en": "Six of Pentacles", "img": "p06",
     "upright": ["慷慨", "给予", "分享"], "reversed": ["不公平", "施舍感", "自私"],
     "upright_meaning": "适合慷慨地分享你所拥有的，付出终会以某种方式回到你身边。",
     "reversed_meaning": "给予和接受之间出现了不平衡。"},
    {"id": 70, "name_cn": "星币七", "name_en": "Seven of Pentacles", "img": "p07",
     "upright": ["等待收获", "评估", "耐心"], "reversed": ["急于求成", "回报不足", "方向错误"],
     "upright_meaning": "种子已经种下，需要耐心等待它发芽结果。",
     "reversed_meaning": "付出了很多却看不到回报，也许需要重新评估方向。"},
    {"id": 71, "name_cn": "星币八", "name_en": "Eight of Pentacles", "img": "p08",
     "upright": ["勤奋", "精进", "匠心"], "reversed": ["马虎", "厌倦", "缺乏动力"],
     "upright_meaning": "现在是专注打磨技能和精进自我的好时机，量变终会引起质变。",
     "reversed_meaning": "对重复的工作感到厌倦，重新找到工作的意义感。"},
    {"id": 72, "name_cn": "星币九", "name_en": "Nine of Pentacles", "img": "p09",
     "upright": ["丰收", "独立", "品质生活"], "reversed": ["过度挥霍", "缺乏独立", "虚荣"],
     "upright_meaning": "过去的努力开始带来丰厚的回报，享受劳动的成果吧。",
     "reversed_meaning": "真正的富足不只是银行卡里的数字，还有内心的充实。"},
    {"id": 73, "name_cn": "星币十", "name_en": "Ten of Pentacles", "img": "p10",
     "upright": ["财富传承", "家族", "稳定"], "reversed": ["家族矛盾", "遗产纠纷", "短视"],
     "upright_meaning": "物质和精神层面都达到了一种长久稳定的状态，你正在建立持久的价值。",
     "reversed_meaning": "家庭中可能因为金钱问题产生矛盾，把眼光放长远些。"},
    {"id": 74, "name_cn": "星币侍从", "name_en": "Page of Pentacles", "img": "p11",
     "upright": ["学习", "踏实", "新计划"], "reversed": ["懒散", "不务实", "好高骛远"],
     "upright_meaning": "一个务实的新计划或学习机会出现了，一步步把想法变成现实。",
     "reversed_meaning": "想法不少但落地不够，把手弄脏、真正开始做才是最重要的。"},
    {"id": 75, "name_cn": "星币骑士", "name_en": "Knight of Pentacles", "img": "p12",
     "upright": ["稳健", "可靠", "坚持"], "reversed": ["固执", "过于保守", "停滞"],
     "upright_meaning": "用最踏实可靠的方式推进事情，虽然速度不快但走得很实在。",
     "reversed_meaning": "稳健过了头就变成了固执和守旧。"},
    {"id": 76, "name_cn": "星币王后", "name_en": "Queen of Pentacles", "img": "p13",
     "upright": ["持家", "务实", "滋养"], "reversed": ["过度操劳", "忽视自我", "物质执念"],
     "upright_meaning": "能够把工作和生活打理得井井有条，你的务实和温暖让身边的人感到安心。",
     "reversed_meaning": "把所有精力都花在照顾别人上，自己的身心却被忽略了。"},
    {"id": 77, "name_cn": "星币国王", "name_en": "King of Pentacles", "img": "p14",
     "upright": ["财务成功", "稳定", "慷慨"], "reversed": ["贪婪", "物质至上", "过度控制"],
     "upright_meaning": "在物质世界中达到了稳定和成功的状态，你的可靠和慷慨为自己赢得了尊重。",
     "reversed_meaning": "可能过于看重金钱和地位，别让金钱成为唯一的衡量标准。"},
]

# 完整牌组
FULL_DECK = MAJOR_ARCANA + WANDS + CUPS + SWORDS + PENTACLES

IMG_BASE = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards"
HISTORY_FILE = Path("/tmp/tarot_history.json")

# ========== 牌阵配置 ==========
SPREADS = {
    "每日运势": {"count": 3, "positions": ["过去", "现在", "未来"],
                 "desc": "三张牌揭示今日运势走向"},
    "问题指引": {"count": 3, "positions": ["现状", "障碍", "建议"],
                 "desc": "针对具体问题给出指引方向"},
    "单牌指引": {"count": 1, "positions": ["指引"],
                 "desc": "一张牌给出核心启示"},
    "二选一":   {"count": 5, "positions": ["核心", "选择A", "选择B", "A结果", "B结果"],
                 "desc": "帮助在两个选项间看清方向"},
}


def get_image_url(img_code: str) -> str:
    return f"{IMG_BASE}/{img_code}.jpg"


def generate_share_image(cards, spread_type, question, reading_text, date_str, target_name=""):
    """生成分享图片，包含牌面图片和解读摘要"""
    from PIL import Image, ImageDraw, ImageFont
    import requests
    
    # 图片尺寸（适合手机分享）
    WIDTH = 750
    CARD_WIDTH = 180
    CARD_HEIGHT = 310
    PADDING = 30
    
    # 颜色定义
    BG_COLOR = (43, 36, 58)  # 深紫色背景
    TEXT_COLOR = (255, 255, 255)
    GOLD_COLOR = (212, 175, 55)
    LIGHT_PURPLE = (160, 152, 176)
    
    # 计算高度（根据牌数和内容动态调整）
    num_cards = len(cards)
    # 标题区 + 牌面区 + 解读摘要区 + 底部
    HEADER_HEIGHT = 120
    CARD_SECTION_HEIGHT = CARD_HEIGHT + 80  # 牌面 + 牌名
    SUMMARY_HEIGHT = 400  # 解读摘要区
    FOOTER_HEIGHT = 60
    HEIGHT = HEADER_HEIGHT + CARD_SECTION_HEIGHT + SUMMARY_HEIGHT + FOOTER_HEIGHT
    
    # 创建画布
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    def get_font(size, bold=False):
        # Linux (Streamlit Cloud) 常见字体路径
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            # macOS
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
        ]
        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except (IOError, OSError):
                continue
        # 如果都找不到，使用默认字体
        return ImageFont.load_default()
    
    title_font = get_font(36, bold=True)
    subtitle_font = get_font(20)
    card_name_font = get_font(18)
    summary_font = get_font(18)
    footer_font = get_font(14)
    
    # ===== 绘制标题区 =====
    y_offset = PADDING
    
    # 主标题
    title = "🔮 塔罗牌灵感指引"
    draw.text((WIDTH // 2, y_offset), title, fill=GOLD_COLOR, font=title_font, anchor="mt")
    y_offset += 50
    
    # 副标题（日期 + 牌阵类型）
    target_text = f"· 为{target_name}占卜" if target_name else ""
    subtitle = f"📅 {date_str} · {spread_type}{target_text}"
    draw.text((WIDTH // 2, y_offset), subtitle, fill=LIGHT_PURPLE, font=subtitle_font, anchor="mt")
    y_offset += 40
    
    # 问题（如果有）
    if question:
        q_text = f"❓ {question[:30]}{'...' if len(question) > 30 else ''}"
        draw.text((WIDTH // 2, y_offset), q_text, fill=TEXT_COLOR, font=subtitle_font, anchor="mt")
    y_offset = HEADER_HEIGHT
    
    # ===== 绘制牌面区 =====
    # 下载并排列牌面图片
    card_images = []
    for c in cards:
        card = c["card"]
        img_url = get_image_url(card["img"])
        try:
            resp = requests.get(img_url, timeout=10)
            if resp.status_code == 200:
                card_img = Image.open(BytesIO(resp.content))
                # 调整大小
                card_img = card_img.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
                # 如果是逆位，旋转180度
                if c["orientation"] == "逆位":
                    card_img = card_img.rotate(180)
                card_images.append((card_img, c))
        except Exception:
            # 如果下载失败，创建占位符
            placeholder = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (80, 70, 100))
            card_images.append((placeholder, c))
    
    # 计算牌面水平排列位置
    total_card_width = num_cards * CARD_WIDTH + (num_cards - 1) * 15
    start_x = (WIDTH - total_card_width) // 2
    
    for i, (card_img, c) in enumerate(card_images):
        x = start_x + i * (CARD_WIDTH + 15)
        img.paste(card_img, (x, y_offset))
        
        # 牌名
        card_name = f"{c['card']['name_cn']} · {c['orientation']}"
        draw.text((x + CARD_WIDTH // 2, y_offset + CARD_HEIGHT + 10), 
                  card_name, fill=TEXT_COLOR, font=card_name_font, anchor="mt")
    
    y_offset += CARD_SECTION_HEIGHT
    
    # ===== 绘制解读摘要区 =====
    draw.line([(PADDING, y_offset), (WIDTH - PADDING, y_offset)], fill=LIGHT_PURPLE, width=1)
    y_offset += 20
    
    # 提取解读摘要（取前300字符）
    summary = reading_text[:350].replace('\n\n', '\n').strip()
    if len(reading_text) > 350:
        summary += "..."
    
    # 文字换行
    def wrap_text(text, font, max_width):
        lines = []
        for paragraph in text.split('\n'):
            if not paragraph.strip():
                lines.append('')
                continue
            current_line = ''
            for char in paragraph:
                test_line = current_line + char
                bbox = font.getbbox(test_line) if hasattr(font, 'getbbox') else (0, 0, len(test_line) * 10, 20)
                if bbox[2] > max_width:
                    if current_line:
                        lines.append(current_line)
                    current_line = char
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
        return lines
    
    summary_lines = wrap_text(summary, summary_font, WIDTH - 2 * PADDING)
    
    for line in summary_lines[:15]:  # 最多显示15行
        draw.text((PADDING, y_offset), line, fill=TEXT_COLOR, font=summary_font)
        y_offset += 24
    
    # ===== 绘制底部 =====
    y_offset = HEIGHT - FOOTER_HEIGHT + 10
    draw.line([(PADDING, y_offset - 15), (WIDTH - PADDING, y_offset - 15)], fill=LIGHT_PURPLE, width=1)
    footer_text = "✨ 塔罗牌灵感指引 · 聆听内心的声音"
    draw.text((WIDTH // 2, y_offset), footer_text, fill=LIGHT_PURPLE, font=footer_font, anchor="mt")
    
    # 返回图片字节
    buffer = BytesIO()
    img.save(buffer, format='PNG', quality=95)
    buffer.seek(0)
    return buffer
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_all_history(data: dict):
    HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def save_user_draw(nickname: str, date_str: str, cards):
    """保存用户抽牌记录"""
    uid = hashlib.md5(nickname.encode()).hexdigest()[:10]
    all_hist = _load_all_history()
    if uid not in all_hist:
        all_hist[uid] = {}
    all_hist[uid][date_str] = [
        {"name_cn": c["card"]["name_cn"], "orientation": c["orientation"], "position": c["position"]}
        for c in cards
    ]
    # 只保留最近7天
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    all_hist[uid] = {k: v for k, v in all_hist[uid].items() if k >= cutoff}
    _save_all_history(all_hist)


def get_user_history(nickname: str, today: str, days: int = 3) -> list:
    """获取用户前几天的历史"""
    uid = hashlib.md5(nickname.encode()).hexdigest()[:10]
    all_hist = _load_all_history()
    user_hist = all_hist.get(uid, {})
    recent = []
    for i in range(1, days + 1):
        past = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")
        if past in user_hist:
            recent.append({"date": past, "cards": user_hist[past]})
    return recent


def draw_cards(spread_type="每日运势"):
    """根据牌阵类型抽取对应数量的牌"""
    spread = SPREADS[spread_type]
    selected = random.sample(FULL_DECK, spread["count"])

    results = []
    for i, card in enumerate(selected):
        is_upright = random.choice([True, False])
        results.append({
            "card": card,
            "position": spread["positions"][i],
            "is_upright": is_upright,
            "orientation": "正位" if is_upright else "逆位",
            "keywords": card["upright"] if is_upright else card["reversed"],
            "meaning": card["upright_meaning"] if is_upright else card["reversed_meaning"],
        })
    return results


def _render_card(c):
    """渲染单张牌的显示"""
    card = c["card"]
    st.markdown(f"<p style='text-align:center; color:#a098b0;'>{c['position']}</p>", unsafe_allow_html=True)
    img_url = get_image_url(card["img"])
    if c["is_upright"]:
        st.image(img_url, use_container_width=True)
    else:
        st.markdown(f"<img src='{img_url}' style='width:100%; transform:rotate(180deg);'>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#f0d890; font-weight:bold;'>{card['name_cn']}</p>", unsafe_allow_html=True)
    ori_color = "#90e0a0" if c["is_upright"] else "#e0a090"
    st.markdown(f"<p style='text-align:center; color:{ori_color}; font-size:0.9em;'>{'↑ 正位' if c['is_upright'] else '↓ 逆位'}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#b0a8c0; font-size:0.8em;'>{' / '.join(c['keywords'])}</p>", unsafe_allow_html=True)


    st.markdown(f"<p style='text-align:center; color:#b0a8c0; font-size:0.8em;'>{' / '.join(c['keywords'])}</p>", unsafe_allow_html=True)


def _render_followup_item(followup):
    """渲染单条追问历史记录"""
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(240, 216, 144, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    ">
        <h4 style="color:#f0d890; text-align:center;">🔄 第{followup['round']}轮追问</h4>
        <p style="color:#b0a8c0; text-align:center; font-size:0.9em; font-style:italic;">
            "{followup['question']}"
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 居中渲染追问牌
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        card = followup["card"]
        img_url = get_image_url(card["img"])
        if followup["is_upright"]:
            st.image(img_url, use_container_width=True)
        else:
            st.markdown(f"<img src='{img_url}' style='width:100%; transform:rotate(180deg);'>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#f0d890; font-weight:bold;'>{card['name_cn']}</p>", unsafe_allow_html=True)
        ori_color = "#90e0a0" if followup["is_upright"] else "#e0a090"
        st.markdown(f"<p style='text-align:center; color:{ori_color}; font-size:0.9em;'>{'↑ 正位' if followup['is_upright'] else '↓ 逆位'}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#b0a8c0; font-size:0.8em;'>{' / '.join(followup['keywords'])}</p>", unsafe_allow_html=True)

    # 追问解读
    st.markdown(f"<div class='reading-section'>{followup['reading']}</div>", unsafe_allow_html=True)


def _build_followup_prompt(initial_cards, initial_question, initial_reading,
                           spread_type, followup_history, followup_card,
                           followup_question, date_str):
    """构建追问专用prompt，包含累积上下文 + 教练式引导"""

    # 1. 初始牌阵摘要
    initial_cards_desc = []
    for c in initial_cards:
        initial_cards_desc.append(f"{c['card']['name_cn']}（{c['orientation']}）[{c['position']}]")
    initial_cards_text = " | ".join(initial_cards_desc)

    reading_summary = (initial_reading or "")[:200]
    if len(initial_reading or "") > 200:
        reading_summary += "..."

    # 2. 历史追问摘要
    history_section = ""
    if followup_history:
        history_parts = []
        for fh in followup_history:
            rd_summary = (fh["reading"] or "")[:100]
            if len(fh["reading"] or "") > 100:
                rd_summary += "..."
            history_parts.append(
                f"第{fh['round']}轮追问：\n"
                f"  问题：{fh['question']}\n"
                f"  牌：{fh['card']['name_cn']}（{fh['orientation']}）\n"
                f"  解读要点：{rd_summary}"
            )
        history_section = "\n\n".join(history_parts)

    # 3. 当前追问牌面
    card = followup_card["card"]
    current_round = len(followup_history) + 1
    question_display = followup_question if followup_question else "用户未提出具体问题，只是想再抽一张指引牌"

    return f"""你是一位温暖、富有人文关怀的塔罗师，擅长用教练式提问帮助人们找到内心的答案。
你精通心理学中的自我觉察、内在动机、情绪识别等方法，善于通过开放性问题引导人们深入思考。

【初始占卜信息】
日期：{date_str}
牌阵：{spread_type}
初始问题："{initial_question}"
初始牌面：{initial_cards_text}
初始解读摘要：{reading_summary}

{"【历史追问记录】" + chr(10) + history_section if history_section else ""}

【本轮追问 · 第{current_round}轮】
用户追问："{question_display}"
追问牌：{card['name_cn']} - {followup_card['orientation']}
  关键词：{' / '.join(followup_card['keywords'])}
  基础含义：{followup_card['meaning']}

---

请用温暖、富有启发性的口吻生成约400-600字的追问解读，包含以下内容：

- 【追问牌解读：{card['name_cn']}（{followup_card['orientation']}）】（120-150字）
  深入解读这张牌在当前累积语境下的含义，它为之前的占卜补充了什么新视角
  要结合用户的追问内容进行针对性分析

- 【故事的延续】（100-120字）
  分析这张追问牌与初始牌阵{"及前几轮追问" if followup_history else ""}的呼应关系
  它们共同讲述了一个怎样的事件发展脉络？能量在如何流动和变化？

- 【想和你聊聊】（100-150字）
  针对这次的追问和牌面信息，提出3-5个开放性问题，帮助深入思考：
  这些问题要真诚有力，不是形式化的修辞，要能触动内心
  例如：这张牌让你联想到生活中的哪个具体画面？你内心最真实的期待是什么？如果抛开外界评判，你的直觉告诉你什么？

- 【温柔提醒】（60-80字）
  如果发现用户有以下倾向，温和地点出供其自行判断：
  • 反复纠结同一问题 → 也许现在需要的不是更多答案，而是迈出行动的勇气
  • 期待外界拯救 → 温和指出力量一直在自己手中
  • 过度焦虑未来 → 引导关注当下能做的小事
  如果没有这些倾向，则给出一句温暖的鼓励

【语气要求】
- 温暖积极为主，像一个懂你的朋友在聊天
- 不说教，不用"你应该"，用"不妨试试""也许可以"
- 语言自然，避免AI套话
- 坦诚但温柔：对风险和问题不回避，但用理解和支持的方式表达"""


def _call_ai_followup_reading(initial_cards, initial_question, initial_reading,
                              spread_type, followup_history, followup_card,
                              followup_question, api_key):
    """调用通义千问生成追问解读"""
    import requests

    date_str = datetime.now().strftime("%Y-%m-%d")
    prompt = _build_followup_prompt(
        initial_cards=initial_cards,
        initial_question=initial_question,
        initial_reading=initial_reading,
        spread_type=spread_type,
        followup_history=followup_history,
        followup_card=followup_card,
        followup_question=followup_question,
        date_str=date_str,
    )

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
                "max_tokens": 2000,
                "temperature": 0.85,
            },
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return None
    except Exception:
        return None


def _handle_followup_draw(followup_question):
    """处理追问抽牌：抽牌 → 调用AI → 存入session_state"""
    selected = random.sample(FULL_DECK, 1)[0]
    is_upright = random.choice([True, False])

    followup_card = {
        "card": selected,
        "is_upright": is_upright,
        "orientation": "正位" if is_upright else "逆位",
        "keywords": selected["upright"] if is_upright else selected["reversed"],
        "meaning": selected["upright_meaning"] if is_upright else selected["reversed_meaning"],
    }

    api_key = os.environ.get("TONGYI_API_KEY") or st.secrets.get("TONGYI_API_KEY", "")

    followup_reading = None
    if api_key:
        followup_reading = _call_ai_followup_reading(
            initial_cards=st.session_state.cards,
            initial_question=st.session_state.get("question", ""),
            initial_reading=st.session_state.get("reading", ""),
            spread_type=st.session_state.get("spread_type", ""),
            followup_history=st.session_state.get("followup_history", []),
            followup_card=followup_card,
            followup_question=followup_question,
            api_key=api_key,
        )

    if not followup_reading:
        followup_reading = f"💡 **AI解读暂时无法生成，以下是牌面的基础含义：**\n\n{followup_card['meaning']}\n\n你可以结合前面的占卜结果，感受这张牌想告诉你什么。"

    followup_count = st.session_state.get("followup_count", 0)
    record = {
        "round": followup_count + 1,
        "question": followup_question if followup_question else "（未输入具体问题）",
        "card": selected,
        "is_upright": is_upright,
        "orientation": followup_card["orientation"],
        "keywords": followup_card["keywords"],
        "meaning": followup_card["meaning"],
        "reading": followup_reading,
    }

    if "followup_history" not in st.session_state:
        st.session_state.followup_history = []
    st.session_state.followup_history.append(record)
    st.session_state.followup_count = followup_count + 1


def _build_prompt(cards, cards_text, date_str, spread_type, question, history, target_name=""):
    """根据牌阵类型构建不同的 AI prompt
    
    Args:
        target_name: 如果不为空，表示是"为TA占卜"模式，需要把"你"改成这个名字/称呼
    """
    
    # 根据是否为TA占卜调整称呼
    subject = target_name if target_name else "你"
    subject_de = f"{target_name}的" if target_name else "你的"
    is_for_other = bool(target_name)
    
    # 为TA占卜时的额外提示
    for_other_note = ""
    if is_for_other:
        for_other_note = f"""
【重要】这次占卜是帮「{target_name}」进行的，请在整个解读中：
- 用「{target_name}」或「TA」代替「你」
- 语气像是在向占卜师描述这位朋友/客户的情况
- 例如：「{target_name}最近可能...」「TA需要注意的是...」「对{target_name}来说...」
"""

    if spread_type == "每日运势":
        history_section = ""
        if history:
            history_lines = []
            for day in history:
                card_strs = [f"{c['name_cn']}（{c['orientation']}）[{c['position']}]" for c in day["cards"]]
                history_lines.append(f"  {day['date']}：{' | '.join(card_strs)}")
            history_text = "\n".join(history_lines)
            history_section = f"""

【近期抽牌历史】
{history_text}

请在解读中额外增加一个段落：
- 【运势流动】（100-150字）
  结合近几天的牌面变化趋势，分析运势的整体走向
  指出能量的转变方向（如：从低谷走向恢复、从迷茫到清晰等）
  给出顺应趋势的建议"""

        return f"""你是一位温暖、富有人文关怀的塔罗师。
{for_other_note}
今天是 {date_str}，有人抽取了每日塔罗牌：

{cards_text}
{history_section}

请用温暖的口吻生成约800-1000字的解读（有历史记录时约900-1100字），包含以下内容：

- 【第一张牌解读：{cards[0]['card']['name_cn']}（{cards[0]['orientation']}）】（80-100字）
  针对"过去"位置，解读这张牌在当前语境下的具体含义

- 【第二张牌解读：{cards[1]['card']['name_cn']}（{cards[1]['orientation']}）】（80-100字）
  针对"现在"位置，解读这张牌在当前语境下的具体含义

- 【第三张牌解读：{cards[2]['card']['name_cn']}（{cards[2]['orientation']}）】（80-100字）
  针对"未来"位置，解读这张牌在当前语境下的具体含义

- 【今日整体运势】（100-150字）
  综合三张牌的组合，用"过去-现在-未来"串联整体能量走向

- 【事业与财运】（80-120字）
  具体指引和可落地的行动建议

- 【情感与人际】（80-120字）
  关系和沟通提醒

- 【今日能量总结】（60-80字）
  用一句话概括今天的核心能量主题，以及最适合做什么、最不适合做什么

- 【风险提示】（60-80字）
  基于牌面组合，指出今天需要特别注意和回避的事项
  如果牌面暗示不确定性或变化，自然引入"未雨绸缪"的思考角度

- 【关爱身边人】（50-70字）
  今天的能量对你身边重要的人（家人、伴侣、孩子）可能有什么影响？
  你可以为他们做点什么小事？

- 【本周可以做的一件小事】（40-60字）
  基于今日牌面能量，给出一个具体、可执行的小行动
  例如：给某人发条消息、整理某个物品、完成某个搁置的小任务

- 【今日温馨提示】（40-60字）
  一句温暖的鼓励

- 【留给自己的问题】（30-50字）
  在解读最后，留一个启发性的问题让用户带着思考
  例如："如果今天的你可以给三年后的自己一个承诺，那会是什么？"

要求：语言自然，像朋友聊天，避免AI套话，不要说"首先其次最后"。

【语气与方法要求】
1. 温暖积极为主基调，相信用户有力量面对一切
2. 融入教练问话技术：多用启发性问题代替直接建议，例如"不妨问问自己，如果抛开顾虑，你最想尝试什么？"
3. 运用心理学视角：融入自我觉察、内在动机、情绪识别等概念
4. 对于不合理的期待或逃避倾向，温和地点出供用户自行判断，例如"这张牌提醒我们，也许现在是个好时机去审视一下..."
5. 不要说教，不要用"你应该"，而是引导用户自己发现答案
6. 【关爱身边人】要自然不刻意，从牌面能量出发，不要有推销感"""

    elif spread_type == "问题指引":
        return f"""你是一位温暖、富有人文关怀的塔罗师。
{for_other_note}
今天是 {date_str}，有人就以下问题进行了塔罗占卜：

问题：{question}

牌阵：问题指引（现状 - 障碍 - 建议）

{cards_text}

请用温暖的口吻生成约700-900字的解读，包含以下内容：

- 【现状解读：{cards[0]['card']['name_cn']}（{cards[0]['orientation']}）】（80-120字）
  针对"现状"位置，解读这张牌反映出当前问题所处的状态和能量

- 【障碍解读：{cards[1]['card']['name_cn']}（{cards[1]['orientation']}）】（80-120字）
  针对"障碍"位置，解读目前面临的主要阻碍和需要克服的挑战

- 【建议解读：{cards[2]['card']['name_cn']}（{cards[2]['orientation']}）】（80-120字）
  针对"建议"位置，解读塔罗给出的行动方向和指引

- 【综合分析】（120-160字）
  结合三张牌和问题本身，给出整体分析和具体可操作的行动建议
  如果问题涉及风险或不确定性，自然引入"提前准备"的思考角度

- 【这件事对身边人的影响】（60-80字）
  你正在思考的这个问题，可能会如何影响你身边重要的人？
  他们会希望你怎么做？

- 【本周可以做的一件小事】（50-70字）
  基于牌面建议，给出一个具体、可执行的小行动
  这个行动应该是低门槛、可在一周内完成的

- 【核心提醒】（60-80字）
  一句话总结这个问题的关键能量，给出最重要的行动指引

- 【留给自己的问题】（30-50字）
  在解读最后，留一个启发性的深层问题让用户继续思考
  例如："如果这个问题5年后回头看，你会希望当时的自己怎么选？"

要求：紧扣问题"{question}"进行解读，语言自然，像朋友聊天，避免AI套话。

【语气与方法要求】
1. 温暖积极为主基调，相信用户有力量面对一切
2. 融入教练问话技术：多用启发性问题代替直接建议，例如"不妨问问自己，如果抛开顾虑，你最想尝试什么？"
3. 运用心理学视角：融入自我觉察、内在动机、情绪识别等概念
4. 对于不合理的期待或逃避倾向，温和地点出供用户自行判断
5. 不要说教，不要用"你应该"，而是引导用户自己发现答案
6. 【这件事对身边人的影响】要从关怀角度出发，不要有说教感"""

    elif spread_type == "单牌指引":
        return f"""你是一位温暖、富有人文关怀的塔罗师。
{for_other_note}
今天是 {date_str}，有人抽取了一张塔罗牌寻求指引：

问题：{question}

{cards_text}

请用温暖的口吻生成约350-450字的解读，包含以下内容：

- 【牌面解读：{cards[0]['card']['name_cn']}（{cards[0]['orientation']}）】（100-130字）
  深入解读这张牌在问题语境下的含义，它想告诉你什么

- 【行动指引】（80-100字）
  基于牌面给出具体、可落地的建议
  如果牌面暗示变化或不确定性，可以提及"为可能的变化做些小准备"

- 【今天可以做的一件小事】（40-60字）
  一个具体、简单、马上可以执行的小行动

- 【一句话点睛】（30-50字）
  一句温暖有力的总结

- 【延伸思考】（30-50字）
  留一个启发性问题，让用户带走继续思考
  例如："如果这张牌想提醒你注意身边的某个人，那会是谁？"

要求：紧扣问题"{question}"进行解读，语言自然，像朋友聊天，避免AI套话。

【语气与方法要求】
1. 温暖积极为主基调，相信用户有力量面对一切
2. 融入教练问话技术：多用启发性问题代替直接建议
3. 运用心理学视角：融入自我觉察、内在动机等概念
4. 对于不合理的期待或逃避倾向，温和地点出供用户自行判断
5. 不要说教，不要用"你应该"，而是引导用户自己发现答案
6. 【延伸思考】的问题要有趣、有深度，能引发继续对话的欲望"""

    elif spread_type == "二选一":
        return f"""你是一位温暖、富有人文关怀的塔罗师。
{for_other_note}
今天是 {date_str}，有人面临选择，进行了二选一塔罗占卜：

问题：{question}

牌阵：二选一（核心 - 选择A - 选择B - A结果 - B结果）

{cards_text}

请用温暖的口吻生成约800-1000字的解读，包含以下内容：

- 【核心能量：{cards[0]['card']['name_cn']}（{cards[0]['orientation']}）】（80-100字）
  解读你在这个选择中的核心状态和真实需求

- 【选择A解读：{cards[1]['card']['name_cn']}（{cards[1]['orientation']}）】（80-100字）
  解读选择A代表的能量和特质

- 【选择B解读：{cards[2]['card']['name_cn']}（{cards[2]['orientation']}）】（80-100字）
  解读选择B代表的能量和特质

- 【A的可能走向：{cards[3]['card']['name_cn']}（{cards[3]['orientation']}）】（80-100字）
  如果选择A，可能带来的发展和结果

- 【B的可能走向：{cards[4]['card']['name_cn']}（{cards[4]['orientation']}）】（80-100字）
  如果选择B，可能带来的发展和结果

- 【综合建议】（100-150字）
  综合五张牌的能量对比，客观分析各自的优劣势，帮助看清两条路的不同走向
  如果选择涉及风险或长期影响，可以提及"无论选哪条路，都要为不确定性留出空间"

- 【你的选择会影响谁？】（60-80字）
  这个决定不仅关乎你自己，还可能影响哪些人？
  他们会希望你怎么选？他们的期待是否也是你内心的声音？

- 【做决定前可以做的一件事】（50-70字）
  在真正做出选择之前，一个能帮你更清晰的小行动
  例如：和某个信任的人聊聊、写下两个选择的优缺点、给自己一天时间静心

- 【留给自己的问题】（40-60字）
  一个深层的启发性问题，帮助用户触及选择背后的真实渴望
  例如："如果两个选择都不会失败，你的心会先走向哪一边？"

要求：紧扣问题"{question}"进行解读。不要直接告诉选A还是选B，而是分析各自的能量走向，尊重问卜者的自由意志。语言自然，像朋友聊天，避免AI套话。

【语气与方法要求】
1. 温暖积极为主基调，相信用户有力量面对一切
2. 融入教练问话技术：多用启发性问题代替直接建议，例如"如果两个选择都不会失败，你的心会先走向哪一边？"
3. 运用心理学视角：融入自我觉察、内在动机、价值观澄清等概念
4. 对于不合理的期待或逃避倾向，温和地点出供用户自行判断
5. 不要说教，不要用"你应该"，而是引导用户自己发现答案
6. 【你的选择会影响谁？】要从关爱视角出发，帮助用户看到选择的涟漪效应"""

    return ""


def call_ai_reading(cards, date_str, api_key, spread_type="每日运势", question="", history=None, target_name=""):
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

    prompt = _build_prompt(cards, cards_text, date_str, spread_type, question, history, target_name)

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
                "max_tokens": 2000,
                "temperature": 0.85,
            },
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return None
    except Exception:
        return None


# ========== 主界面 ==========
st.markdown("<h1 style='text-align:center;'>🔮 塔罗牌灵感指引</h1>", unsafe_allow_html=True)

today = datetime.now().strftime("%Y-%m-%d")
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
st.markdown(f"<p style='text-align:center; color:#a098b0;'>📅 {today} {weekday}</p>", unsafe_allow_html=True)

# 昵称输入（用于关联历史记录）
nickname = st.text_input("输入你的昵称（可追踪运势变化）", placeholder="例如：小明", key="nickname_input")

# 占卜对象选择
divination_mode = st.radio(
    "占卜对象",
    ["为自己占卜", "为TA占卜"],
    horizontal=True,
    key="divination_mode",
    help="选择「为TA占卜」可以帮朋友/客户抽牌解读"
)

# 如果是为TA占卜，显示对方昵称输入
target_name = ""
if divination_mode == "为TA占卜":
    target_name = st.text_input(
        "TA的称呼",
        placeholder="例如：王姐、朋友",
        key="target_name_input"
    )

# 牌阵选择
spread_names = list(SPREADS.keys())
spread_type = st.selectbox(
    "选择牌阵",
    spread_names,
    format_func=lambda x: f"{x} — {SPREADS[x]['desc']}",
    key="spread_select",
)

# 问题输入（非每日运势时显示）
question = ""
if spread_type != "每日运势":
    if spread_type == "二选一":
        question = st.text_input(
            "请描述你面临的选择",
            placeholder="例如：应该换工作还是留在现在的公司？",
            key="question_input",
        )
    else:
        question = st.text_input(
            "请输入你想测算的问题",
            placeholder="例如：近期的感情发展如何？",
            key="question_input",
        )

# 抽牌按钮
button_labels = {
    "每日运势": "✨ 抽取今日运势",
    "问题指引": "🔍 抽取问题指引",
    "单牌指引": "🃏 抽取一张牌",
    "二选一": "⚖️ 抽取二选一牌阵",
}
if st.button(button_labels.get(spread_type, "✨ 开始占卜"), use_container_width=True):
    if spread_type != "每日运势" and not question.strip():
        st.warning("请先输入你想测算的问题")
    elif divination_mode == "为TA占卜" and not target_name.strip():
        st.warning("请输入TA的称呼")
    else:
        st.session_state.cards = draw_cards(spread_type)
        st.session_state.reading = None
        st.session_state.draw_id = str(uuid.uuid4())
        st.session_state.spread_type = spread_type
        st.session_state.question = question.strip()
        st.session_state.current_divination_mode = divination_mode
        st.session_state.target_name = target_name.strip() if divination_mode == "为TA占卜" else ""
        # 初始化追问状态（非每日运势模式）
        if spread_type != "每日运势":
            st.session_state.followup_count = 0
            st.session_state.followup_history = []
        if nickname.strip():
            save_user_draw(nickname.strip(), today, st.session_state.cards)

# 显示牌面
if "cards" in st.session_state and st.session_state.cards:
    cards = st.session_state.cards
    current_spread = st.session_state.get("spread_type", "每日运势")
    current_question = st.session_state.get("question", "")

    st.markdown("---")

    # 牌阵标题
    spread_title = current_spread
    if current_question:
        spread_title += f" · {current_question}"
    st.markdown(f"<h3 style='text-align:center;'>{spread_title}</h3>", unsafe_allow_html=True)

    # 根据牌数调整布局
    num_cards = len(cards)

    if num_cards == 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            _render_card(cards[0])

    elif num_cards == 3:
        cols = st.columns(3)
        for i, c in enumerate(cards):
            with cols[i]:
                _render_card(c)

    elif num_cards == 5:
        # 二选一：核心居中 + 两组对比
        st.markdown("<p style='text-align:center;color:#8880a0;font-size:0.85em;'>— 核心 —</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            _render_card(cards[0])

        st.markdown("<p style='text-align:center;color:#8880a0;font-size:0.85em;'>— 两个选择 —</p>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            _render_card(cards[1])
        with col_b:
            _render_card(cards[2])

        st.markdown("<p style='text-align:center;color:#8880a0;font-size:0.85em;'>— 选择结果 —</p>", unsafe_allow_html=True)
        col_ra, col_rb = st.columns(2)
        with col_ra:
            _render_card(cards[3])
        with col_rb:
            _render_card(cards[4])

    # AI解读
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>✨ 灵感解读</h3>", unsafe_allow_html=True)

    api_key = os.environ.get("TONGYI_API_KEY") or st.secrets.get("TONGYI_API_KEY", "")

    # 历史记录仅用于每日运势
    history = []
    if current_spread == "每日运势" and nickname.strip():
        history = get_user_history(nickname.strip(), today, days=3)

    if api_key:
        if st.session_state.get("reading") is None:
            current_target = st.session_state.get("target_name", "")
            spinner_text = f"正在为{current_target}解读..." if current_target else "正在为你解读..."
            with st.spinner(spinner_text):
                reading = call_ai_reading(
                    cards, today, api_key,
                    spread_type=current_spread,
                    question=current_question,
                    history=history,
                    target_name=current_target,
                )
                st.session_state.reading = reading if reading else "fallback"

        if st.session_state.reading and st.session_state.reading != "fallback":
            st.markdown(f"<div class='reading-section'>{st.session_state.reading}</div>", unsafe_allow_html=True)
            
            # 分享功能
            st.markdown("---")
            target_name_display = st.session_state.get("target_name", "")
            
            col_share1, col_share2 = st.columns(2)
            with col_share1:
                # 生成分享图片按钮
                if st.button("🖼️ 生成分享图片", use_container_width=True, key="gen_share_image"):
                    with st.spinner("正在生成分享图片..."):
                        try:
                            share_img = generate_share_image(
                                cards=cards,
                                spread_type=current_spread,
                                question=current_question,
                                reading_text=st.session_state.reading,
                                date_str=today,
                                target_name=target_name_display
                            )
                            st.session_state.share_image = share_img
                            st.success("图片生成成功！点击下方按钮保存")
                        except Exception as e:
                            st.error(f"图片生成失败：{str(e)}")
            
            with col_share2:
                # 复制文本按钮（备用）
                if st.button("📋 复制文字版", use_container_width=True, key="copy_reading"):
                    card_names = " | ".join([f"{c['card']['name_cn']}（{c['orientation']}）" for c in cards])
                    share_text = f"""🔮 塔罗牌灵感指引
📅 {today}
🃏 {current_spread}
{f"❓ {current_question}" if current_question else ""}

【牌面】{card_names}

{st.session_state.reading}

---
✨ 来自塔罗牌灵感指引"""
                    st.session_state.share_text = share_text
                    st.session_state.share_image = None  # 清除图片状态
                    st.success("已生成，请在下方复制")
            
            # 显示生成的分享图片
            if st.session_state.get("share_image"):
                st.image(st.session_state.share_image, caption="长按保存图片，或点击下方按钮下载", use_container_width=True)
                # 下载按钮
                st.download_button(
                    label="📥 下载分享图片",
                    data=st.session_state.share_image,
                    file_name=f"tarot_{today}_{current_spread}.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            # 显示文字版（如果选择了复制文字）
            elif st.session_state.get("share_text"):
                st.text_area("分享文本（长按复制）", st.session_state.share_text, height=200, key="share_textarea")
        else:
            for c in cards:
                st.markdown(f"**【{c['position']} - {c['card']['name_cn']}（{c['orientation']}）】**")
                st.write(c["meaning"])
    else:
        for c in cards:
            st.markdown(f"**【{c['position']} - {c['card']['name_cn']}（{c['orientation']}）】**")
            st.write(c["meaning"])

    # 历史记录展示（仅每日运势模式）
    if history:
        st.markdown("---")
        st.markdown("<h3 style='text-align:center;'>📜 近期牌面记录</h3>", unsafe_allow_html=True)
        for day in history:
            card_tags = ""
            for c in day["cards"]:
                color = "#90e0a0" if c["orientation"] == "正位" else "#e0a090"
                mark = "↑" if c["orientation"] == "正位" else "↓"
                card_tags += f'<span style="display:inline-block;padding:3px 10px;margin:2px;border-radius:6px;font-size:0.8em;background:rgba(255,255,255,0.06);color:{color};border:1px solid {color}30;">{c["name_cn"]} {mark}</span>'
            st.markdown(f"<p style='color:#8880a0;margin-bottom:4px;'>{day['date']}</p>{card_tags}", unsafe_allow_html=True)

    # ========== 追问系统 ==========
    if current_spread != "每日运势" and st.session_state.get("reading") and st.session_state.reading != "fallback":
        st.markdown("---")

        followup_count = st.session_state.get("followup_count", 0)
        followup_max = 3
        remaining = followup_max - followup_count

        st.markdown(
            f"<h3 style='text-align:center;'>💬 深度追问 (剩余 {remaining}/{followup_max} 次)</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;color:#8880a0;font-size:0.85em;'>"
            "塔罗帮你找到内心的声音，追问解读会引导你深入思考"
            "</p>",
            unsafe_allow_html=True,
        )

        # 按时间正序显示追问历史
        followup_history = st.session_state.get("followup_history", [])
        for followup in followup_history:
            _render_followup_item(followup)

        # 追问输入区
        if remaining > 0:
            followup_question = st.text_input(
                "追问内容（选填，可留空）",
                placeholder="例如：如果选择A，感情方面会怎样发展？",
                key=f"followup_q_{followup_count}",
            )

            if st.button("🔮 抽取追问牌", key=f"followup_btn_{followup_count}", use_container_width=True):
                with st.spinner("正在为你解读追问..."):
                    _handle_followup_draw(followup_question.strip())
                st.rerun()
        else:
            st.markdown(
                "<div class='blessing'>✨ 已用完所有追问机会，愿你找到内心的答案 ✨</div>",
                unsafe_allow_html=True,
            )

    # 祝福语
    st.markdown("<div class='blessing'>✨ 愿灵感照亮你的方向 ✨</div>", unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("<p style='text-align:center; color:#605878; font-size:0.8em;'>Rider-Waite Tarot · 78张完整牌组 · 多牌阵</p>", unsafe_allow_html=True)
