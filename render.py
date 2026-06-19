#!/usr/bin/env python3
"""SanYuan · 三垣 — v2.0"""
import re, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.join(BASE, "examples")
OUTPUT = os.path.join(BASE, "output", "看板.html")

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
HTML_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="initial-scale=1.0">
<title>✦ 三垣 · SanYuan ✦</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020617;font-family:'Inter','PingFang SC','Microsoft YaHei',sans-serif;min-height:100vh;overflow-x:hidden;position:relative;}
#bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}
.container{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:20px;}
.header{text-align:center;padding:28px 0 6px;}
.header h1{font-size:28px;font-weight:700;background:linear-gradient(135deg,#FCA9B7,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:4px;}
.header .sub{font-size:11px;color:#475569;margin-top:2px;letter-spacing:2px;}
.header .time{font-size:10px;color:#334155;margin-top:2px;font-weight:300;}
.agent-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:20px 0;}
.agent-card{background:rgba(15,23,42,0.7);border:1px solid;border-radius:12px;padding:14px;display:flex;align-items:center;gap:12px;position:relative;backdrop-filter:blur(6px);transition:all 0.2s;}
.agent-card:hover{background:rgba(15,23,42,0.9);transform:translateY(-1px);}
.agent-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}
.agent-info{flex:1;min-width:0;}
.agent-name{font-size:12px;font-weight:600;letter-spacing:0.5px;}
.agent-desc{font-size:9px;color:#64748b;margin-top:1px;}
.agent-stat{font-size:9px;color:#475569;margin-top:3px;}
.agent-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
.stats-bar{display:flex;justify-content:center;gap:32px;padding:8px 0 16px;font-size:11px;color:#475569;}
.stats-bar span{display:flex;align-items:center;gap:6px;}
.chat{display:flex;flex-direction:column;gap:4px;padding:4px 0;}
.msg{display:flex;align-items:flex-start;gap:14px;padding:14px 18px;margin-bottom:6px;position:relative;
  background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.03);border-radius:14px;
  backdrop-filter:blur(6px);transition:all 0.15s;}
.msg:hover{background:rgba(15,23,42,0.7);border-color:rgba(255,255,255,0.06);}
.msg-line{width:3px;border-radius:2px;flex-shrink:0;align-self:stretch;margin:2px 0;}
.msg-avatar{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;}
.msg-body{flex:1;min-width:0;}
.msg-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;}
.msg-name{font-size:11px;font-weight:600;letter-spacing:0.3px;}
.msg-time{font-size:10px;color:#475569;font-weight:300;}
.msg-text{font-size:13px;line-height:1.7;color:#94a3b8;white-space:pre-wrap;word-break:break-word;}
.empty{text-align:center;padding:80px 0;color:#334155;font-size:14px;letter-spacing:1px;}
.footer{text-align:center;padding:20px 0;font-size:9px;color:#1e293b;letter-spacing:2px;}
.btn-bar{display:flex;justify-content:center;gap:12px;padding:14px 0 4px;}
.btn{padding:6px 20px;border-radius:20px;border:1px solid rgba(252,169,183,0.2);background:rgba(252,169,183,0.05);color:#FCA9B7;font-size:11px;cursor:pointer;font-family:inherit;transition:all 0.2s;letter-spacing:1px;}
.btn:hover{background:rgba(252,169,183,0.15);border-color:#FCA9B7;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="container">
    <div class="header">
        <h1>✦ 三垣 · SanYuan ✦</h1>
        <div class="sub">紫微垣 · 太微垣 · 天市垣</div>
        <div class="time">{now}</div>
    </div>
    <div class="agent-grid">{status_cards}</div>
    <div class="stats-bar">{stats_html}</div>
    <div class="btn-bar"><button class="btn" onclick="location.reload()">⟳ 刷新</button></div>
    <div class="chat">{cards}</div>
    <div class="footer">✦ 三垣 · 让 AI Agent 的通信清晰可见 ✦</div>
</div>
<script>
const BG=document.getElementById('bg'),BX=BG.getContext('2d');
BG.width=window.innerWidth;BG.height=window.innerHeight;
window.addEventListener('resize',()=>{BG.width=window.innerWidth;BG.height=window.innerHeight;});
const P=[],CS=['rgba(252,169,183,','rgba(167,139,250,','rgba(140,214,140,','rgba(255,182,193,','rgba(200,160,255,'];
function mk(){return{
    x:Math.random()*BG.width,y:Math.random()*BG.height,
    r:Math.random()*4+0.3,
    dx:(Math.random()-0.5)*0.15,dy:-(Math.random()*0.1+0.04),
    c:CS[Math.floor(Math.random()*CS.length)],
    a:Math.random()*0.5+0.1,
    ts:0.5+Math.random()*1.5,tp:Math.random()*6.28,
    l:Math.floor(Math.random()*3),
}}
for(let i=0;i<200;i++)P.push(mk());
setInterval(()=>{P.push(mk());if(P.length>250)P.shift();},2000);
function draw(){
    BX.clearRect(0,0,BG.width,BG.height);
    // 层0大星光晕
    for(let p of P)if(p.l===0){
        const t=p.a+Math.sin(Date.now()/600*p.ts+p.tp)*0.2;
        const g=BX.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*6);
        g.addColorStop(0,p.c+(t*0.3)+')');g.addColorStop(1,p.c+'0)');
        BX.fillStyle=g;BX.beginPath();BX.arc(p.x,p.y,p.r*6,0,6.28);BX.fill();
    }
    // 连线
    for(let i=0;i<P.length;i+=2)for(let j=i+2;j<P.length;j+=4){
        const dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<100){
            BX.beginPath();BX.moveTo(P[i].x,P[i].y);BX.lineTo(P[j].x,P[j].y);
            BX.strokeStyle='rgba(255,255,255,'+((1-d/100)*0.06)+')';BX.lineWidth=0.5;BX.stroke();
        }
    }
    // 画粒子
    for(let p of P){
        p.x+=p.dx;p.y+=p.dy;
        if(p.y<-20){p.y=BG.height+20;p.x=Math.random()*BG.width;}
        if(p.x<0||p.x>BG.width){p.dx*=-1;}
        const t=p.a+Math.sin(Date.now()/800*p.ts+p.tp)*0.2;
        BX.beginPath();BX.arc(p.x,p.y,p.r,0,6.28);
        BX.fillStyle=p.c+Math.max(0.05,t)+')';BX.fill();
        // 十字星光芒
        if(p.r>2.5&&t>0.3){
            BX.strokeStyle=p.c+(t*0.15)+')';BX.lineWidth=0.5;
            BX.beginPath();BX.moveTo(p.x-p.r*2.5,p.y);BX.lineTo(p.x+p.r*2.5,p.y);
            BX.moveTo(p.x,p.y-p.r*2.5);BX.lineTo(p.x,p.y+p.r*2.5);BX.stroke();
        }
    }
    requestAnimationFrame(draw);
}
draw();
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
    for m in all_msgs:
        counts[m["sender"]] = counts.get(m["sender"], 0) + 1

    cards = ""
    if not all_msgs:
        cards = '<div class="empty">📭 仰望星空，等待第一个消息…</div>'
    else:
        for m in all_msgs:
            s = STARS[m["sender"]]
            cards += (
                '<div class="msg">'
                '<div class="msg-line" style="background:' + s['color'] + ';"></div>'
                '<div class="msg-avatar" style="background:' + s['gradient'] + ';box-shadow:0 0 20px ' + s['color'] + '44;">' + s['emoji'] + '</div>'
                '<div class="msg-body">'
                '<div class="msg-meta"><span class="msg-name" style="color:' + s['color'] + ';">' + s['label'] + '</span>'
                '<span class="msg-time">' + m['time'] + '</span></div>'
                '<div class="msg-text">' + m['body'] + '</div></div></div>'
            )

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

    stats_html = (
        '<span>📨 总消息 <b style="color:#FCA9B7;">' + str(total) + '</b></span>'
        '<span>🏛️ 紫微垣 <b style="color:#FCA9B7;">' + str(counts.get("A", 0)) + '</b></span>'
        '<span>⚖️ 太微垣 <b style="color:#8CD68C;">' + str(counts.get("B", 0)) + '</b></span>'
        '<span>💠 天市垣 <b style="color:#a78bfa;">' + str(counts.get("C", 0)) + '</b></span>'
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    html = HTML_TPL.replace("{now}", now)
    html = html.replace("{status_cards}", status_cards)
    html = html.replace("{stats_html}", stats_html)
    html = html.replace("{cards}", cards)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 三垣看板 v2.0: {total} 条消息 → output/看板.html")

if __name__ == "__main__":
    render()
