<p align="center">
  <img src="pantheon/assets/pantheon-hero-gpt.png" width="100%" alt="Pantheon Skills">
</p>

<p align="center">
  <a href="https://github.com/jweihe/Pantheon-skills/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/jweihe/Pantheon-skills/actions/workflows/ci.yml/badge.svg"></a>
  <a href="pantheon/SKILL.md"><img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-17151f?style=flat-square"></a>
  <img alt="No package install" src="https://img.shields.io/badge/deps-Python%20stdlib-f5c86a?style=flat-square">
  <a href="README.md"><img alt="English README" src="https://img.shields.io/badge/docs-English-0969da?style=flat-square"></a>
</p>

Pantheon Skills 是一个用于进化 Codex skills 的框架：把你反复告诉 AI Agent 的工作流，沉淀成可复用、可审计、可继续迭代的 skill。

它不是 prompt 合集，而是一个 skill evolution loop：seed、fork、mutate、score、select、merge、preserve lineage。

如果你总是在重复告诉 Agent：

- 这个项目提交前要跑哪些命令
- review 时要检查哪些问题
- 这个仓库有哪些隐藏约定
- 某类 bug 应该怎么排查
- 哪些操作必须先问人

那么 Pantheon 的作用就是把这些经验变成一个 `SKILL.md`，再配上 references、scripts、audit 和 benchmark。

## 具体例子

输入一个 brief：

```text
我们每次做一个小型前端工具，都会忘记同样的检查：
响应式布局、文字不能重叠、样例数据要真实、最后要截图检查。
把这个流程做成一个可复用的 Codex skill。
```

Pantheon 可以生成：

```text
frontend-tool-builder/
├── SKILL.md
├── agents/openai.yaml
└── references/checklist.md
```

然后它会 audit 这个 skill，也可以在固定 benchmark case 上和普通生成方式做对比。

## 一句话解释

Pantheon 不是一个“神秘的自进化 Agent”。

它更像一个有边界的 skill 进化系统：

```text
重复工作流 -> seed skill -> 多个变体 -> arena 评分 -> 合并胜者 -> 保存 lineage
```

## Skill Evolution

Pantheon 会从一个 seed workflow 开始，生成多个互相竞争的 skill variants。每个变体强调不同策略：

- **Archivist**：保存可复用的项目记忆
- **Smith**：把重复操作变成 scripts、references 和结构化流程
- **Oracle**：优化触发条件和语言表达
- **Judge**：强化验证、安全边界和可审计性
- **Arena**：面向固定 benchmark case 优化

这些变体会进入同一个 arena，用同一套标准评分。更强的变体会被选择、融合，形成 ascended skill。整个过程会留下 lineage report，下一次进化从证据开始，而不是从感觉开始。

## 60 秒跑起来

```bash
git clone https://github.com/jweihe/Pantheon-skills.git
cd Pantheon-skills
make audit
make demo
```

不需要安装额外依赖，核心脚本只用 Python 标准库。

正常输出应该类似：

```text
Pantheon audit: 10 passed, 0 failed
Skill-forge experiment: 9 passed, 0 failed
```

## 常用命令

### 1. 检查 Pantheon 自己

```bash
python3 pantheon/scripts/pantheon.py audit pantheon
```

### 2. 从一个 brief 生成 skill 草稿

```bash
python3 pantheon/scripts/pantheon.py scaffold \
  --brief pantheon/experiments/skill-forge-basic.md \
  --out /tmp/pantheon-skills
```

### 3. 跑一个完整 demo

```bash
python3 pantheon/scripts/pantheon.py experiment \
  --case pantheon/experiments/skill-forge-basic.md \
  --workdir /tmp/pantheon-exp
```

### 4. 对比普通生成和 Pantheon 生成

```bash
python3 pantheon/scripts/pantheon.py benchmark \
  --dataset pantheon/experiments/pantheon-benchmark.jsonl \
  --workdir /tmp/pantheon-bench
```

### 5. 跑一次 evolution 流程

```bash
python3 pantheon/scripts/pantheon.py evolve \
  --brief pantheon/experiments/skill-forge-basic.md \
  --workdir /tmp/pantheon-evolve \
  --report /tmp/pantheon-evolve/report.json \
  --svg /tmp/pantheon-evolve/lineage.svg
```

## 作为 Codex Skill 使用

把 `pantheon/` 目录软链到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/pantheon" "${CODEX_HOME:-$HOME/.codex}/skills/pantheon"
```

然后对 Codex 说：

```text
使用 $pantheon，把这个重复工作流沉淀成一个经过验证的 Codex skill。
```

英文也可以：

```text
Use $pantheon to turn this repeated workflow into a validated Codex skill.
```

## 为什么叫万神殿？

名字来自美剧《Pantheon》的启发。

这里真正有意思的不是“数字智能记得更多”，而是数字智能可以复制自己、分叉出多个版本、并行试错、合并有效经验，并把记忆跨代保存下来。

Pantheon 把这个想法落到 AI-agent skills 上：

- 一个重复工作流先变成 seed skill
- seed skill 分叉成多个 variants
- variants 围绕不同能力变异
- arena 在固定 case 上评分
- 胜出的 traits 被合并成更强 skill
- lineage 被保存，供下一轮进化继续使用

这不是无边界的自我修改。Pantheon 应该生成、审计、benchmark、提出 evolution，但不应该在没有确认的情况下替换已安装 skill。

## 品牌资产

主视觉图：[pantheon/assets/pantheon-hero-gpt.png](pantheon/assets/pantheon-hero-gpt.png)。

## Makefile 快捷命令

```bash
make audit       # 检查 pantheon/SKILL.md
make demo        # 跑 scaffold + audit demo
make benchmark   # 跑本地 benchmark
make evolve      # 跑 evolution 流程，输出到 /tmp
```

也可以直接看 CLI：

```bash
python3 pantheon/scripts/pantheon.py --help
```

## 当前结果

仓库里包含可复现报告：

- 内置 skill-forge benchmark：4 个 case，Pantheon 平均 8.25 / 10
- Stanford Alpaca sample：50 个 case，Pantheon 平均 8.00 / 10
- awesome-chatgpt-prompts sample：50 个 case，Pantheon 平均 8.00 / 10

这些只是工程 smoke test，不是“万能效果”声明。

## 项目结构

```text
pantheon/
├── SKILL.md
├── agents/openai.yaml
├── experiments/
├── references/
├── reports/
└── scripts/pantheon.py
```

## 安全边界

Pantheon 可以生成和测试 skill 草稿，但不应该静默替换你已经安装的 skill。

安装或替换前，请先看 diff，并运行：

```bash
python3 pantheon/scripts/pantheon.py audit path/to/skill
```

## 引用

```bibtex
@software{pantheon_skills_2026,
  title = {Pantheon-skills: A toolkit for creating and validating Codex skills},
  author = {He, Jwei},
  year = {2026},
  url = {https://github.com/jweihe/Pantheon-skills}
}
```

也可以使用 [CITATION.cff](CITATION.cff)。
