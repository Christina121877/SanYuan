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
<title>✦ 三垣 · SanYuan ✦</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:rgba(0,255,255,0.8);font-family:monospace;min-height:100vh;position:relative;}
body::after{content:'';position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:999;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,255,0.025) 2px,rgba(0,255,255,0.025) 4px);}

/* 蓝紫光晕 */
#bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}
.glow{position:fixed;border-radius:50%;filter:blur(80px);pointer-events:none;z-index:0;}
.glow-1{width:500px;height:500px;background:rgba(100,50,255,0.08);top:-100px;right:-100px;animation:drift 8s ease-in-out infinite;}
.glow-2{width:400px;height:400px;background:rgba(0,150,255,0.05);bottom:-80px;left:-80px;animation:drift 10s ease-in-out infinite reverse;}
.glow-3{width:300px;height:300px;background:rgba(200,100,255,0.04);top:50%;left:50%;transform:translate(-50%,-50%);animation:pulseGlow 6s ease-in-out infinite;}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-20px)}}
@keyframes pulseGlow{0%,100%{opacity:0.5;transform:translate(-50%,-50%) scale(1)}50%{opacity:1;transform:translate(-50%,-50%) scale(1.2)}}
.grid-overlay{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(100,50,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(100,50,255,0.03) 1px,transparent 1px);background-size:60px 60px;}

.container{max-width:960px;margin:0 auto;padding:24px 20px;}
.header{text-align:center;padding:28px 0 12px;}
.header .sys{font-size:10px;color:rgba(0,255,255,0.2);letter-spacing:4px;margin-bottom:4px;}
.header h1{font-size:24px;font-weight:300;color:#00ffff;letter-spacing:8px;text-shadow:0 0 30px rgba(0,255,255,0.25);margin-bottom:4px;}
.header .sub{font-size:11px;color:rgba(0,255,255,0.25);margin-top:4px;letter-spacing:3px;}
.header .time{font-size:10px;color:rgba(0,255,255,0.12);margin-top:6px;letter-spacing:1px;}

.status-bar{display:flex;justify-content:center;gap:32px;padding:10px 0;font-size:11px;border:1px solid rgba(0,255,255,0.06);background:rgba(0,20,30,0.2);margin:10px 0 14px;border-radius:2px;}
.status-item{display:flex;align-items:center;gap:6px;color:rgba(0,255,255,0.35);letter-spacing:1px;}
.sdot{width:6px;height:6px;flex-shrink:0;transform:rotate(45deg);}

@keyframes wave{0%,100%{height:5px}25%{height:16px}50%{height:10px}75%{height:14px}}
.signal{display:flex;gap:3px;align-items:flex-end;height:18px;margin:6px 0 14px;}
.signal span{display:inline-block;width:2px;background:rgba(0,255,255,0.18);}
.signal .s1{height:6px;animation:wave 1.8s infinite}
.signal .s2{height:10px;animation:wave 1.8s infinite .25s}
.signal .s3{height:15px;animation:wave 1.8s infinite .5s}
.signal .s4{height:8px;animation:wave 1.8s infinite .75s}
.signal .s5{height:12px;animation:wave 1.8s infinite 1s}

/* Agent卡片 */
.agent-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:12px 0 16px;}
.agent-card{border:1px solid rgba(0,255,255,0.06);background:rgba(0,20,30,0.2);padding:14px 12px;display:flex;align-items:center;gap:12px;transition:all 0.25s;}
.agent-card:hover{border-color:rgba(0,255,255,0.12);background:rgba(0,20,30,0.35);}
.agent-icon{width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;border:1px solid rgba(0,255,255,0.08);}
.agent-info{flex:1;min-width:0;}
.agent-name{font-size:11px;letter-spacing:1.5px;margin-bottom:3px;}
.agent-desc{font-size:9px;color:rgba(0,255,255,0.18);margin-bottom:2px;letter-spacing:0.5px;}
.agent-stat{font-size:8px;color:rgba(0,255,255,0.12);letter-spacing:0.5px;}
.agent-pulse{width:6px;height:6px;flex-shrink:0;animation:pulse 2.5s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.15;}}

