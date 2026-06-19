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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020617;font-family:'Inter','PingFang SC','Microsoft YaHei',sans-serif;min-height:100vh;overflow-x:hidden;position:relative;}
#bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;}
.container{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:16px 20px;}
.header{text-align:center;padding:20px 0 4px;}
.header h1{font-size:26px;font-weight:700;background:linear-gradient(135deg,#FCA9B7,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:4px;}
.header .sub{font-size:10px;color:#475569;margin-top:1px;letter-spacing:2px;}
.header .time{font-size:9px;color:#334155;margin-top:1px;font-weight:300;}
.agent-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:14px 0;}
.agent-card{background:rgba(15,23,42,0.7);border:1px solid;border-radius:10px;padding:12px;display:flex;align-items:center;gap:10px;position:relative;backdrop-filter:blur(6px);transition:all 0.2s;}
.agent-card:hover{background:rgba(15,23,42,0.9);transform:translateY(-1px);}
.agent-icon{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.agent-info{flex:1;min-width:0;}
.agent-name{font-size:11px;font-weight:600;letter-spacing:0.5px;}
.agent-desc{font-size:8px;color:#64748b;margin-top:1px;}
.agent-stat{font-size:8px;color:#475569;margin-top:2px;}
.agent-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.3;}}
.stats-bar{display:flex;justify-content:center;gap:24px;padding:4px 0 10px;font-size:10px;color:#475569;flex-wrap:wrap;}
.stats-bar span{display:flex;align-items:center;gap:5px;}
.toolbar{display:flex;justify-content:center;gap:8px;padding:6px 0 10px;flex-wrap:wrap;}
.toolbar input{padding:6px 12px;border-radius:16px;border:1px solid rgba(255,255,255,0.08);background:rgba(15,23,42,0.6);color:#94a3b8;font-size:12px;font-family:inherit;width:180px;outline:none;transition:all 0.2s;}
.toolbar input:focus{border-color:rgba(252,169,183,0.3);color:#e2e8f0;}
.toolbar input::placeholder{color:#475569;}
.toolbar select{padding:6px 10px;border-radius:16px;border:1px solid rgba(255,255,255,0.08);background:rgba(15,23,42,0.6);color:#94a3b8;font-size:11px;font-family:inherit;outline:none;cursor:pointer;}
.toolbar .btn{padding:6px 16px;border-radius:16px;border:1px solid rgba(252,169,183,0.15);background:rgba(252,169,183,0.05);color:#FCA9B7;font-size:11px;cursor:pointer;font-family:inherit;transition:all 0.2s;letter-spacing:0.5px;}
.toolbar .btn:hover{background:rgba(252,169,183,0.15);border-color:#FCA9B7;}
.chart-bar{display:flex;justify-content:center;gap:6px;padding:4px 0 10px;height:28px;align-items:flex-end;}
.chart-bar .seg{width:20px;border-radius:3px 3px 0 0;min-height:4px;transition:all 0.3s;position:relative;}
.chart-bar .seg:hover{opacity:0.8;}
.chart-bar .seg .tip{position:absolute;top:-16px;left:50%;transform:translateX(-50%);font-size:8px;color:#94a3b8;white-space:nowrap;display:none;}
.chart-bar .seg:hover .tip{display:block;}
.chat{display:flex;flex-direction:column;gap:3px;padding:2px 0;}
.msg{display:flex;align-items:flex-start;gap:12px;padding:12px 16px;margin-bottom:4px;position:relative;
  background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.03);border-radius:12px;
  backdrop-filter:blur(6px);transition:all 0.15s;}
.msg:hover{background:rgba(15,23,42,0.7);border-color:rgba(255,255,255,0.06);}
.msg-line{width:3px;border-radius:2px;flex-shrink:0;align-self:stretch;margin:2px 0;}
.msg-avatar{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;}
.msg-body{flex:1;min-width:0;}
.msg-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.msg-name{font-size:10px;font-weight:600;letter-spacing:0.3px;}
.msg-time{font-size:9px;color:#475569;font-weight:300;}
.msg-text{font-size:12px;line-height:1.6;color:#94a3b8;white-space:pre-wrap;word-break:break-word;}
.msg.hidden{display:none;}
.empty{text-align:center;padding:60px 0;color:#334155;font-size:13px;letter-spacing:1px;}
.footer{text-align:center;padding:16px 0;font-size:8px;color:#1e293b;letter-spacing:2px;}
#countUp{text-align:center;font-size:10px;color:#334155;padding:2px 0 6px;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="container">
    <div class="header">
        <h1>✦ 三垣 · SanYuan v2 ✦</h1>
        <div class="sub">紫微垣 · 太微垣 · 天市垣</div>
        <div class="time">{now}</div>
    </div>
    <div class="agent-grid">{status_cards}</div>
    <div class="stats-bar">{stats_html}</div>
    <div class="chart-bar">{chart_html}</div>
    <div class="toolbar">
        <input type="text" id="search" placeholder="🔍 搜索消息内容…" oninput="filter()">
        <select id="dateFilter" onchange="filter()"><option value="">全部日期</option>{date_options}</select>
        <select id="senderFilter" onchange="filter()"><option value="">全部Agent</option><option value="A">紫微垣</option><option value="B">太微垣</option><option value="C">天市垣</option></select>
        <button class="btn" onclick="location.reload()">⟳ 刷新</button>
    </div>
    <div id="countUp">共 {total} 条消息</div>
    <div class="chat" id="chat">{cards}</div>
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
function dr(){
    BX.clearRect(0,0,BG.width,BG.height);
    for(let p of P)if(p.l===0){
        const t=p.a+Math.sin(Date.now()/600*p.ts+p.tp)*0.2;
        const g=BX.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*6);
        g.addColorStop(0,p.c+(t*0.3)+')');g.addColorStop(1,p.c+'0)');
        BX.fillStyle=g;BX.beginPath();BX.arc(p.x,p.y,p.r*6,0,6.28);BX.fill();
    }
    for(let i=0;i<P.length;i+=2)for(let j=i+2;j<P.length;j+=4){
        const dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<100){
            BX.beginPath();BX.moveTo(P[i].x,P[i].y);BX.lineTo(P[j].x,P[j].y);
            BX.strokeStyle='rgba(255,255,255,'+((1-d/100)*0.06)+')';BX.lineWidth=0.5;BX.stroke();
        }
    }
    for(let p of P){
        p.x+=p.dx;p.y+=p.dy;
        if(p.y<-20){p.y=BG.height+20;p.x=Math.random()*BG.width;}
        if(p.x<0||p.x>BG.width){p.dx*=-1;}
        const t=p.a+Math.sin(Date.now()/800*p.ts+p.tp)*0.2;
        BX.beginPath();BX.arc(p.x,p.y,p.r,0,6.28);
        BX.fillStyle=p.c+Math.max(0.05,t)+')';BX.fill();
        if(p.r>2.5&&t>0.3){
            BX.strokeStyle=p.c+(t*0.15)+')';BX.lineWidth=0.5;
            BX.beginPath();BX.moveTo(p.x-p.r*2.5,p.y);BX.lineTo(p.x+p.r*2.5,p.y);
            BX.moveTo(p.x,p.y-p.r*2.5);BX.lineTo(p.x,p.y+p.r*2.5);BX.stroke();
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
        const matchSender=s===''||name.includes(s===A?'紫微':s===B?'太微':'天市');
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

    # 修复 JS 中的 total
    html = html.replace('{total}', str(total))

    # 修正 JS 中的 A/B 引用
    html = html.replace("name.includes(s===A?'紫微':s===B?'太微':'天市')",
                         "name.includes(s==='A'?'紫微':s==='B'?'太微':'天市')")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 三垣看板 v2.0: {total} 条消息 → output/看板.html")

if __name__ == "__main__":
    render()
