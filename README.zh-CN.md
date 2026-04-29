# Pantheon / 万神殿

Pantheon 是一个 Codex skill，用来创建、审计、验证和演化其他 Codex skills。

[English README](README.md)

它借用了《Pantheon / 万神殿》的精神内核：记忆只有在经历转化之后仍然保留责任边界，才真正变得有用。在这个项目里，一个 skill 被看作一种“上传后的工作记忆”：它从真实任务中提取流程，经过实验验证，然后作为可复用能力继续存在。

## 它能做什么

- 从混乱 brief、历史对话或重复工作流中提炼 skill 提案。
- 生成合法的 Codex skill 目录。
- 审计 skill 的触发描述、上下文体积、验证完整性、占位符和自治边界。
- 在临时目录运行实验：生成 skill，再审计它是否可用。
- 用 benchmark 比较 Pantheon 生成器和朴素 baseline。
- 下载公开数据集样本，并转换成 skill 创建 benchmark。
- 按用户偏好的语言生成 skill 草案、说明和报告。

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

## 快速开始

在仓库根目录运行：

```bash
python3 pantheon/scripts/pantheon.py audit pantheon
python3 pantheon/scripts/pantheon.py distill --input pantheon/experiments/skill-forge-basic.md
python3 pantheon/scripts/pantheon.py experiment --case pantheon/experiments/skill-forge-basic.md --workdir /tmp/pantheon-exp
python3 pantheon/scripts/pantheon.py benchmark --dataset pantheon/experiments/pantheon-benchmark.jsonl --workdir /tmp/pantheon-bench
```

公开数据集样本：

```bash
python3 pantheon/scripts/pantheon.py benchmark-public --name alpaca --limit 12 --report pantheon/reports/alpaca-12.json
python3 pantheon/scripts/pantheon.py benchmark-public --name awesome-chatgpt-prompts --limit 12 --report pantheon/reports/prompts-12.json
```

当前支持：

- `alpaca`：Stanford Alpaca 指令数据，来自 `tatsu-lab/stanford_alpaca`
- `awesome-chatgpt-prompts`：角色提示数据，来自 `f/awesome-chatgpt-prompts`

## 实验设计

benchmark 会在同一组 brief 上比较两个生成器：

- **Baseline**：生成一个最小、泛化的 skill。
- **Pantheon**：生成带 workflow、references、validation 和自治边界的 skill。

每个生成结果按 0 到 10 分评分：

- 触发清晰度
- 工作流复用价值
- 资源匹配度
- 验证完整性
- 自治边界

这些分数是工程证据，不是学术结论。它们的价值在于可复现、可失败，并且能在安装前暴露弱 skill。

## 当前实验结果

内置 benchmark：

```text
cases: 4
baseline_avg: 2.0 / 10
pantheon_avg: 8.25 / 10
```

公开数据集样本：

```text
Stanford Alpaca sample, 12 cases:
baseline_avg: 1.0 / 10
pantheon_avg: 8.0 / 10
report: pantheon/reports/alpaca-12.json

awesome-chatgpt-prompts sample, 12 cases:
baseline_avg: 1.75 / 10
pantheon_avg: 8.0 / 10
report: pantheon/reports/prompts-12.json
```

验证结果：

```text
Pantheon audit: 10 passed, 0 failed
Codex quick_validate: Skill is valid
Skill-forge experiment: 9 passed, 0 failed
```

## 作为 Codex Skill 安装

本地发现可以复制或软链接 `pantheon` 目录：

```bash
ln -s "$PWD/pantheon" "${CODEX_HOME:-$HOME/.codex}/skills/pantheon"
```

然后在 prompt 中调用：

```text
Use $pantheon to turn this repeated workflow into a validated Codex skill.
```

中文也可以：

```text
使用 $pantheon，把这个重复工作流沉淀成一个经过验证的 Codex skill。
```

## 安全模型

Pantheon 不是一个静默自我修改系统。

它可以：

- 提出进化方案。
- 生成补丁。
- 运行审计和 benchmark。
- 产出可安装的 skill 草案。

它不应该：

- 未确认就替换已安装 skill。
- 声称运行过并未运行的验证。
- 用浪漫语言掩盖破坏性修改。
- 把 benchmark 分数包装成普遍质量证明。

它的浪漫主义很朴素：保留人的记忆，但让记忆变得可执行。
