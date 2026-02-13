"""
塔罗牌完整数据 - 78张牌（22大阿卡纳 + 56小阿卡纳）
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TarotCard:
    id: int
    name_cn: str
    name_en: str
    category: str  # "大阿卡纳" / "小阿卡纳"
    suit: Optional[str]  # 花色（仅小阿卡纳）
    upright_keywords: List[str]
    upright_meaning: str
    reversed_keywords: List[str]
    reversed_meaning: str
    symbol: str  # emoji符号


# ═══════════════════════════════════════════
# 22张大阿卡纳
# ═══════════════════════════════════════════

MAJOR_ARCANA = [
    TarotCard(
        id=0, name_cn="愚者", name_en="The Fool", category="大阿卡纳", suit=None,
        upright_keywords=["新开始", "冒险", "纯真", "信任", "自由"],
        upright_meaning="一段全新旅程即将开始，怀着纯真的心去探索未知。虽然前方看不清，但内心有股天真的勇气在支撑。现在是行动的时刻，不是犹豫的时候。",
        reversed_keywords=["鲁莽", "逃避", "不成熟", "盲目冒进"],
        reversed_meaning="可能在没有充分准备的情况下冲动行事，或因恐惧而不敢迈出第一步。需要在勇气和理性之间找到平衡，重新审视计划是否可行。",
        symbol="🃏"
    ),
    TarotCard(
        id=1, name_cn="魔术师", name_en="The Magician", category="大阿卡纳", suit=None,
        upright_keywords=["创造力", "技能", "意志力", "自信", "行动"],
        upright_meaning="你拥有实现目标所需的一切资源和能力。现在是将想法变为现实的好时机，相信自己的技能，专注且果断地行动起来。",
        reversed_keywords=["欺骗", "操控", "才能浪费", "缺乏方向"],
        reversed_meaning="可能在浪费天赋或迷失方向，也要警惕周围是否有人在刻意误导你。重新聚焦目标，把精力放在真正重要的事情上。",
        symbol="🎩"
    ),
    TarotCard(
        id=2, name_cn="女祭司", name_en="The High Priestess", category="大阿卡纳", suit=None,
        upright_keywords=["直觉", "潜意识", "内在智慧", "神秘", "耐心"],
        upright_meaning="此刻需要倾听内心的声音，答案就藏在你的直觉里。不必急于行动，安静下来，感受潜意识传递的信息，时机未到时等待也是一种力量。",
        reversed_keywords=["忽视直觉", "表面化", "信息隐瞒", "过度理性"],
        reversed_meaning="你可能过于依赖逻辑而忽略了内心的感受，或者有些重要信息尚未浮出水面。试着放下头脑的执念，重新连接自己的直觉。",
        symbol="🌙"
    ),
    TarotCard(
        id=3, name_cn="皇后", name_en="The Empress", category="大阿卡纳", suit=None,
        upright_keywords=["丰盛", "滋养", "创造", "美感", "母性"],
        upright_meaning="生活中充满丰盛和温柔的能量，适合去创造、去感受美好。无论是人际关系还是项目计划，都在一个生长和繁荣的阶段。",
        reversed_keywords=["过度依赖", "创造力受阻", "忽视自我", "匮乏感"],
        reversed_meaning="可能过度照顾他人而忽略了自己的需求，或者对生活产生了匮乏感。记得先填满自己的杯子，才能有余力去滋养他人。",
        symbol="👑"
    ),
    TarotCard(
        id=4, name_cn="皇帝", name_en="The Emperor", category="大阿卡纳", suit=None,
        upright_keywords=["权威", "结构", "稳定", "纪律", "领导力"],
        upright_meaning="现在需要用理性和纪律来构建秩序。无论是工作还是生活，建立清晰的框架和规则会帮助你掌控局面，稳步前行。",
        reversed_keywords=["专制", "僵化", "控制欲", "缺乏弹性"],
        reversed_meaning="可能过于执着于控制一切，反而失去了灵活性。试着放松一些，不是所有事情都需要按照你的计划来，适度的妥协也是智慧。",
        symbol="⚜️"
    ),
    TarotCard(
        id=5, name_cn="教皇", name_en="The Hierophant", category="大阿卡纳", suit=None,
        upright_keywords=["传统", "指引", "信仰", "教育", "精神导师"],
        upright_meaning="适合向有经验的人请教或学习。遵循成熟的方法论和传统智慧，会比自己摸索更高效。也是一个适合深入学习和精神成长的时期。",
        reversed_keywords=["打破常规", "挑战权威", "自由思考", "非传统"],
        reversed_meaning="你可能对既定规则感到不满，想要走出一条自己的路。这种叛逆不一定是坏事，但要确保自己是在有思考的基础上做选择。",
        symbol="📿"
    ),
    TarotCard(
        id=6, name_cn="恋人", name_en="The Lovers", category="大阿卡纳", suit=None,
        upright_keywords=["爱情", "选择", "和谐", "价值观", "连接"],
        upright_meaning="面临重要的选择，需要跟随内心的价值观做决定。人际关系中充满和谐与深层连接的能量，真诚的沟通能带来意想不到的美好。",
        reversed_keywords=["价值观冲突", "关系不和", "犹豫不决", "错误选择"],
        reversed_meaning="可能在某个选择上左右为难，或者和身边的人存在价值观上的分歧。不要回避矛盾，正视内心真正的需求才能找到答案。",
        symbol="💕"
    ),
    TarotCard(
        id=7, name_cn="战车", name_en="The Chariot", category="大阿卡纳", suit=None,
        upright_keywords=["胜利", "意志力", "决心", "克服障碍", "前进"],
        upright_meaning="凭借坚定的意志力和决心，你能克服眼前的困难。现在是全力以赴的时候，保持专注，不要被干扰分散注意力，胜利就在前方。",
        reversed_keywords=["失控", "方向迷失", "挫败", "攻击性"],
        reversed_meaning="感觉事情脱离了掌控，或者在前进的路上遇到了阻碍。也许需要重新调整策略，蛮力不一定是解决问题的最好方式。",
        symbol="🏇"
    ),
    TarotCard(
        id=8, name_cn="力量", name_en="Strength", category="大阿卡纳", suit=None,
        upright_keywords=["内在力量", "勇气", "耐心", "温柔", "自律"],
        upright_meaning="真正的力量不是来自外在的强硬，而是内心的温柔与坚韧。用耐心和包容去面对挑战，以柔克刚往往比硬碰硬更有效。",
        reversed_keywords=["自我怀疑", "脆弱", "缺乏自信", "内心挣扎"],
        reversed_meaning="可能正在经历自我怀疑或内心的挣扎。不必苛责自己，允许脆弱的存在，休息之后重新找回内在的平衡和勇气。",
        symbol="🦁"
    ),
    TarotCard(
        id=9, name_cn="隐士", name_en="The Hermit", category="大阿卡纳", suit=None,
        upright_keywords=["内省", "独处", "寻找真相", "智慧", "指引"],
        upright_meaning="现在适合暂时从喧嚣中抽身，给自己一些独处和思考的时间。向内探索会带来深刻的领悟，安静中往往能找到最清晰的方向。",
        reversed_keywords=["孤僻", "逃避社交", "过度封闭", "迷失方向"],
        reversed_meaning="独处太久可能变成了逃避。如果感觉越来越封闭，是时候走出来和外界重新建立连接了，别让孤独变成一种习惯。",
        symbol="🕯️"
    ),
    TarotCard(
        id=10, name_cn="命运之轮", name_en="Wheel of Fortune", category="大阿卡纳", suit=None,
        upright_keywords=["转折", "好运", "命运", "周期", "机遇"],
        upright_meaning="命运的齿轮正在转动，变化即将到来。这是一个充满机遇的转折点，顺势而为比逆流而上更聪明。好运正在靠近，保持开放的心态。",
        reversed_keywords=["厄运", "抗拒变化", "失控", "坏运气"],
        reversed_meaning="生活中似乎出现了一些不如意的变化，或者感觉运气不太好。记住低谷是暂时的，轮子还会转回来，现在能做的是稳住自己。",
        symbol="🎡"
    ),
    TarotCard(
        id=11, name_cn="正义", name_en="Justice", category="大阿卡纳", suit=None,
        upright_keywords=["公正", "因果", "真相", "责任", "平衡"],
        upright_meaning="因果法则正在运作，做过的事情会得到相应的回报。现在需要诚实面对自己，做出公正的判断，承担应有的责任。",
        reversed_keywords=["不公", "逃避责任", "偏见", "失衡"],
        reversed_meaning="可能感受到某种不公正，或者自己在逃避某些责任。偏见会蒙蔽判断力，试着从更客观的角度重新审视局面。",
        symbol="⚖️"
    ),
    TarotCard(
        id=12, name_cn="倒吊人", name_en="The Hanged Man", category="大阿卡纳", suit=None,
        upright_keywords=["暂停", "牺牲", "换角度", "放手", "等待"],
        upright_meaning="有时候停下来不是退步，而是为了看到不同的风景。换一个角度看问题，放下执着，你会发现答案一直就在那里。",
        reversed_keywords=["拖延", "无谓牺牲", "固执", "抗拒改变"],
        reversed_meaning="可能一直在原地打转，不愿意做出必要的改变或牺牲。拖延只会让局面更复杂，是时候做个决定了。",
        symbol="🙃"
    ),
    TarotCard(
        id=13, name_cn="死神", name_en="Death", category="大阿卡纳", suit=None,
        upright_keywords=["结束", "转变", "新生", "告别", "蜕变"],
        upright_meaning="某个阶段正在走向终结，但结束意味着新的开始。不必恐惧变化，旧的不去新的不来，这是一次深层的蜕变和重生。",
        reversed_keywords=["抗拒结束", "恐惧改变", "停滞", "拒绝放手"],
        reversed_meaning="你可能紧紧抓着不该留的东西不放，害怕失去带来的未知感。但越是抗拒，越难前行。学会优雅地告别，才能迎接新生。",
        symbol="💀"
    ),
    TarotCard(
        id=14, name_cn="节制", name_en="Temperance", category="大阿卡纳", suit=None,
        upright_keywords=["平衡", "调和", "耐心", "适度", "疗愈"],
        upright_meaning="现在最需要的是平衡与适度。不要走极端，在各种力量之间找到和谐的中间点。耐心地调和矛盾，时间会帮你理顺一切。",
        reversed_keywords=["失衡", "过度", "急躁", "极端"],
        reversed_meaning="生活的某个方面可能失去了平衡，或者你太急于求成了。过度的投入反而会适得其反，需要重新校准节奏。",
        symbol="🍷"
    ),
    TarotCard(
        id=15, name_cn="恶魔", name_en="The Devil", category="大阿卡纳", suit=None,
        upright_keywords=["束缚", "欲望", "诱惑", "物质", "阴暗面"],
        upright_meaning="可能被某种欲望或不健康的模式所束缚，感觉难以挣脱。但仔细看看，那些锁链其实很松——你随时可以选择离开，关键是你愿不愿意。",
        reversed_keywords=["解脱", "打破束缚", "觉醒", "释放"],
        reversed_meaning="正在从某种束缚中挣脱出来，或者开始意识到那些限制你的东西其实可以被打破。这是一个觉醒和释放的好兆头。",
        symbol="😈"
    ),
    TarotCard(
        id=16, name_cn="高塔", name_en="The Tower", category="大阿卡纳", suit=None,
        upright_keywords=["突变", "崩塌", "颠覆", "真相揭露", "震动"],
        upright_meaning="一些看似稳固的东西可能突然被打破，这个过程会让人措手不及。但高塔的倒塌往往是为了清除不真实的基础，重建需要从真实开始。",
        reversed_keywords=["恐惧变化", "勉强维持", "内在危机", "延迟崩溃"],
        reversed_meaning="你感觉到变化即将来临却在抗拒它，或者一直在勉强维持着某种快要崩塌的状况。与其等它自然倒塌，不如主动做出调整。",
        symbol="⚡"
    ),
    TarotCard(
        id=17, name_cn="星星", name_en="The Star", category="大阿卡纳", suit=None,
        upright_keywords=["希望", "疗愈", "灵感", "平静", "信心"],
        upright_meaning="经历风雨之后，希望的光芒正在照耀你。这是一个疗愈和恢复的时期，内心会感到前所未有的平静。相信自己，美好的事情正在悄悄发生。",
        reversed_keywords=["失望", "缺乏信心", "创意枯竭", "迷茫"],
        reversed_meaning="可能暂时看不到希望的光，感到迷茫和失落。但星星不会消失，只是被云遮住了。给自己一些时间，阴霾终会散去。",
        symbol="⭐"
    ),
    TarotCard(
        id=18, name_cn="月亮", name_en="The Moon", category="大阿卡纳", suit=None,
        upright_keywords=["幻觉", "不安", "直觉", "潜意识", "恐惧"],
        upright_meaning="事情可能不像表面看起来那样，内心的不安和迷惑在提醒你注意。不要被恐惧驱动做决定，等迷雾散去后再看清楚全貌。",
        reversed_keywords=["走出迷惑", "真相浮现", "克服恐惧", "清醒"],
        reversed_meaning="之前困扰你的迷惑正在消散，你开始看清事情的真相。那些让你不安的恐惧，其实没有你想象的那么可怕。",
        symbol="🌛"
    ),
    TarotCard(
        id=19, name_cn="太阳", name_en="The Sun", category="大阿卡纳", suit=None,
        upright_keywords=["成功", "快乐", "活力", "乐观", "自信"],
        upright_meaning="阳光普照的好日子！充满活力和正面的能量，一切都在往好的方向发展。带着孩子般的喜悦和真诚去面对今天吧。",
        reversed_keywords=["暂时受阻", "过度乐观", "延迟的快乐", "自负"],
        reversed_meaning="好事可能来得比预期慢一些，或者过于乐观而忽视了潜在的问题。阳光还在，只是需要多一点耐心等它穿透云层。",
        symbol="☀️"
    ),
    TarotCard(
        id=20, name_cn="审判", name_en="Judgement", category="大阿卡纳", suit=None,
        upright_keywords=["觉醒", "重生", "反思", "召唤", "内在审视"],
        upright_meaning="一个深刻的内在觉醒正在发生，过去的经历都在为现在的你铺路。这是一个重新审视自己、做出重大决定的时刻，听从内心的召唤。",
        reversed_keywords=["自我怀疑", "逃避审视", "害怕评价", "拒绝改变"],
        reversed_meaning="可能在逃避面对自己内心深处的声音，或者害怕被评判。但成长需要勇气去正视过去，接受自己的全部才能真正前行。",
        symbol="📯"
    ),
    TarotCard(
        id=21, name_cn="世界", name_en="The World", category="大阿卡纳", suit=None,
        upright_keywords=["圆满", "完成", "成就", "旅程终点", "整合"],
        upright_meaning="一个重要的阶段正在圆满结束，所有的努力终于有了成果。享受这份成就感吧，同时也为下一段旅程的开始做好准备。",
        reversed_keywords=["未完成", "缺乏闭合", "拖延结束", "不圆满"],
        reversed_meaning="可能还有一些事情没有完全了结，或者感觉离终点差了最后一步。别急，补上缺失的那一块，圆满就在不远处。",
        symbol="🌍"
    ),
]


# ═══════════════════════════════════════════
# 56张小阿卡纳 - 权杖牌组
# ═══════════════════════════════════════════

WANDS = [
    TarotCard(
        id=22, name_cn="权杖一", name_en="Ace of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["灵感", "新机会", "创造力", "热情"],
        upright_meaning="一股新的创造能量正在涌入，可能是一个令人兴奋的新想法或机会。趁热情还在，赶紧行动起来把它变为现实。",
        reversed_keywords=["延迟", "缺乏动力", "错失机会", "虚假开始"],
        reversed_meaning="灵感似乎被堵住了，或者一个好机会因为犹豫而溜走。也许需要清除内心的障碍，重新找到那股冲劲。",
        symbol="🔥"
    ),
    TarotCard(
        id=23, name_cn="权杖二", name_en="Two of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["规划", "决策", "远见", "探索"],
        upright_meaning="站在十字路口，需要做出下一步的规划。你手握不止一种可能性，现在是时候制定计划并选择一个方向前进了。",
        reversed_keywords=["恐惧未知", "计划不周", "缺乏远见", "安于现状"],
        reversed_meaning="可能因为害怕未知而不敢往前走，或者计划做得不够周全。跳出舒适区虽然不容易，但原地踏步不会带来成长。",
        symbol="🔥"
    ),
    TarotCard(
        id=24, name_cn="权杖三", name_en="Three of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["拓展", "进展", "远方", "等待回报"],
        upright_meaning="前期的投入正在显现成果，视野正在变得开阔。可以考虑把眼光放得更远一些，拓展到新的领域或市场。",
        reversed_keywords=["回报延迟", "眼界狭窄", "挫折", "计划受阻"],
        reversed_meaning="期待的成果还没有到来，或者发展受到了限制。不要急躁，有时候回报需要更长的时间来酝酿。",
        symbol="🔥"
    ),
    TarotCard(
        id=25, name_cn="权杖四", name_en="Four of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["庆祝", "和谐", "里程碑", "归属感"],
        upright_meaning="值得庆祝的好时刻！达成了一个小里程碑，周围的人际关系也很和谐温暖。享受这份喜悦，和在乎的人一起分享。",
        reversed_keywords=["不安定", "缺乏归属", "庆祝受阻", "人际紧张"],
        reversed_meaning="可能在某个环境中感到不太安定，或者本该开心的事情被一些小摩擦影响了心情。先处理好让你不安的那件事。",
        symbol="🔥"
    ),
    TarotCard(
        id=26, name_cn="权杖五", name_en="Five of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["竞争", "冲突", "挑战", "不同意见"],
        upright_meaning="可能会遇到一些竞争或意见分歧，但这不一定是坏事。健康的竞争能激发潜力，关键是不要让争论变成人身攻击。",
        reversed_keywords=["避免冲突", "内耗", "妥协", "混乱"],
        reversed_meaning="为了避免冲突而一味退让，反而造成了内耗。也许适度表达自己的立场比息事宁人更有效。",
        symbol="🔥"
    ),
    TarotCard(
        id=27, name_cn="权杖六", name_en="Six of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["胜利", "认可", "成就", "自信"],
        upright_meaning="你的努力得到了认可和赞赏，这是一个值得骄傲的时刻。带着自信继续前行，好的势头还在延续。",
        reversed_keywords=["自负", "名声受损", "缺乏认可", "虚荣"],
        reversed_meaning="可能期待的认可没有到来，或者过于在意外界的评价。真正的自信来自内心，不需要所有人的掌声来证明。",
        symbol="🔥"
    ),
    TarotCard(
        id=28, name_cn="权杖七", name_en="Seven of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["坚守", "防御", "捍卫立场", "勇气"],
        upright_meaning="面对压力和挑战需要坚守自己的立场。你的位置是靠实力赢来的，不要轻易退让，勇敢地捍卫你所相信的。",
        reversed_keywords=["力不从心", "退让", "被击败", "放弃坚持"],
        reversed_meaning="也许已经筋疲力尽了，继续硬撑不一定是最好的选择。有时候战略性地后退一步，反而能看清全局。",
        symbol="🔥"
    ),
    TarotCard(
        id=29, name_cn="权杖八", name_en="Eight of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["快速行动", "进展", "消息", "势头"],
        upright_meaning="事情突然加速，信息和机会纷至沓来。现在适合快速决策和行动，犹豫太久反而会错过窗口期。顺着势头往前冲。",
        reversed_keywords=["延迟", "混乱", "方向不明", "受阻"],
        reversed_meaning="期待的消息迟迟未到，或者事情进展得比想象中慢。现在急不来，利用等待的时间把准备工作做得更充分。",
        symbol="🔥"
    ),
    TarotCard(
        id=30, name_cn="权杖九", name_en="Nine of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["坚韧", "毅力", "最后一关", "警惕"],
        upright_meaning="你已经走过了很长的路，虽然有些疲惫，但终点就在前方。再坚持一下，不要在最后一步放弃。你比自己以为的更强大。",
        reversed_keywords=["精疲力竭", "放弃", "偏执", "不愿妥协"],
        reversed_meaning="已经到了极限，身心俱疲。硬撑下去可能会适得其反，允许自己休息一下，恢复体力后再继续并不丢人。",
        symbol="🔥"
    ),
    TarotCard(
        id=31, name_cn="权杖十", name_en="Ten of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["负担", "责任过重", "压力", "硬撑"],
        upright_meaning="背负了太多的责任和压力，已经快要扛不住了。不必什么都自己扛，学会分担和取舍，放下不必要的负担。",
        reversed_keywords=["释放负担", "委派任务", "崩溃", "学会放手"],
        reversed_meaning="要么正在学着把部分责任交出去，要么已经被压垮了。无论哪种情况，现在最重要的是减轻自己的负荷。",
        symbol="🔥"
    ),
    TarotCard(
        id=32, name_cn="权杖侍从", name_en="Page of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["探索", "热忱", "好消息", "冒险精神"],
        upright_meaning="一个充满好奇心和冒险精神的时刻，可能会收到一个令人兴奋的消息或邀请。保持开放和热忱，去探索新的可能性。",
        reversed_keywords=["三分钟热度", "不切实际", "挫败", "缺乏方向"],
        reversed_meaning="热情来得快去得也快，一个想法还没落地就又被新的兴趣吸引了。试着专注在一件事上，把它做完再说。",
        symbol="🔥"
    ),
    TarotCard(
        id=33, name_cn="权杖骑士", name_en="Knight of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["冲劲", "冒险", "充满能量", "追求热情"],
        upright_meaning="充满行动力和冒险精神的能量，适合大胆地追求你想要的东西。带着激情和自信出发，不要让过多的思虑拖慢脚步。",
        reversed_keywords=["冲动", "鲁莽", "方向不定", "半途而废"],
        reversed_meaning="热情有余但耐心不足，做事容易虎头蛇尾或者方向频繁改变。在行动之前多想想，一根筋的冲锋不一定能到达目的地。",
        symbol="🔥"
    ),
    TarotCard(
        id=34, name_cn="权杖王后", name_en="Queen of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["自信", "温暖", "魅力", "独立"],
        upright_meaning="散发着温暖而自信的光芒，能够吸引和鼓舞身边的人。相信自己的判断，用你独特的方式去影响和创造。",
        reversed_keywords=["嫉妒", "自私", "控制欲", "缺乏自信"],
        reversed_meaning="可能因为不安全感而变得控制欲强或嫉妒他人的成就。回到自己的赛道上，你的光芒不需要和任何人比较。",
        symbol="🔥"
    ),
    TarotCard(
        id=35, name_cn="权杖国王", name_en="King of Wands", category="小阿卡纳", suit="权杖",
        upright_keywords=["领导力", "远见", "企业家精神", "果断"],
        upright_meaning="展现出强大的领导力和远见，能够把愿景变成现实。现在适合主导局面，用你的魄力和热情带领大家前进。",
        reversed_keywords=["专横", "不切实际", "独断", "急功近利"],
        reversed_meaning="领导欲过强反而让周围的人感到压力，或者目标设得太高太急。好的领导者知道何时倾听，何时放慢脚步。",
        symbol="🔥"
    ),
]


# ═══════════════════════════════════════════
# 56张小阿卡纳 - 圣杯牌组
# ═══════════════════════════════════════════

CUPS = [
    TarotCard(
        id=36, name_cn="圣杯一", name_en="Ace of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["新感情", "爱", "直觉", "情感涌动"],
        upright_meaning="一份新的情感正在萌芽，可能是一段新关系，也可能是内心深处被触动的感觉。打开心扉去接受爱和温暖。",
        reversed_keywords=["情感封闭", "爱被拒绝", "空虚", "情绪不稳"],
        reversed_meaning="可能在情感上筑起了高墙，不愿意让任何人靠近。或者一份感情没有得到回应。试着允许自己去感受，封闭不是保护。",
        symbol="💧"
    ),
    TarotCard(
        id=37, name_cn="圣杯二", name_en="Two of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["伙伴", "连接", "互相吸引", "合作"],
        upright_meaning="两颗心之间建立了美好的连接，无论是爱情、友谊还是合作伙伴关系，都在朝着和谐的方向发展。珍惜这份难得的默契。",
        reversed_keywords=["关系失衡", "误解", "分离", "信任缺失"],
        reversed_meaning="一段关系中可能出现了不平衡或误解，双方的给予和接受不太对等。坦诚的对话比沉默更能修复裂痕。",
        symbol="💧"
    ),
    TarotCard(
        id=38, name_cn="圣杯三", name_en="Three of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["友谊", "聚会", "庆祝", "社交"],
        upright_meaning="和朋友们在一起的愉快时光！适合社交、聚会和庆祝。人际关系中充满欢乐和温暖，享受这份陪伴带来的幸福感。",
        reversed_keywords=["社交倦怠", "八卦", "孤立", "过度放纵"],
        reversed_meaning="也许需要从频繁的社交中退出来喘口气，或者朋友圈里出现了一些让你不舒服的状况。质量比数量更重要。",
        symbol="💧"
    ),
    TarotCard(
        id=39, name_cn="圣杯四", name_en="Four of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["冷漠", "内省", "不满足", "错失"],
        upright_meaning="对眼前的一切感到无聊或不满足，注意力都放在缺少的东西上，反而忽略了身边已经存在的好机会。换个心态看看。",
        reversed_keywords=["觉醒", "重新发现", "抓住机会", "走出低谷"],
        reversed_meaning="开始从消极的状态中走出来，重新打开眼睛看到生活中的美好。一个之前被忽略的机会可能重新出现在眼前。",
        symbol="💧"
    ),
    TarotCard(
        id=40, name_cn="圣杯五", name_en="Five of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["失落", "遗憾", "悲伤", "只看消极面"],
        upright_meaning="为失去的东西感到悲伤和遗憾，但别忘了回头看看——还有没倒的杯子在等着你。允许自己悲伤，但不要沉溺其中。",
        reversed_keywords=["接受", "走出悲伤", "向前看", "原谅"],
        reversed_meaning="正在慢慢从悲伤中走出来，开始接受已经发生的事情。原谅过去、放下遗憾的过程虽然不容易，但你正在做到。",
        symbol="💧"
    ),
    TarotCard(
        id=41, name_cn="圣杯六", name_en="Six of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["回忆", "纯真", "故人", "怀旧"],
        upright_meaning="美好的回忆涌上心头，可能会遇到老朋友或想起过去的温暖时光。那份纯真的快乐提醒你，简单的幸福一直都在。",
        reversed_keywords=["活在过去", "无法放下", "不成熟", "过度怀旧"],
        reversed_meaning="过于沉浸在过去的回忆中，反而影响了现在的生活。怀旧是甜蜜的，但脚步要留在当下，未来还需要你去创造。",
        symbol="💧"
    ),
    TarotCard(
        id=42, name_cn="圣杯七", name_en="Seven of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["幻想", "选择太多", "白日梦", "诱惑"],
        upright_meaning="面前有太多选择和可能性，让人眼花缭乱。但不是每一个都是真实的——分清幻想和实际，选一个最靠谱的深入下去。",
        reversed_keywords=["回归现实", "聚焦", "做出选择", "清醒"],
        reversed_meaning="开始从幻想中醒来，看清楚什么是真正值得追求的。这种清醒虽然少了些浪漫，但多了份踏实。",
        symbol="💧"
    ),
    TarotCard(
        id=43, name_cn="圣杯八", name_en="Eight of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["离开", "寻找更多", "放弃", "精神追求"],
        upright_meaning="虽然现在拥有的看起来不错，但内心知道这不是你真正想要的。有勇气离开不再满足你的东西，去寻找更深层的意义。",
        reversed_keywords=["犹豫不走", "害怕改变", "得过且过", "回头"],
        reversed_meaning="知道应该离开却迈不开步，或者已经走了又想回头。不必急着做决定，但也别永远停在不属于你的地方。",
        symbol="💧"
    ),
    TarotCard(
        id=44, name_cn="圣杯九", name_en="Nine of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["满足", "愿望成真", "幸福", "富足"],
        upright_meaning="这是一张许愿牌！你内心的愿望很可能正在实现或即将实现。享受这份满足感和幸福吧，你值得拥有这一切。",
        reversed_keywords=["贪婪", "不满足", "浮夸", "愿望受阻"],
        reversed_meaning="也许得到了想要的东西却依然不快乐，或者愿望的实现遇到了一些阻碍。重新审视什么才是真正让你幸福的东西。",
        symbol="💧"
    ),
    TarotCard(
        id=45, name_cn="圣杯十", name_en="Ten of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["圆满", "家庭幸福", "和谐", "情感满足"],
        upright_meaning="情感上达到了一种圆满和谐的状态，家庭或亲密关系中充满了爱和温暖。这就是你一直追求的幸福，好好珍惜。",
        reversed_keywords=["家庭矛盾", "关系破裂", "不和谐", "理想幻灭"],
        reversed_meaning="家庭或亲密关系中可能出现了裂痕，现实和理想之间存在差距。修复关系需要双方的努力，先从理解和包容开始。",
        symbol="💧"
    ),
    TarotCard(
        id=46, name_cn="圣杯侍从", name_en="Page of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["浪漫", "直觉", "好消息", "创意"],
        upright_meaning="可能会收到一个温暖的消息或惊喜，内心变得柔软而充满创意。保持对美好事物的敏感度，让直觉引导你。",
        reversed_keywords=["情绪化", "不切实际", "消息延迟", "幼稚"],
        reversed_meaning="情绪起伏比较大，容易被感性冲昏头脑。在做重要决定之前，先让自己冷静下来，分清楚感受和事实。",
        symbol="💧"
    ),
    TarotCard(
        id=47, name_cn="圣杯骑士", name_en="Knight of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["浪漫追求", "邀请", "魅力", "理想主义"],
        upright_meaning="一份充满浪漫和理想色彩的邀请可能正在路上。跟随内心的感受，用真诚和温柔去追求你在乎的人或事。",
        reversed_keywords=["不切实际", "情感操控", "虚假承诺", "逃避现实"],
        reversed_meaning="当心那些听起来太美好的承诺，包括你自己对别人做的承诺。确保浪漫建立在真实的基础上，而不只是一时的感觉。",
        symbol="💧"
    ),
    TarotCard(
        id=48, name_cn="圣杯王后", name_en="Queen of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["共情", "温柔", "直觉力", "情感成熟"],
        upright_meaning="用温柔和理解去感受他人的情绪，你的共情能力是一种天赋。在照顾别人的同时，也别忘了关照自己的内心。",
        reversed_keywords=["过度敏感", "情绪依赖", "牺牲自我", "情感操控"],
        reversed_meaning="可能过于沉浸在他人的情绪中，把别人的问题当成了自己的。建立健康的情感边界，你不需要为所有人的感受负责。",
        symbol="💧"
    ),
    TarotCard(
        id=49, name_cn="圣杯国王", name_en="King of Cups", category="小阿卡纳", suit="圣杯",
        upright_keywords=["情绪稳定", "智慧", "包容", "情商高"],
        upright_meaning="能够在感性和理性之间保持平衡，用成熟的方式处理情绪。你的沉稳和包容让身边的人感到安心和信任。",
        reversed_keywords=["情绪压抑", "冷漠", "操控", "情绪爆发"],
        reversed_meaning="可能一直在压抑自己的真实感受，表面平静下面暗流涌动。找到安全的方式释放情绪，别让它们积累到爆发。",
        symbol="💧"
    ),
]


# ═══════════════════════════════════════════
# 56张小阿卡纳 - 宝剑牌组
# ═══════════════════════════════════════════

SWORDS = [
    TarotCard(
        id=50, name_cn="宝剑一", name_en="Ace of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["清晰", "真相", "突破", "新思维"],
        upright_meaning="思维变得异常清晰，能看透事物的本质。适合做重要的决定、说出真相，或者用全新的思路解决老问题。",
        reversed_keywords=["混乱", "误导", "思维受阻", "真相模糊"],
        reversed_meaning="脑子里一团乱麻，很难理清头绪。现在不适合做重大决定，等思路清晰了再说。也要小心被错误的信息误导。",
        symbol="⚔️"
    ),
    TarotCard(
        id=51, name_cn="宝剑二", name_en="Two of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["僵局", "两难", "拒绝面对", "需要平衡"],
        upright_meaning="面对一个左右为难的选择，迟迟不愿做决定。但蒙上眼睛不看不代表问题不存在，总有一刻需要摘下面具正视现实。",
        reversed_keywords=["做出选择", "真相浮现", "信息过载", "内心冲突"],
        reversed_meaning="被压抑的信息开始浮出水面，你不得不面对之前回避的问题。虽然不容易，但做出选择比悬而未决要好。",
        symbol="⚔️"
    ),
    TarotCard(
        id=52, name_cn="宝剑三", name_en="Three of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["心痛", "悲伤", "失望", "背叛"],
        upright_meaning="内心正在经历一种深刻的痛苦，可能是失望、分离或被伤害。这种痛是真实的，不必假装没事，允许自己哭一场。",
        reversed_keywords=["疗愈中", "释放痛苦", "原谅", "走出伤痛"],
        reversed_meaning="最痛的时刻正在过去，伤口在慢慢愈合。虽然疤痕还在，但你已经在学着原谅和放下了。继续往前走。",
        symbol="⚔️"
    ),
    TarotCard(
        id=53, name_cn="宝剑四", name_en="Four of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["休息", "恢复", "静养", "暂停反思"],
        upright_meaning="身心都需要一个暂停键。这不是偷懒，而是必要的恢复和充电。安静地休息，让思绪沉淀下来，恢复后你会更有力量。",
        reversed_keywords=["焦虑", "无法放松", "强迫自己", "过度疲劳"],
        reversed_meaning="明明已经很累了却停不下来，或者休息时也充满焦虑。你的身体在发出警告，请认真对待它的信号。",
        symbol="⚔️"
    ),
    TarotCard(
        id=54, name_cn="宝剑五", name_en="Five of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["争斗", "输赢", "自私", "冲突后果"],
        upright_meaning="一场争斗中，即使赢了也可能感觉失去了什么。不是每场仗都值得打，有时候放下争胜心反而能保全更重要的东西。",
        reversed_keywords=["和解", "认输", "吸取教训", "放下争斗"],
        reversed_meaning="意识到争吵没有赢家，开始愿意放下身段去和解。吸取这次的教训，有些战争根本不值得参与。",
        symbol="⚔️"
    ),
    TarotCard(
        id=55, name_cn="宝剑六", name_en="Six of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["过渡", "离开困境", "转移", "恢复"],
        upright_meaning="正在从一个困难的处境中慢慢走出来，虽然还没有完全到达彼岸，但最艰难的部分已经过去了。继续前行，平静的水域就在前方。",
        reversed_keywords=["无法离开", "停滞", "回到过去", "抗拒转变"],
        reversed_meaning="想要离开困境却似乎走不掉，或者刚离开又被拉回去。有些东西必须彻底放下，才能真正地过渡到新阶段。",
        symbol="⚔️"
    ),
    TarotCard(
        id=56, name_cn="宝剑七", name_en="Seven of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["策略", "隐瞒", "单打独斗", "聪明行事"],
        upright_meaning="有时候不必正面硬刚，用智慧和策略来解决问题更聪明。但也要注意，秘密和隐瞒的代价有时候比你想象的大。",
        reversed_keywords=["真相大白", "计划败露", "良心不安", "回归正道"],
        reversed_meaning="之前隐瞒的事情可能要被发现了，或者你自己决定不再遮掩。诚实虽然有时让人不舒服，但长远来看是更好的选择。",
        symbol="⚔️"
    ),
    TarotCard(
        id=57, name_cn="宝剑八", name_en="Eight of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["困境", "自我限制", "无力感", "受困"],
        upright_meaning="感觉被困住了、动弹不得，但很多束缚其实是自己给自己套上的。睁开眼睛看看，出路一直都在，只是你以为自己走不了。",
        reversed_keywords=["解脱", "看到出路", "自我释放", "新视角"],
        reversed_meaning="开始意识到困住自己的不是环境而是心态，正在一步步打破自我设限。每一小步的突破都值得鼓励。",
        symbol="⚔️"
    ),
    TarotCard(
        id=58, name_cn="宝剑九", name_en="Nine of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["焦虑", "噩梦", "失眠", "过度担忧"],
        upright_meaning="深夜的焦虑和担忧让人难以入眠，脑海中不断回放着最坏的情况。但很多恐惧都比现实中的困难要大得多，别让想象吓倒自己。",
        reversed_keywords=["走出焦虑", "面对恐惧", "释然", "寻求帮助"],
        reversed_meaning="焦虑开始慢慢减轻，你正在学着面对那些曾经让你彻夜难眠的恐惧。如果自己扛不住，向信任的人寻求帮助并不丢脸。",
        symbol="⚔️"
    ),
    TarotCard(
        id=59, name_cn="宝剑十", name_en="Ten of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["结束", "触底", "背叛", "最低谷"],
        upright_meaning="已经到了最低谷，不可能再更糟了——这其实是个好消息。既然已经触底，接下来只有往上走的方向。黎明就在最深的夜之后。",
        reversed_keywords=["复苏", "拒绝放弃", "最坏已过", "重新站起"],
        reversed_meaning="最痛苦的时刻已经过去，虽然还在恢复中，但你已经开始重新站起来了。每一天都会比昨天好一点。",
        symbol="⚔️"
    ),
    TarotCard(
        id=60, name_cn="宝剑侍从", name_en="Page of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["好奇心", "新想法", "观察", "求知"],
        upright_meaning="头脑特别活跃，对一切都充满好奇。适合学习新知识、收集信息或提出新的想法。保持敏锐的观察力，但也记得想好了再说。",
        reversed_keywords=["八卦", "草率", "刻薄", "消息不实"],
        reversed_meaning="小心说话太快太尖锐而伤到别人，也要对听到的信息保持怀疑。不是每一个传闻都值得传播。",
        symbol="⚔️"
    ),
    TarotCard(
        id=61, name_cn="宝剑骑士", name_en="Knight of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["果断", "快速行动", "思维敏捷", "直言不讳"],
        upright_meaning="思维如闪电般敏捷，行动力极强。看准了方向就立即出击，犹豫只会错过最佳时机。但也别忽略了周围人的感受。",
        reversed_keywords=["鲁莽", "攻击性", "言辞伤人", "仓促决定"],
        reversed_meaning="行动太快反而出了错，或者说话太直接伤到了人。慢下来不代表软弱，有时候三思而后行才是真正的智慧。",
        symbol="⚔️"
    ),
    TarotCard(
        id=62, name_cn="宝剑王后", name_en="Queen of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["清醒", "独立", "直率", "理性判断"],
        upright_meaning="用清醒的头脑和直率的态度去处理问题，不被感情左右判断。你的独立和理性在此刻是最大的优势，相信自己的分析。",
        reversed_keywords=["冷酷", "偏见", "过度批判", "情感压抑"],
        reversed_meaning="理性过了头就变成了冷酷，或者对人对事过于苛刻。适当地让温暖回来，不是所有事情都需要用逻辑来衡量。",
        symbol="⚔️"
    ),
    TarotCard(
        id=63, name_cn="宝剑国王", name_en="King of Swords", category="小阿卡纳", suit="宝剑",
        upright_keywords=["权威", "清晰思维", "公正", "逻辑分析"],
        upright_meaning="拥有清晰的逻辑思维和公正的判断力，适合处理需要理性决策的事务。用专业和客观的态度去引领方向。",
        reversed_keywords=["滥用权力", "冷漠无情", "独裁", "思维偏执"],
        reversed_meaning="可能过于执着于自己的观点而听不进不同的声音，或者用权力来压制异议。真正的智者知道自己的局限性。",
        symbol="⚔️"
    ),
]


# ═══════════════════════════════════════════
# 56张小阿卡纳 - 星币牌组
# ═══════════════════════════════════════════

PENTACLES = [
    TarotCard(
        id=64, name_cn="星币一", name_en="Ace of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["新财源", "机会", "物质基础", "播种"],
        upright_meaning="一个与物质和金钱相关的新机会出现了。可能是一份新工作、投资机会或者开始积累财富的好时机。抓住它，打好基础。",
        reversed_keywords=["错失机会", "财务不稳", "计划落空", "贪婪"],
        reversed_meaning="一个好的财务机会可能因为犹豫而溜走，或者投资方向选错了。在金钱方面需要更加谨慎和务实。",
        symbol="💰"
    ),
    TarotCard(
        id=65, name_cn="星币二", name_en="Two of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["平衡", "适应", "多任务", "灵活"],
        upright_meaning="同时在处理多件事情，需要灵活地调配时间和精力。虽然有点忙，但你应付得来。保持弹性，不要让任何一方失控。",
        reversed_keywords=["失衡", "应接不暇", "财务混乱", "力不从心"],
        reversed_meaning="同时要做的事情太多，已经开始顾不过来了。是时候重新排优先级，放下不那么紧急的事情。",
        symbol="💰"
    ),
    TarotCard(
        id=66, name_cn="星币三", name_en="Three of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["团队合作", "技能", "学习", "工匠精神"],
        upright_meaning="通过团队合作和专业技能取得进展的时候。虚心学习、发挥各自的长处，才能把事情做到最好。质量比速度更重要。",
        reversed_keywords=["配合不佳", "水平不够", "敷衍了事", "不受重视"],
        reversed_meaning="团队中的配合出了问题，或者你的专业能力没有得到应有的发挥和认可。主动沟通比默默抱怨更有效。",
        symbol="💰"
    ),
    TarotCard(
        id=67, name_cn="星币四", name_en="Four of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["守财", "安全感", "控制", "保守"],
        upright_meaning="对现有的东西抓得很紧，害怕失去。适度的谨慎是好的，但如果因为害怕而不敢投入任何东西，反而会限制自己的成长。",
        reversed_keywords=["放手", "过度消费", "财务不安", "打开心扉"],
        reversed_meaning="要么开始学着松开紧握的双手，要么因为守得太紧反而失去了什么。钱是流动的能量，过度执着反而会堵塞它的流通。",
        symbol="💰"
    ),
    TarotCard(
        id=68, name_cn="星币五", name_en="Five of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["困难", "财务危机", "孤立", "缺乏支持"],
        upright_meaning="正在经历一段物质或精神上的困难时期，感觉孤立无援。但帮助其实就在身边，只是你可能没有看到或不好意思开口。",
        reversed_keywords=["走出困境", "获得帮助", "恢复", "转机"],
        reversed_meaning="最困难的时期正在过去，开始有了转机的迹象。无论是财务上还是精神上，情况都在慢慢好转。",
        symbol="💰"
    ),
    TarotCard(
        id=69, name_cn="星币六", name_en="Six of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["慷慨", "给予", "分享", "公平"],
        upright_meaning="适合慷慨地分享你所拥有的，无论是金钱、时间还是知识。给予和接受之间保持平衡，付出终会以某种方式回到你身边。",
        reversed_keywords=["不公平", "施舍感", "自私", "债务"],
        reversed_meaning="给予和接受之间出现了不平衡，可能是付出太多没有回报，也可能是接受了不该接受的东西。重新审视这种不对等。",
        symbol="💰"
    ),
    TarotCard(
        id=70, name_cn="星币七", name_en="Seven of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["等待收获", "评估", "耐心", "长期投资"],
        upright_meaning="种子已经种下，需要耐心等待它发芽结果。现在是评估前期投入的好时机——方向对了就继续坚持，不对就及时调整。",
        reversed_keywords=["急于求成", "回报不足", "方向错误", "浪费"],
        reversed_meaning="付出了很多却看不到回报，让人沮丧和怀疑。也许需要重新评估方向是否正确，而不是继续在错误的道路上加倍投入。",
        symbol="💰"
    ),
    TarotCard(
        id=71, name_cn="星币八", name_en="Eight of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["勤奋", "精进", "匠心", "技能提升"],
        upright_meaning="现在是专注打磨技能和精进自我的好时机。一步一个脚印，认真对待手头的每一件事。量变终会引起质变。",
        reversed_keywords=["马虎", "厌倦", "技能不足", "缺乏动力"],
        reversed_meaning="对重复的工作感到厌倦，或者工作质量开始下滑。重新找到工作的意义感，哪怕是最日常的事情中也藏着成长的机会。",
        symbol="💰"
    ),
    TarotCard(
        id=72, name_cn="星币九", name_en="Nine of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["丰收", "独立", "享受成果", "品质生活"],
        upright_meaning="过去的努力开始带来丰厚的回报，可以好好享受劳动的成果了。你的独立和自律为自己创造了有品质的生活，这是你应得的。",
        reversed_keywords=["过度挥霍", "缺乏独立", "物质至上", "虚荣"],
        reversed_meaning="可能把幸福等同于物质享受，或者经济独立性不够强。真正的富足不只是银行卡里的数字，还有内心的充实。",
        symbol="💰"
    ),
    TarotCard(
        id=73, name_cn="星币十", name_en="Ten of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["财富传承", "家族", "稳定", "长久富足"],
        upright_meaning="物质和精神层面都达到了一种长久稳定的状态，不仅是个人的成功，更是对家庭和后代的庇荫。你正在建立的东西具有持久的价值。",
        reversed_keywords=["家族矛盾", "遗产纠纷", "不稳定", "短视"],
        reversed_meaning="家庭中可能因为金钱或遗产问题产生矛盾，或者过于追求短期利益而忽视了长远规划。把眼光放长远些。",
        symbol="💰"
    ),
    TarotCard(
        id=74, name_cn="星币侍从", name_en="Page of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["学习", "踏实", "新计划", "实践"],
        upright_meaning="一个务实的新计划或学习机会出现了。保持脚踏实地的态度，一步步把想法变成现实。好的开始是成功的一半。",
        reversed_keywords=["懒散", "不务实", "缺乏规划", "好高骛远"],
        reversed_meaning="想法不少但落地不够，或者总是在规划却不去执行。把手弄脏、真正开始做才是最重要的第一步。",
        symbol="💰"
    ),
    TarotCard(
        id=75, name_cn="星币骑士", name_en="Knight of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["稳健", "可靠", "坚持", "务实"],
        upright_meaning="用最踏实可靠的方式推进事情，不急不躁、稳扎稳打。虽然速度不快，但每一步都走得很实在，终点一定能到达。",
        reversed_keywords=["固执", "过于保守", "停滞", "无聊"],
        reversed_meaning="稳健过了头就变成了固执和守旧，不愿意接受任何变化。偶尔跳出常规思考一下，也许会发现更好的路。",
        symbol="💰"
    ),
    TarotCard(
        id=76, name_cn="星币王后", name_en="Queen of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["持家", "务实", "滋养", "财务管理"],
        upright_meaning="能够把工作和生活打理得井井有条，既能赚钱也懂得经营。你的务实和温暖让身边的人感到安心和被照顾。",
        reversed_keywords=["过度操劳", "忽视自我", "财务焦虑", "物质执念"],
        reversed_meaning="把所有精力都花在照顾别人和经营物质上，自己的身心却被忽略了。再能干的人也需要被照顾，别忘了那个人也可以是自己。",
        symbol="💰"
    ),
    TarotCard(
        id=77, name_cn="星币国王", name_en="King of Pentacles", category="小阿卡纳", suit="星币",
        upright_keywords=["财务成功", "稳定", "慷慨", "商业头脑"],
        upright_meaning="在物质世界中达到了一种稳定和成功的状态，具有出色的商业头脑和管理能力。你的可靠和慷慨为自己赢得了尊重。",
        reversed_keywords=["贪婪", "物质至上", "顽固", "过度控制"],
        reversed_meaning="可能过于看重金钱和地位，忽视了生活中其他同样重要的东西。成功不只是物质的积累，别让金钱成为你唯一的衡量标准。",
        symbol="💰"
    ),
]


# ═══════════════════════════════════════════
# 完整牌组
# ═══════════════════════════════════════════

TAROT_DECK = MAJOR_ARCANA + WANDS + CUPS + SWORDS + PENTACLES

# 图片URL基础路径（GitHub公版韦特塔罗牌）
_IMG_BASE = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards"


def get_card_image_url(card: TarotCard) -> str:
    """根据牌的ID获取韦特牌面图片URL"""
    cid = card.id
    if cid <= 21:
        return f"{_IMG_BASE}/m{cid:02d}.jpg"
    elif cid <= 35:
        return f"{_IMG_BASE}/w{cid - 21:02d}.jpg"
    elif cid <= 49:
        return f"{_IMG_BASE}/c{cid - 35:02d}.jpg"
    elif cid <= 63:
        return f"{_IMG_BASE}/s{cid - 49:02d}.jpg"
    else:
        return f"{_IMG_BASE}/p{cid - 63:02d}.jpg"
