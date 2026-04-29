<p align="center">
  <img src="pantheon/assets/pantheon-mark.svg" width="120" alt="Pantheon mark">
</p>

<h1 align="center">Pantheon / 万神殿</h1>

<p align="center">
  <strong>把一次次踩坑得到的工作流，沉淀成可验证、可复用、能继续进化的 Codex skills。</strong>
</p>

<p align="center">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/English-README-17151f?style=for-the-badge"></a>
  <a href="README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-%E6%96%87%E6%A1%A3-f5c86a?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="pantheon/SKILL.md"><img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-17151f?style=flat-square"></a>
  <a href="pantheon/references/evolution-protocol.md"><img alt="Self Evolving" src="https://img.shields.io/badge/Self--Evolving-Bounded-f5c86a?style=flat-square"></a>
  <a href="pantheon/reports/alpaca-12.json"><img alt="Alpaca" src="https://img.shields.io/badge/Alpaca-8.0%2F10-2ea043?style=flat-square"></a>
  <a href="pantheon/reports/prompts-12.json"><img alt="Prompts" src="https://img.shields.io/badge/Prompts-8.0%2F10-2ea043?style=flat-square"></a>
  <a href="pantheon/references/language-policy.md"><img alt="Multilingual" src="https://img.shields.io/badge/Docs-Multilingual-0969da?style=flat-square"></a>
</p>

---

<table>
  <tr>
    <td><strong>提炼</strong><br>从混乱任务里抓出可复用流程。</td>
    <td><strong>铸造</strong><br>生成能安装、能复用的 Codex skill。</td>
    <td><strong>审计</strong><br>用实验和边界条件防止它失控。</td>
  </tr>
</table>

## 这个项目想解决什么

很多 AI 工作流，其实都死在聊天记录里。

今天你让 agent 修了一个很难的 bug，明天它又忘了这套检查流程。今天你总结出一套 code review 处理方法，下次又要重新解释。今天你把一个工具链跑通了，但经验没有沉淀成任何可以复用的东西。

Pantheon 做的事情很简单：把这些经验变成 **skills**。

不是普通 prompt，也不是无限自治的 agent。它更像一个“工作记忆容器”：把有用流程提炼出来，生成 skill，跑审计和 benchmark，确认安全边界，然后再考虑安装和演化。

> 不做偷偷自我修改。
>
> 不把一堆 prompt 包装成系统。
>
> 不用浪漫文案掩盖工程风险。
>
> Pantheon 要做的是：让经验变成可以复用的能力。

## 为什么它可能有用

Agent 最浪费时间的地方，往往不是不会写代码，而是反复忘记上下文：

- 项目里已有的约定
- 每次交付前必须跑的验证
- 某类任务的固定处理顺序
- 上次 debug 才发现的坑
- 哪些操作必须先问用户确认

Pantheon 把这些东西变成一套可以安装的 skill。

<p align="center">
  <img alt="Flow" src="https://img.shields.io/badge/%E6%B7%B7%E4%B9%B1%E4%BB%BB%E5%8A%A1-%E6%8F%90%E7%82%BC-17151f?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/%E5%B7%A5%E4%BD%9C%E6%B5%81-%E9%93%B8%E9%80%A0-f5c86a?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/skill-%E5%AE%A1%E8%AE%A1-0969da?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/%E8%AE%B0%E5%BF%86-%E5%AE%89%E8%A3%85-2ea043?style=for-the-badge">
</p>

## 它能做什么

