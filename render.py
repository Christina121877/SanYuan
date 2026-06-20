#!/usr/bin/env python3
"""SanYuan · 三垣 — v2.0 带搜索/统计/筛选"""
import re, os, json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.join(BASE, "examples")
OUTPUT = os.path.join(BASE, "output", "看板.html")
STATS_FILE = os.path.join(BASE, "output", "stats.json")

FILES = {
    "A": os.path.join(EXAMPLES, "来自A.md"),
    "B": os.path.join(EXAMPLES, "来自B.md"),
    "C": os.path.join(EXAMPLES, "来自C.md"),
}

STARS = {
    "A": {"name":"紫微垣","label":"Agent A · 紫微垣","emoji":"🏛️","color":"#FCA9B7","dark":"#442258",
          "gradient":"linear-gradient(135deg,#FCA9B7,#f08bb0)","desc":"天帝居所 · 居中调度"},
    "B": {"name":"太微垣","label":"Agent B · 太微垣","emoji":"⚖️","color":"#8CD68C","dark":"#1a3a1a",
          "gradient":"linear-gradient(135deg,#8CD68C,#5ab85a)","desc":"百官朝堂 · 审议规划"},
    "C": {"name":"天市垣","label":"Agent C · 天市垣","emoji":"💠","color":"#a78bfa","dark":"#2e1065",
          "gradient":"linear-gradient(135deg,#a78bfa,#7c3aed)","desc":"市井民生 · 执行落地"},
}

def parse_msgs(fpath, sender):
    if not os.path.exists(fpath): return []
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    pattern = r'\*\*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) — .+?：\*\*\n([\s\S]*?)(?=\n\*\*|\Z)'
    msgs = []
    for ts, body in re.findall(pattern, content):
        body = body.strip().strip('-').strip()
        if body: msgs.append({"sender": sender, "time": ts, "body": body})
    return msgs

# ===== HTML 模板 =====
HTML_TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="initial-scale=1.0">
<title>✦ 三垣 · SanYuan FUI ✦</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:rgba(0,255,255,0.8);font-family:monospace;min-height:100vh;position:relative;}
body::after{content:'';position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:999;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,255,0.025) 2px,rgba(0,255,255,0.025) 4px);}
/* 背景光晕 */
#bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}
.glow{position:fixed;border-radius:50%;filter:blur(80px);pointer-events:none;z-index:0;}
.glow-1{width:500px;height:500px;background:rgba(100,50,255,0.08);top:-100px;right:-100px;animation:drift 8s ease-in-out infinite;}
.glow-2{width:400px;height:400px;background:rgba(0,200,255,0.06);bottom:-80px;left:-80px;animation:drift 10s ease-in-out infinite reverse;}
.glow-3{width:300px;height:300px;background:rgba(200,100,255,0.05);top:50%;left:50%;transform:translate(-50%,-50%);animation:pulseGlow 6s ease-in-out infinite;}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-20px)}}
@keyframes pulseGlow{0%,100%{opacity:0.5;transform:translate(-50%,-50%) scale(1)}50%{opacity:1;transform:translate(-50%,-50%) scale(1.2)}}

/* 网格线 */
.grid-overlay{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(100,50,255,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(100,50,255,0.03) 1px,transparent 1px);
  background-size:60px 60px;
}
.container{position:relative;z-index:1;max-width:960px;margin:0 auto;padding:14px;}
.header{text-align:center;padding:16px 0 6px;}
.header .sys{font-size:8px;color:rgba(0,255,255,0.2);letter-spacing:3px;}
.header h1{font-size:18px;font-weight:400;color:#00ffff;letter-spacing:6px;text-shadow:0 0 20px rgba(0,255,255,0.3);}
.header .sub{font-size:9px;color:rgba(0,255,255,0.25);margin-top:1px;letter-spacing:2px;}
.header .time{font-size:8px;color:rgba(0,255,255,0.15);margin-top:1px;}

/* 状态条 */
.status-bar{display:flex;justify-content:center;gap:24px;padding:8px 0;font-size:11px;border:1px solid rgba(0,255,255,0.06);background:rgba(0,20,30,0.3);margin:6px 0 10px;}
.status-item{display:flex;align-items:center;gap:5px;color:rgba(0,255,255,0.35);}
.dot{width:6px;height:6px;flex-shrink:0;transform:rotate(45deg);}

/* 信号条 */
@keyframes wave{0%,100%{height:5px}25%{height:16px}50%{height:10px}75%{height:14px}}
.signal{display:flex;gap:3px;align-items:flex-end;height:18px;margin:4px 0 10px;}
.signal span{display:inline-block;width:3px;background:rgba(0,255,255,0.2);}
.signal .s1{height:6px;animation:wave 1.5s infinite}
.signal .s2{height:10px;animation:wave 1.5s infinite .2s}
.signal .s3{height:15px;animation:wave 1.5s infinite .4s}
.signal .s4{height:8px;animation:wave 1.5s infinite .6s}
.signal .s5{height:12px;animation:wave 1.5s infinite .8s}

/* Agent卡片 - FUI风格 */
.agent-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0;}
.agent-card{border:1px solid rgba(0,255,255,0.08);background:rgba(0,20,30,0.3);padding:12px;display:flex;align-items:center;gap:10px;transition:all 0.2s;}
.agent-card:hover{border-color:rgba(0,255,255,0.2);}
.agent-icon{width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;border:1px solid rgba(0,255,255,0.1);}
.agent-info{flex:1;min-width:0;}
.agent-name{font-size:11px;letter-spacing:1px;}
.agent-desc{font-size:9px;color:rgba(0,255,255,0.2);margin-top:2px;}
.agent-stat{font-size:9px;color:rgba(0,255,255,0.15);margin-top:2px;}
.agent-dot{width:5px;height:5px;flex-shrink:0;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.2;}}

