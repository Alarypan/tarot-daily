"""
网页模板生成 - 生成塔罗牌解读的HTML页面
"""

from typing import List, Dict
from tarot_data import get_card_image_url


def generate_html(date: str, weekday: str, cards: List[Dict], reading: str,
                  history: List[Dict] = None) -> str:
    """生成完整的HTML页面"""

    # 构建卡牌HTML
    cards_html = ""
    for i, card_info in enumerate(cards):
        card = card_info["card"]
        orientation = card_info["orientation"]
        position = card_info["position"]
        keywords = " / ".join(card_info["keywords"])
        image_url = get_card_image_url(card)
        is_reversed = orientation == "逆位"
        rotate_class = "reversed" if is_reversed else ""
        ori_badge = "↓ 逆位" if is_reversed else "↑ 正位"
        delay = i * 0.3

        cards_html += f"""
        <div class="card-wrapper" style="animation-delay: {delay}s">
          <div class="position-label">{position}</div>
          <div class="card {rotate_class}">
            <img src="{image_url}" alt="{card.name_cn}" loading="eager">
          </div>
          <div class="card-info">
            <div class="card-name">{card.name_cn}</div>
            <div class="card-en">{card.name_en}</div>
            <div class="orientation-badge {rotate_class}">{ori_badge}</div>
            <div class="keywords">{keywords}</div>
          </div>
        </div>
        """

    # 处理AI解读文本 -> HTML
    reading_html = _format_reading(reading)

    # 构建历史记录HTML
    history_html = ""
    if history:
        history_items = ""
        for day in history:
            date_str = day["date"]
            day_cards = day["cards"]
            card_tags = ""
            for c in day_cards:
                ori_class = "reversed" if c["orientation"] == "逆位" else ""
                ori_mark = "↓" if c["orientation"] == "逆位" else "↑"
                card_tags += f"""<span class="history-card {ori_class}">{c["name_cn"]} {ori_mark}</span>"""
            history_items += f"""
            <div class="history-day">
              <div class="history-date">{date_str}</div>
              <div class="history-cards">{card_tags}</div>
            </div>"""

        history_html = f"""
  <div class="history-section">
    <h2>近期牌面记录</h2>
    {history_items}
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>塔罗牌每日运势 - {date}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Noto Serif SC', 'PingFang SC', 'Microsoft YaHei', serif;
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2b 100%);
    color: #e8e0d0;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* 星空背景 */
  body::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image:
      radial-gradient(2px 2px at 20px 30px, #fff, transparent),
      radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
      radial-gradient(1px 1px at 90px 40px, #fff, transparent),
      radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
      radial-gradient(2px 2px at 160px 30px, #fff, transparent);
    background-size: 200px 100px;
    animation: twinkle 4s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
  }}

  @keyframes twinkle {{
    0% {{ opacity: 0.5; }}
    100% {{ opacity: 1; }}
  }}

  .container {{
    position: relative;
    z-index: 1;
    max-width: 960px;
    margin: 0 auto;
    padding: 40px 20px 60px;
  }}

  /* 头部 */
  .header {{
    text-align: center;
    margin-bottom: 50px;
  }}
  .header h1 {{
    font-size: 2.2em;
    font-weight: 700;
    color: #f0d890;
    text-shadow: 0 0 20px rgba(240, 216, 144, 0.3);
    margin-bottom: 12px;
    letter-spacing: 6px;
  }}
  .header .date {{
    font-size: 1.1em;
    color: #a098b0;
    letter-spacing: 2px;
  }}
  .divider {{
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #f0d890, transparent);
    margin: 20px auto;
  }}

  /* 卡牌区域 */
  .cards-section {{
    display: flex;
    justify-content: center;
    gap: 36px;
    margin-bottom: 60px;
    flex-wrap: wrap;
  }}

  .card-wrapper {{
    text-align: center;
    animation: fadeInUp 0.8s ease-out both;
  }}

  @keyframes fadeInUp {{
    from {{
      opacity: 0;
      transform: translateY(40px);
    }}
    to {{
      opacity: 1;
      transform: translateY(0);
    }}
  }}

  .position-label {{
    font-size: 1em;
    color: #a098b0;
    margin-bottom: 12px;
    letter-spacing: 4px;
    text-transform: uppercase;
  }}

  .card {{
    width: 180px;
    height: 310px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow:
      0 8px 32px rgba(0,0,0,0.5),
      0 0 20px rgba(240, 216, 144, 0.1);
    border: 2px solid rgba(240, 216, 144, 0.3);
    transition: transform 0.5s ease, box-shadow 0.3s ease;
    margin: 0 auto;
  }}
  .card:hover {{
    transform: scale(1.05);
    box-shadow:
      0 12px 40px rgba(0,0,0,0.6),
      0 0 30px rgba(240, 216, 144, 0.2);
  }}
  .card.reversed {{
    transform: rotate(180deg);
  }}
  .card.reversed:hover {{
    transform: rotate(180deg) scale(1.05);
  }}
  .card img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  .card-info {{
    margin-top: 16px;
  }}
  .card-name {{
    font-size: 1.3em;
    font-weight: 700;
    color: #f0d890;
    margin-bottom: 4px;
  }}
  .card-en {{
    font-size: 0.8em;
    color: #8880a0;
    margin-bottom: 8px;
  }}
  .orientation-badge {{
    display: inline-block;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.8em;
    background: rgba(100, 200, 120, 0.2);
    color: #90e0a0;
    border: 1px solid rgba(100, 200, 120, 0.3);
    margin-bottom: 8px;
  }}
  .orientation-badge.reversed {{
    background: rgba(200, 100, 100, 0.2);
    color: #e0a090;
    border-color: rgba(200, 100, 100, 0.3);
  }}
  .keywords {{
    font-size: 0.85em;
    color: #b0a8c0;
    line-height: 1.6;
    max-width: 200px;
    margin: 0 auto;
  }}

  /* 解读区域 */
  .reading-section {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(240, 216, 144, 0.15);
    border-radius: 16px;
    padding: 40px;
    margin-top: 20px;
    animation: fadeInUp 1.2s ease-out both;
  }}
  .reading-section h2 {{
    text-align: center;
    font-size: 1.5em;
    color: #f0d890;
    margin-bottom: 30px;
    letter-spacing: 4px;
  }}
  .reading-content {{
    line-height: 2;
    font-size: 1.05em;
    color: #d8d0c0;
  }}
  .reading-content h3 {{
    color: #f0d890;
    font-size: 1.15em;
    margin-top: 28px;
    margin-bottom: 10px;
    padding-left: 12px;
    border-left: 3px solid #f0d890;
  }}
  .reading-content p {{
    margin-bottom: 16px;
    text-indent: 0;
  }}

  /* 历史记录区域 */
  .history-section {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(160, 140, 200, 0.15);
    border-radius: 16px;
    padding: 30px 40px;
    margin-top: 30px;
    animation: fadeInUp 1.4s ease-out both;
  }}
  .history-section h2 {{
    text-align: center;
    font-size: 1.2em;
    color: #a098b0;
    margin-bottom: 20px;
    letter-spacing: 3px;
  }}
  .history-day {{
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }}
  .history-day:last-child {{
    border-bottom: none;
  }}
  .history-date {{
    color: #8880a0;
    font-size: 0.9em;
    min-width: 100px;
  }}
  .history-cards {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .history-card {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.8em;
    background: rgba(100, 200, 120, 0.1);
    color: #a0c8a0;
    border: 1px solid rgba(100, 200, 120, 0.2);
  }}
  .history-card.reversed {{
    background: rgba(200, 100, 100, 0.1);
    color: #c8a0a0;
    border-color: rgba(200, 100, 100, 0.2);
  }}

  /* 页脚 */
  .footer {{
    text-align: center;
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid rgba(240, 216, 144, 0.1);
    color: #686078;
    font-size: 0.9em;
  }}
  .footer .blessing {{
    font-size: 1.1em;
    color: #f0d890;
    margin-bottom: 10px;
    letter-spacing: 2px;
  }}
  .footer .credit {{
    color: #605878;
    font-size: 0.8em;
  }}

  /* 响应式 */
  @media (max-width: 700px) {{
    .cards-section {{
      flex-direction: column;
      align-items: center;
      gap: 30px;
    }}
    .header h1 {{
      font-size: 1.6em;
      letter-spacing: 3px;
    }}
    .reading-section {{
      padding: 24px;
    }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>塔罗牌每日运势</h1>
    <div class="divider"></div>
    <div class="date">{date}  {weekday}</div>
  </div>

  <div class="cards-section">
    {cards_html}
  </div>

  <div class="reading-section">
    <h2>今日运势解读</h2>
    <div class="reading-content">
      {reading_html}
    </div>
  </div>
{history_html}
  <div class="footer">
    <div class="blessing">愿你今天平安喜乐</div>
    <div class="credit">Rider-Waite Tarot &middot; AI Powered</div>
  </div>

</div>
</body>
</html>"""

    return html


def _format_reading(text: str) -> str:
    """将AI解读纯文本转为HTML"""
    lines = text.split("\n")
    html_parts = []
    current_paragraph = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                html_parts.append("<p>" + " ".join(current_paragraph) + "</p>")
                current_paragraph = []
            continue

        # 检测标题行 【xxx】
        if line.startswith("【") and "】" in line:
            if current_paragraph:
                html_parts.append("<p>" + " ".join(current_paragraph) + "</p>")
                current_paragraph = []
            # 提取标题
            title_end = line.index("】") + 1
            title = line[:title_end]
            rest = line[title_end:].strip()
            html_parts.append(f"<h3>{title}</h3>")
            if rest:
                current_paragraph.append(rest)
        else:
            current_paragraph.append(line)

    if current_paragraph:
        html_parts.append("<p>" + " ".join(current_paragraph) + "</p>")

    return "\n".join(html_parts)
