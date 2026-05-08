# Pantheon Skills / 万神殿技能

Pantheon Skills 是一个小工具：把你反复告诉 AI Agent 的工作流，沉淀成可复用的 Codex skill。

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

它更像一个 skill 工厂：

```text
重复工作流 -> 生成 skill 草稿 -> audit -> benchmark -> 保留更好的版本
```

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

## 什么是 Codex Skill?

一个 Codex skill 本质上就是一个文件夹，里面有一个 `SKILL.md`，告诉 Codex：

- 什么时候应该触发这个 skill
- 这个工作流应该怎么执行
- 需要参考哪些规则、脚本、检查项
- 完成前应该怎么验证

最小结构：

```text
my-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

Pantheon 帮你创建、检查、评分和迭代这个文件夹。

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

名字只是一个比喻：把有用的 Agent 工作流保存下来。

不要被名字吓到。实际流程很朴素：

1. 读一个工作流 brief
2. 生成几个 skill 候选
3. 用 audit 检查结构和安全边界
4. 用 benchmark 在固定案例上评分
5. 保存更好的版本和 lineage report

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