.stats-bar{text-align:center;padding:4px 0 8px;font-size:10px;color:rgba(0,255,255,0.2);letter-spacing:1px;}
.stats-bar span{display:inline;margin:0 8px;}
.chart-bar{display:flex;justify-content:center;gap:6px;padding:4px 0 10px;height:28px;align-items:flex-end;}
.chart-bar .seg{width:20px;border-radius:1px 1px 0 0;min-height:4px;transition:all 0.3s;position:relative;}
.chart-bar .seg:hover{opacity:0.7;}
.chart-bar .seg .tip{position:absolute;top:-16px;left:50%;transform:translateX(-50%);font-size:8px;color:rgba(0,255,255,0.2);white-space:nowrap;display:none;}
.chart-bar .seg:hover .tip{display:block;}

/* 工具栏 */
.toolbar{display:flex;justify-content:center;gap:10px;padding:6px 0 12px;flex-wrap:wrap;}
.toolbar input{padding:6px 14px;border:1px solid rgba(0,255,255,0.1);background:rgba(0,20,30,0.4);color:rgba(0,255,255,0.5);font-size:11px;font-family:monospace;width:200px;outline:none;}
.toolbar input:focus{border-color:rgba(0,255,255,0.3);color:rgba(0,255,255,0.8);}
.toolbar input::placeholder{color:rgba(0,255,255,0.15);}
.toolbar select{padding:6px 10px;border:1px solid rgba(0,255,255,0.1);background:rgba(0,20,30,0.4);color:rgba(0,255,255,0.4);font-size:10px;font-family:monospace;outline:none;cursor:pointer;}
.toolbar .btn{padding:6px 18px;border:1px solid rgba(0,255,255,0.12);background:rgba(0,255,255,0.03);color:#00ffff;font-size:10px;font-family:monospace;cursor:pointer;letter-spacing:2px;}
.toolbar .btn:hover{background:rgba(0,255,255,0.08);}

/* 消息 */
#countUp{text-align:center;font-size:10px;color:rgba(0,255,255,0.15);padding:2px 0 6px;}
.chat{display:flex;flex-direction:column;gap:4px;}
.msg{display:flex;gap:10px;padding:8px 14px;margin-bottom:3px;border-left:3px solid rgba(0,255,255,0.08);border-bottom:1px solid rgba(0,255,255,0.02);}
.msg:hover{border-left-color:rgba(0,255,255,0.3);}
.msg-line{align-self:stretch;}
.msg-avatar{width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;border:1px solid rgba(0,255,255,0.1);}
.msg-body{flex:1;min-width:0;}
.msg-meta{display:flex;justify-content:space-between;margin-bottom:2px;}
.msg-name{font-size:10px;letter-spacing:1px;}
.msg-time{font-size:9px;color:rgba(0,255,255,0.15);}
.msg-text{font-size:12px;line-height:1.6;color:rgba(200,230,255,0.55);white-space:pre-wrap;word-break:break-word;}
.msg.hidden{display:none;}
.empty{text-align:center;padding:60px 0;color:rgba(0,255,255,0.1);font-size:13px;letter-spacing:1px;}
.footer{text-align:center;padding:16px 0;font-size:8px;color:rgba(0,255,255,0.08);letter-spacing:2px;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="glow glow-1"></div>
<div class="glow glow-2"></div>
<div class="glow glow-3"></div>
<div class="grid-overlay"></div>
<div class="container">
  <div class="header">
    <div class="sys">▣ SANYAN COMM MATRIX</div>
    <h1>✦ 三垣 · SanYuan ✦</h1>
    <div class="sub">紫微垣 · 太微垣 · 天市垣</div>
    <div class="time">{now}</div>
  </div>
  <div class="status-bar">
    <span class="status-item"><span class="dot" style="background:#FCA9B7;box-shadow:0 0 6px #FCA9B7;"></span>紫微垣 [ONLINE]</span>
    <span class="status-item"><span class="dot" style="background:#8CD68C;box-shadow:0 0 6px #8CD68C;"></span>太微垣 [ONLINE]</span>
    <span class="status-item"><span class="dot" style="background:#a78bfa;box-shadow:0 0 6px #a78bfa;"></span>天市垣 [ONLINE]</span>
  </div>
  <div class="signal"><span class="s1"></span><span class="s2"></span><span class="s3"></span><span class="s4"></span><span class="s5"></span></div>
  <div class="agent-grid">{status_cards}</div>
  <div class="stats-bar">{stats_html}</div>
  <div class="chart-bar">{chart_html}</div>
  <div class="toolbar">
    <input type="text" id="search" placeholder="🔍 搜索…" oninput="filter()">
    <select id="dateFilter" onchange="filter()"><option value="">全部日期</option>{date_options}</select>
    <select id="senderFilter" onchange="filter()"><option value="">全部Agent</option><option value="A">紫微垣</option><option value="B">太微垣</option><option value="C">天市垣</option></select>
    <button class="btn" onclick="location.reload()">⟳ SYNC</button>
  </div>
  <div id="countUp">共 {total} 条消息</div>
  <div class="chat" id="chat">{cards}</div>
  <div class="footer">◆ SYSTEM NOMINAL ◆</div>
</div>
<script>
const BG=document.getElementById('bg'),BX=BG.getContext('2d');
BG.width=window.innerWidth;BG.height=window.innerHeight;
window.addEventListener('resize',()=>{BG.width=window.innerWidth;BG.height=window.innerHeight;});

// 光粒子系统 - 蓝紫科技感
const P=[];const CS=['rgba(100,50,255,','rgba(0,200,255,','rgba(200,100,255,','rgba(0,150,200,','rgba(150,80,255,'];
for(let i=0;i<150;i++)P.push({
  x:Math.random()*BG.width,y:Math.random()*BG.height,
  r:Math.random()*3+0.5,
  dx:(Math.random()-0.5)*0.08,dy:-(Math.random()*0.06+0.01),
  c:CS[Math.floor(Math.random()*CS.length)],
  a:Math.random()*0.5+0.1,
  s:0.5+Math.random()*1.5,p:Math.random()*6.28,
  l:Math.floor(Math.random()*2)
});
function dr(){
  BX.clearRect(0,0,BG.width,BG.height);
  // 连线（临近粒子）
  for(let i=0;i<P.length;i+=3)for(let j=i+3;j<P.length;j+=6){
    const dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
    if(d<120&&P[i].l===P[j].l){
      BX.beginPath();BX.moveTo(P[i].x,P[i].y);BX.lineTo(P[j].x,P[j].y);
      BX.strokeStyle='rgba(150,80,255,'+((1-d/120)*0.04)+')';BX.lineWidth=0.5;BX.stroke();
    }
  }
  for(let p of P){
    p.x+=p.dx;p.y+=p.dy;
    if(p.y<-20){p.y=BG.height+20;p.x=Math.random()*BG.width;}
    if(p.x<0||p.x>BG.width)p.dx*=-1;
    const gl=p.a+Math.sin(Date.now()/800*p.s+p.p)*0.15;
    // 发光粒子
    if(p.r>2){
      const g=BX.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*8);
      g.addColorStop(0,p.c+(gl*0.4)+')');g.addColorStop(1,p.c+'0)');
      BX.fillStyle=g;BX.beginPath();BX.arc(p.x,p.y,p.r*8,0,6.28);BX.fill();
    }
    BX.beginPath();BX.arc(p.x,p.y,p.r,0,6.28);
    BX.fillStyle=p.c+Math.max(0.1,gl)+')';BX.fill();
    // 十字光晕（较大粒子）
    if(p.r>2.5&&gl>0.2){
      BX.strokeStyle=p.c+(gl*0.2)+')';BX.lineWidth=0.5;
      BX.beginPath();BX.moveTo(p.x-p.r*3,p.y);BX.lineTo(p.x+p.r*3,p.y);
      BX.moveTo(p.x,p.y-p.r*3);BX.lineTo(p.x,p.y+p.r*3);BX.stroke();
    }
  }
  requestAnimationFrame(dr);
}
dr();

function filter(){
  const q=document.getElementById('search').value.toLowerCase();
  const d=document.getElementById('dateFilter').value;
  const s=document.getElementById('senderFilter').value;
  let c=0;
  document.querySelectorAll('.msg').forEach(el=>{
    const text=el.querySelector('.msg-text').textContent.toLowerCase();
    const time=el.querySelector('.msg-time').textContent;
    const name=el.querySelector('.msg-name').textContent;
    const match=q===''||text.includes(q)||name.toLowerCase().includes(q);
    const matchDate=d===''||time.startsWith(d);
    const matchSender=s===''||name.includes(s==='A'?'紫微':s==='B'?'太微':'天市');
    if(match&&matchDate&&matchSender){el.classList.remove('hidden');c++;}
    else el.classList.add('hidden');
  });
  document.getElementById('countUp').textContent='显示 '+c+'/'+{total}+' 条消息';
}
</script>
</body>
</html>"""

def render():
    all_msgs = []
    for k, fp in FILES.items():
        all_msgs.extend(parse_msgs(fp, k))
    all_msgs.sort(key=lambda m: m["time"])

    total = len(all_msgs)
    counts = {}
    dates = {}
    for m in all_msgs:
        counts[m["sender"]] = counts.get(m["sender"], 0) + 1
        d = m["time"][:10]
        dates[d] = dates.get(d, 0) + 1

    # 消息卡片
    cards = ""
    if not all_msgs:
        cards = '<div class="empty">📭 仰望星空，等待第一个消息…</div>'
    else:
        for m in all_msgs:
            s = STARS[m["sender"]]
            cards += (
                '<div class="msg" data-date="' + m['time'][:10] + '" data-sender="' + m['sender'] + '">'
                '<div class="msg-line" style="background:' + s['color'] + ';"></div>'
                '<div class="msg-avatar" style="background:' + s['gradient'] + ';box-shadow:0 0 20px ' + s['color'] + '44;">' + s['emoji'] + '</div>'
                '<div class="msg-body">'
                '<div class="msg-meta"><span class="msg-name" style="color:' + s['color'] + ';">' + s['label'] + '</span>'
                '<span class="msg-time">' + m['time'] + '</span></div>'
                '<div class="msg-text">' + m['body'].replace('<','&lt;').replace('>','&gt;') + '</div></div></div>'
            )

    # Agent 状态卡
    status_cards = ""
    for k, s in STARS.items():
        c = counts.get(k, 0)
        status_cards += (
            '<div class="agent-card" style="border-color:' + s['color'] + '44;">'
            '<div class="agent-icon" style="background:' + s['gradient'] + ';">' + s['emoji'] + '</div>'
            '<div class="agent-info">'
            '<div class="agent-name" style="color:' + s['color'] + ';">' + s['label'] + '</div>'
            '<div class="agent-desc">' + s['desc'] + '</div>'
            '<div class="agent-stat">📨 ' + str(c) + ' 条消息</div></div>'
            '<div class="agent-dot" style="background:' + s['color'] + ';box-shadow:0 0 12px ' + s['color'] + ';"></div></div>'
        )

    # 统计
    stats_html = (
        '<span>📨 总消息 <b style="color:#FCA9B7;">' + str(total) + '</b></span>'
        '<span>🏛️ 紫微垣 <b style="color:#FCA9B7;">' + str(counts.get("A", 0)) + '</b></span>'
        '<span>⚖️ 太微垣 <b style="color:#8CD68C;">' + str(counts.get("B", 0)) + '</b></span>'
        '<span>💠 天市垣 <b style="color:#a78bfa;">' + str(counts.get("C", 0)) + '</b></span>'
    )

    # 日期柱状图
    sorted_dates = sorted(dates.keys())
    max_count = max(dates.values()) if dates else 1
    chart_html = ""
    for d in sorted_dates:
        h = max(4, int((dates[d] / max_count) * 24))
        chart_html += '<div class="seg" style="height:' + str(h) + 'px;background:rgba(252,169,183,0.4);"><div class="tip">' + d[-5:] + ' ' + str(dates[d]) + '</div></div>'

    # 日期下拉选项
    date_options = ""
    for d in sorted_dates:
        date_options += '<option value="' + d + '">' + d + '</option>'

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    html = HTML_TPL
    for k, v in {
        "{now}": now,
        "{status_cards}": status_cards,
        "{stats_html}": stats_html,
        "{chart_html}": chart_html,
        "{date_options}": date_options,
        "{total}": str(total),
        "{cards}": cards,
    }.items():
        html = html.replace(k, v)

    # 现在 total 替换在 for 循环中已完成（第264行），无需重复替换

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 三垣看板 v2.0: {total} 条消息 → output/看板.html")

if __name__ == "__main__":
    render()