<table>
  <tr>
    <th>模块</th>
    <th>能力</th>
    <th>说明</th>
  </tr>
  <tr>
    <td><img alt="Distill" src="https://img.shields.io/badge/01-Distill-17151f"></td>
    <td>提炼工作流</td>
    <td>从 brief、历史对话、重复任务里提取值得沉淀的流程。</td>
  </tr>
  <tr>
    <td><img alt="Scaffold" src="https://img.shields.io/badge/02-Scaffold-f5c86a"></td>
    <td>生成 skill</td>
    <td>生成包含 SKILL.md、references、scripts 和 metadata 的 Codex skill 目录。</td>
  </tr>
  <tr>
    <td><img alt="Audit" src="https://img.shields.io/badge/03-Audit-0969da"></td>
    <td>审计质量</td>
    <td>检查触发描述、占位符、上下文体积、验证步骤和自治边界。</td>
  </tr>
  <tr>
    <td><img alt="Experiment" src="https://img.shields.io/badge/04-Experiment-8250df"></td>
    <td>跑实验</td>
    <td>先在临时目录生成和验证 skill，再决定是否值得安装。</td>
  </tr>
  <tr>
    <td><img alt="Benchmark" src="https://img.shields.io/badge/05-Benchmark-2ea043"></td>
    <td>做对比</td>
    <td>在内置案例和公开数据集上，对比 Pantheon 生成器和朴素 baseline。</td>
  </tr>
  <tr>
    <td><img alt="Language" src="https://img.shields.io/badge/06-Language-c6538c"></td>
    <td>多语言</td>
    <td>按用户语言生成文档、说明和 skill 指南。</td>
  </tr>
</table>

## 实验结果

这个项目不是只讲概念，它带了可以复跑的实验报告。

<table>
  <tr>
    <th>Benchmark</th>
    <th>Cases</th>
    <th>Baseline Avg</th>
    <th>Pantheon Avg</th>
    <th>提升</th>
  </tr>
  <tr>
    <td>内置 skill forge 案例</td>
    <td align="right">4</td>
    <td align="right">2.00 / 10</td>
    <td align="right"><strong>8.25 / 10</strong></td>
    <td><img alt="4.1x" src="https://img.shields.io/badge/lift-4.1x-2ea043"></td>
  </tr>
  <tr>
    <td>Stanford Alpaca 样本</td>
    <td align="right">12</td>
    <td align="right">1.00 / 10</td>
    <td align="right"><strong>8.00 / 10</strong></td>
    <td><img alt="8.0x" src="https://img.shields.io/badge/lift-8.0x-2ea043"></td>
  </tr>
  <tr>
    <td>awesome-chatgpt-prompts 样本</td>
    <td align="right">12</td>
    <td align="right">1.75 / 10</td>
    <td align="right"><strong>8.00 / 10</strong></td>
    <td><img alt="4.6x" src="https://img.shields.io/badge/lift-4.6x-2ea043"></td>
  </tr>
</table>

验证结果：

```text
Pantheon audit: 10 passed, 0 failed
Codex quick_validate: Skill is valid
Skill-forge experiment: 9 passed, 0 failed
```

报告：

- [pantheon/reports/alpaca-12.json](pantheon/reports/alpaca-12.json)
- [pantheon/reports/prompts-12.json](pantheon/reports/prompts-12.json)

这些分数不是论文结论，也不是万能证明。它们的价值在于：这套系统可以被测试，可以失败，也可以继续迭代。

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

## 安全边界

Pantheon 可以进化，但不能偷偷进化。

它可以：

- 提出 skill 演化方案
- 生成补丁
- 跑审计和 benchmark
- 产出可安装的 skill 草案

它不应该：

- 没有确认就替换已安装 skill
- 声称跑过其实没跑的验证
- 用好听的文案掩盖危险操作
- 把 benchmark 分数包装成绝对质量保证

## Roadmap

- 接入更大的公开 benchmark
- 给生成出来的 skill 加人工偏好评审
- 做跨语言 skill 质量检查
- 给 skill evolution 加回归测试
- 做一个常见 agent 工作流的 skill gallery

## 宣言

每个团队都有一些说不清但很重要的经验。

某个命令一定要先跑。某个测试不能省。某类 PR 评论应该怎么处理。某个坑踩过一次就不想再踩第二次。

Pantheon 想把这些经验保存下来，但不是把它们冻住。它们可以继续演化，但每一步都要被看见、被验证、被确认。

把人的经验留下来。

让它变成工具。
