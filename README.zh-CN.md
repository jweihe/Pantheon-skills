<p align="center">
  <img src="pantheon/assets/pantheon-mark.svg" width="120" alt="Pantheon mark">
</p>

<h1 align="center">Pantheon / 万神殿</h1>

<p align="center">
  <strong>一个有边界的自进化 Codex skill 系统，把人的工作流变成可验证、可复用的 AI 记忆。</strong>
</p>

<p align="center">
  <a href="README.md">English README</a>
  ·
  <a href="pantheon/SKILL.md">Skill</a>
  ·
  <a href="pantheon/reports/alpaca-12.json">Alpaca Report</a>
  ·
  <a href="pantheon/reports/prompts-12.json">Prompts Report</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-17151f?style=for-the-badge">
  <img alt="Self Evolving" src="https://img.shields.io/badge/Self--Evolving-Bounded-f5c86a?style=for-the-badge">
  <img alt="Validation" src="https://img.shields.io/badge/Validation-10%2F10-brightgreen?style=for-the-badge">
  <img alt="Language" src="https://img.shields.io/badge/Language-Multilingual-blue?style=for-the-badge">
</p>

---

## 一句话

大多数 AI 工作流都会死在聊天记录里。

Pantheon 把它们变成 **skills**：一种小型、可安装、可审计、可测试、可 benchmark、可本地化、并且能在用户同意下继续演化的操作记忆。

它借用了《Pantheon / 万神殿》的精神核心：记忆如果能穿过形态变化仍保留责任边界，才真正获得第二次生命。在这个项目里，工作流不是被神秘化，而是被结构化、验证化、工具化。

> 不是 agent swarm。
>
> 不是 prompt 大杂烩。
>
> 不是偷偷自我修改。
>
> Pantheon 是一套把有价值的工作沉淀成持久 AI 能力的仪式。

## 为什么值得关注

AI agent 会不断重复浪费：

- 一遍遍重新发现项目约定
- 一遍遍忘记验证步骤
- 一遍遍重写脚手架
- 一遍遍丢失 debug 经验
- 产出看似有用、但完全无法测试的建议

Pantheon 给这些经验一个身体。

```text
混乱任务 -> 工作流提炼 -> skill 生成 -> 审计 -> benchmark -> 可安装记忆
```

## 它能做什么

| 能力 | 含义 |
| --- | --- |
| Distill | 从混乱 brief、历史对话或重复工作中提炼 skill 提案 |
| Scaffold | 生成合法的 Codex skill 目录 |
| Audit | 检查触发描述、占位符、上下文体积、验证完整性和自治边界 |
| Experiment | 在临时目录生成 skill，并在信任前验证 |
| Benchmark | 对比 Pantheon 生成结果和朴素 baseline |
| Public datasets | 支持 Stanford Alpaca 和 awesome-chatgpt-prompts 样本实验 |
| Multilingual | 按用户偏好语言生成文档和 skill 指南 |

## 实验结果

Pantheon 不只给截图和感觉，它带可复现报告。

| Benchmark | Cases | Baseline Avg | Pantheon Avg |
| --- | ---: | ---: | ---: |
| 内置 skill forge 案例 | 4 | 2.00 / 10 | 8.25 / 10 |
| Stanford Alpaca 样本 | 12 | 1.00 / 10 | 8.00 / 10 |
| awesome-chatgpt-prompts 样本 | 12 | 1.75 / 10 | 8.00 / 10 |

验证结果：

```text
Pantheon audit: 10 passed, 0 failed
Codex quick_validate: Skill is valid
Skill-forge experiment: 9 passed, 0 failed
```

报告：

- [pantheon/reports/alpaca-12.json](pantheon/reports/alpaca-12.json)
- [pantheon/reports/prompts-12.json](pantheon/reports/prompts-12.json)

这些分数不是“通用质量证明”，而是工程证据。重点是它有闭环：生成、审计、失败、修正、benchmark。

## 快速开始

```bash
python3 pantheon/scripts/pantheon.py audit pantheon
python3 pantheon/scripts/pantheon.py distill --input pantheon/experiments/skill-forge-basic.md
python3 pantheon/scripts/pantheon.py experiment --case pantheon/experiments/skill-forge-basic.md --workdir /tmp/pantheon-exp
python3 pantheon/scripts/pantheon.py benchmark --dataset pantheon/experiments/pantheon-benchmark.jsonl --workdir /tmp/pantheon-bench
```

运行公开数据集样本：

```bash
python3 pantheon/scripts/pantheon.py benchmark-public --name alpaca --limit 12 --report pantheon/reports/alpaca-12.json
python3 pantheon/scripts/pantheon.py benchmark-public --name awesome-chatgpt-prompts --limit 12 --report pantheon/reports/prompts-12.json
```

## 作为 Codex Skill 使用

通过软链接安装：

```bash
ln -s "$PWD/pantheon" "${CODEX_HOME:-$HOME/.codex}/skills/pantheon"
```

然后调用：

```text
Use $pantheon to turn this repeated workflow into a validated Codex skill.
```

中文也可以：

```text
使用 $pantheon，把这个重复工作流沉淀成一个经过验证的 Codex skill。
```

## 项目结构

```text
pantheon/
├── SKILL.md
├── agents/openai.yaml
├── assets/pantheon-mark.svg
├── experiments/
│   ├── pantheon-benchmark.jsonl
│   └── skill-forge-basic.md
├── references/
│   ├── evolution-protocol.md
│   ├── experiment-rubric.md
│   └── language-policy.md
├── reports/
│   ├── alpaca-12.json
│   └── prompts-12.json
└── scripts/pantheon.py
```

## 安全模型

Pantheon 的核心不是“无限自治”，而是“有见证的演化”。

它可以：

- 提出进化方案
- 生成补丁
- 运行审计和 benchmark
- 产出可安装的 skill 草案

它不应该：

- 未确认就替换已安装 skill
- 声称运行过并未运行的验证
- 用神话感文案掩盖破坏性修改
- 把 benchmark 分数包装成普遍质量证明

## Roadmap

- 更大的公开 benchmark 适配器
- 对生成 skill 草案加入人类偏好评审
- 跨语言 skill 质量检查
- skill evolution 回归测试
- 面向常见 agent 工作流的“神格 skill”画廊

## 宣言

每个团队都有隐形仪式。

那些大家记在脑子里的命令。那些发版前一定会跑的检查。那个只修过一次但永远不想再踩的 bug。那条让你真正理解系统的 code review 评论。

Pantheon 想保存这些仪式，但不把它们冻住。Skills 可以进化，但必须有见证。记忆可以变成可执行能力，但必须保留责任。

保留人的记忆。

让它成为工具。
