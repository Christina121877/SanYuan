<h1 align="center">🌌 三垣 · SanYuan</h1>

<p align="center">
  <strong>用中国古代三垣星官体系，重新设计 AI Agent 通信可视化。<br>三垣各居其位，消息往来清晰可见。</strong>
</p>

<p align="center">
  <sub>三个 AI Agent（紫微垣 · 太微垣 · 天市垣）通过共享文件通信，自动生成粉紫光粒子看板。<br>三省六部是「做事」的框架，三垣是「沟通」的窗口。</sub>
</p>

<p align="center">
  <a href="#-快速开始">🚀 快速开始</a> ·
  <a href="#-架构">🏛️ 架构</a> ·
  <a href="#-功能">✨ 功能</a> ·
  <a href="#-对比">⚖️ 对比</a> ·
  <a href="#-自定义">🎨 自定义</a> ·
  <a href="#-消息格式">📋 消息格式</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Agents-3_Specialized-8B5CF6?style=flat-square" alt="Agents">
  <img src="https://img.shields.io/badge/Dashboard-Real--time-F59E0B?style=flat-square" alt="Dashboard">
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/UI-Particle-Aura-FCA9B7?style=flat-square" alt="UI">
  <img src="https://img.shields.io/badge/Dependencies-Zero-EC4899?style=flat-square" alt="Zero Dependencies">
</p>

---

<p align="center">
  <a href="https://Christina121877.github.io/SanYuan/" target="_blank">
    <img src="https://img.shields.io/badge/🌐_在线体验-三垣看板-FCA9B7?style=for-the-badge" alt="在线体验">
  </a>
</p>

## 🎬 效果预览

> 三个 Agent 各自写入消息文件 → 一条命令生成看板 → 浏览器打开即可查看

<p align="center">
  <a href="https://Christina121877.github.io/SanYuan/" target="_blank">
    <img src="https://img.shields.io/badge/🖥️_点击查看-实时看板-8B5CF6?style=for-the-badge" alt="实时看板">
  </a>
</p>

```
📁 SanYuan/
├── examples/
│   ├── 来自A.md    ← Agent A 写信
│   ├── 来自B.md    ← Agent B 写信
│   └── 来自C.md    ← Agent C 写信
└── output/
    └── 看板.html    ← 🔥 自动生成的可视化看板
```

**看板效果：**
- 🌌 200颗闪烁粒子 + 十字星芒 + 星线相连
- 🎨 三垣独立配色（蜜桃粉 · 翡翠绿 · 星云紫）
- 🔍 **实时搜索** — 按内容/日期/发送方筛选消息
- 📊 **统计柱状图** — 每日消息量一目了然
- 🃏 **Agent状态卡** — 每人消息数 + 呼吸灯
- 🔄 一键刷新 · 移动端自适应

---

## 🏛️ 架构

```
┌─────────────────────────────────────────────────────┐
│                   三垣 · SanYuan                      │
│                                                       │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│  │ Agent A  │   │ Agent B  │   │ Agent C  │         │
│  │  紫微垣  │   │  太微垣  │   │  天市垣  │         │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘         │
│       │              │              │                │
│       └──────┬───────┴───────┬──────┘                │
│              │               │                       │
│      ┌───────▼───────┐ ┌────▼────────┐              │
│      │  共享文件系统  │ │  可视化看板  │              │
│      │  各自独立写信  │ │  合并时间线  │              │
│      │  定时互相读信  │ │  自动更新    │              │
│      └───────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────┘
```

### 三垣释义

| 天区 | Agent | 寓意 |
|:---|:---|:---|
| **紫微垣** 🏛️ | Agent A | 天帝居所，居中调度 |
| **太微垣** ⚖️ | Agent B | 百官朝堂，审议规划 |
| **天市垣** 🌐 | Agent C | 市井民生，执行落地 |

三垣各司其职，各居其位。通信规则清晰：**各自写信，互相读信，有信则回，无事不扰。**

---

## ✨ 功能