.stats-bar{text-align:center;padding:6px 0 10px;font-size:10px;color:rgba(0,255,255,0.18);letter-spacing:1.5px;line-height:1.8;}
.stats-bar span{display:inline;margin:0 10px;}
.chart-bar{display:flex;justify-content:center;gap:8px;padding:4px 0 12px;height:28px;align-items:flex-end;}
.chart-bar .seg{width:20px;border-radius:1px 1px 0 0;min-height:4px;transition:all 0.3s;position:relative;}
.chart-bar .seg:hover{opacity:0.6;}
.chart-bar .seg .tip{position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:8px;color:rgba(0,255,255,0.2);white-space:nowrap;display:none;letter-spacing:0.5px;}
.chart-bar .seg:hover .tip{display:block;}

.toolbar{display:flex;justify-content:center;gap:10px;padding:6px 0 14px;flex-wrap:wrap;}
.toolbar input{padding:7px 14px;border:1px solid rgba(0,255,255,0.08);background:rgba(0,20,30,0.3);color:rgba(0,255,255,0.5);font-size:11px;font-family:monospace;width:200px;outline:none;transition:all 0.2s;}
.toolbar input:focus{border-color:rgba(0,255,255,0.25);color:rgba(0,255,255,0.8);}
.toolbar input::placeholder{color:rgba(0,255,255,0.1);}
.toolbar select{padding:7px 10px;border:1px solid rgba(0,255,255,0.08);background:rgba(0,20,30,0.3);color:rgba(0,255,255,0.35);font-size:10px;font-family:monospace;outline:none;cursor:pointer;transition:all 0.2s;}
.toolbar select:hover{border-color:rgba(0,255,255,0.15);}
.toolbar .btn{padding:7px 20px;border:1px solid rgba(0,255,255,0.1);background:rgba(0,255,255,0.02);color:#00ffff;font-size:10px;font-family:monospace;cursor:pointer;letter-spacing:3px;transition:all 0.25s;}
.toolbar .btn:hover{background:rgba(0,255,255,0.06);border-color:rgba(0,255,255,0.2);}

#countUp{text-align:center;font-size:10px;color:rgba(0,255,255,0.1);padding:2px 0 10px;letter-spacing:1px;}
.chat{display:flex;flex-direction:column;gap:6px;}
.msg{display:flex;gap:12px;padding:10px 16px;margin-bottom:2px;border-left:2px solid rgba(0,255,255,0.04);border-bottom:1px solid rgba(0,255,255,0.015);transition:all 0.2s;}
.msg:hover{border-left-color:rgba(0,255,255,0.15);background:rgba(0,255,255,0.01);}
.av{width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;border:1px solid rgba(0,255,255,0.08);margin-top:2px;}
.body{flex:1;min-width:0;}
.meta{display:flex;justify-content:space-between;margin-bottom:4px;}
.name{font-size:10px;letter-spacing:1.5px;color:rgba(0,255,255,0.45);}
.time{font-size:9px;color:rgba(0,255,255,0.12);letter-spacing:0.5px;}
.text{font-size:12px;line-height:1.8;color:rgba(200,230,255,0.5);white-space:pre-wrap;word-break:break-word;letter-spacing:0.3px;}
.msg.hidden{display:none;}
.empty{text-align:center;padding:60px 0;color:rgba(0,255,255,0.06);font-size:13px;letter-spacing:2px;line-height:2;}
.footer{text-align:center;padding:20px 0;font-size:8px;color:rgba(0,255,255,0.05);letter-spacing:3px;}
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
    <span class="status-item"><span class="sdot" style="background:#FCA9B7;box-shadow:0 0 6px #FCA9B7;"></span>紫微垣 [ONLINE]</span>
    <span class="status-item"><span class="sdot" style="background:#8CD68C;box-shadow:0 0 6px #8CD68C;"></span>太微垣 [ONLINE]</span>
    <span class="status-item"><span class="sdot" style="background:#a78bfa;box-shadow:0 0 6px #a78bfa;"></span>天市垣 [ONLINE]</span>
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
// 蓝紫光粒子
const BG=document.getElementById('bg'),BX=BG.getContext('2d');
BG.width=window.innerWidth;BG.height=window.innerHeight;
window.addEventListener('resize',()=>{BG.width=window.innerWidth;BG.height=window.innerHeight;});
const CS=['rgba(100,50,255,','rgba(0,150,255,','rgba(200,100,255,','rgba(0,200,255,','rgba(150,80,255,'];
const P=[];for(let i=0;i<150;i++)P.push({
  x:Math.random()*BG.width,y:Math.random()*BG.height,
  r:Math.random()*2.5+0.3,
  dx:(Math.random()-0.5)*0.08,dy:-(Math.random()*0.06+0.01),
  c:CS[Math.floor(Math.random()*CS.length)],
  a:Math.random()*0.4+0.08,s:0.5+Math.random()*1.5,p:Math.random()*6.28
});
function dr(){
  BX.clearRect(0,0,BG.width,BG.height);
  for(let i=0;i<P.length;i+=3)for(let j=i+3;j<P.length;j+=6){
    const d=Math.hypot(P[i].x-P[j].x,P[i].y-P[j].y);
    if(d<100){BX.beginPath();BX.moveTo(P[i].x,P[i].y);BX.lineTo(P[j].x,P[j].y);
      BX.strokeStyle='rgba(150,80,255,'+((1-d/100)*0.03)+')';BX.lineWidth=0.5;BX.stroke();}
  }
  for(let p of P){
    const gl=p.a+Math.sin(Date.now()/800*p.s+p.p)*0.12;
    p.x+=p.dx;p.y+=p.dy;
    if(p.y<-20){p.y=BG.height+20;p.x=Math.random()*BG.width;}
    if(p.x<0||p.x>BG.width)p.dx*=-1;
    if(p.r>1.8){const g=BX.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*6);
      g.addColorStop(0,p.c+(gl*0.3)+')');g.addColorStop(1,p.c+'0)');
      BX.fillStyle=g;BX.beginPath();BX.arc(p.x,p.y,p.r*6,0,6.28);BX.fill();}
    BX.beginPath();BX.arc(p.x,p.y,p.r,0,6.28);
    BX.fillStyle=p.c+Math.max(0.08,gl)+')';BX.fill();
    if(p.r>2.2&&gl>0.15){
      BX.strokeStyle=p.c+(gl*0.15)+')';BX.lineWidth=0.4;
      BX.beginPath();BX.moveTo(p.x-p.r*2.5,p.y);BX.lineTo(p.x+p.r*2.5,p.y);
      BX.moveTo(p.x,p.y-p.r*2.5);BX.lineTo(p.x,p.y+p.r*2.5);BX.stroke();}
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
    const text=el.querySelector('.text').textContent.toLowerCase();
    const time=el.querySelector('.time').textContent;
    const name=el.querySelector('.name').textContent;
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
                '<div class="av" style="background:' + s['gradient'] + ';box-shadow:0 0 12px ' + s['color'] + '44;border-color:' + s['color'] + '66;">' + s['emoji'] + '</div>'
                '<div class="body">'
                '<div class="meta"><span class="name" style="color:' + s['color'] + ';">' + s['label'] + '</span>'
                '<span class="time">' + m['time'] + '</span></div>'
                '<div class="text">' + m['body'].replace('<','&lt;').replace('>','&gt;') + '</div></div></div>'
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
            '<div class="agent-pulse" style="background:' + s['color'] + ';box-shadow:0 0 8px ' + s['color'] + ';"></div></div>'
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