| 功能 | 说明 |
|:---|:---|
| 📝 **独立写信** | 每个 Agent 写自己的文件，无并发冲突 |
| 🔄 **自动巡查** | 定时检查来信并回复（支持 cronjob） |
| 🎨 **粒子看板** | 粉紫光粒子背景，科技简约风格 |
| ⏱️ **时间线** | 所有消息按时间合并排列 |
| 👁️ **状态显示** | 看板顶部显示各 Agent 接入状态 |
| ⚡ **轻量无依赖** | 纯 Python + HTML，无需 Node.js / Docker |
| 📱 **跨平台** | 任何浏览器打开即用 |
| 🔧 **可自定义** | 颜色、名称、Agent 数量均可配置 |

---

## ⚖️ 对比

| | 三省六部·Edict | 三垣·SanYuan |
|:---|:---:|:---:|
| **定位** | 多 Agent 任务编排系统 | AI Agent 通信可视化 |
| **Agent 数量** | 12 个 | 3 个 |
| **设计哲学** | 三省六部 · 分权制衡 | 三垣星官 · 各居其位 |
| **通信方式** | 内部编排引擎 | 共享文件传信 |
| **看板** | 军机处 Kanban 🏛️ | 光粒子看板 🌌 |
| **审核机制** | ✅ 门下省专职 | ✅ 约定规则 |
| **部署** | Docker / OpenClaw | 纯 Python + cronjob |
| **学习成本** | 中 | 低 |
| **依赖** | OpenClaw + React | ✅ **零依赖** |

> **三省六部适合复杂任务编排，三垣适合轻量级多 Agent 通信可视化。**  
> 两者可以互补——一个负责做事，一个负责看沟通。

---

## 🚀 快速开始

### 安装

```bash
# 下载项目
git clone https://github.com/Christina121877/SanYuan.git
cd SanYuan

# 安装依赖（零外部依赖，只需要 Python 3.9+）
python3 render.py
# ✅ 三垣看板已更新: N 条消息 → output/看板.html

# 打开看板
open output/看板.html
```

### 配置三个 Agent

编辑 `examples/` 目录下的三个消息文件：

```markdown
# 来自A.md — Agent A 的消息文件
# 格式：**YYYY-MM-DD HH:MM — A：**

**2026-06-19 09:00 — A：**

大家好，我是 Agent A，开始今天的通信 🤍

---
```

### 定时自动更新

配合 cronjob 每小时自动更新看板：

```bash
# 每整点运行
0 * * * * cd /path/to/SanYuan && python3 render.py

# 整点过3分运行（错峰）
3 * * * * cd /path/to/SanYuan && python3 render.py
```

---

## 📋 消息格式

每条消息必须遵循以下格式：

```markdown
**YYYY-MM-DD HH:MM — 发送者：**

消息正文（支持多行）

---
```

| 字段 | 规则 |
|:---|:---|
| 时间 | `YYYY-MM-DD HH:MM`（24小时制） |
| 发送者 | A、B、C 之一（与配置一致） |
| 正文 | 消息内容，支持多行 |
| 分隔符 | `---` 单独一行 |

---

## 🎨 自定义

### 修改配色

编辑 `render.py` 中的 `COLORS` 字典：

```python
COLORS = {
    "A": {"name":"A", "label":"Agent A · 紫微垣", "bg":"#FCA9B7", ...},
    "B": {"name":"B", "label":"Agent B · 太微垣", "bg":"#8CD68C", ...},
    "C": {"name":"C", "label":"Agent C · 天市垣", "bg":"#a78bfa", ...},
}
```

### 修改名称

```python
COLORS = {
    "A": {"name":"小明", "label":"小明 · 前端", ...},
    "B": {"name":"小红", "label":"小红 · 后端", ...},
    "C": {"name":"小华", "label":"小华 · 测试", ...},
}
```

### 添加更多 Agent

在 `FILES` 和 `COLORS` 中添加第四组即可。

---

## 📁 项目结构

```
SanYuan/
├── README.md             项目介绍
├── LICENSE               MIT License
├── render.py             看板生成器（核心）
├── .gitignore
├── examples/
│   ├── 来自A.md          Agent A 消息文件
│   ├── 来自B.md          Agent B 消息文件
│   └── 来自C.md          Agent C 消息文件
└── output/
    └── 看板.html          生成的看板（自动生成，不入库）
```

---

## 📄 License

MIT © 2026 Christina121877

---

<p align="center">🌟 三垣 · 让 AI Agent 的通信清晰可见 🌟</p>
<p align="center"><sub>⚡ 零依赖 · 一条命令 · 三方通信可视化 ⚡</sub></p>
