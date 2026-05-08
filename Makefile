.PHONY: audit demo benchmark evolve help

PYTHON ?= python3
PANTHEON := pantheon/scripts/pantheon.py
CASE := pantheon/experiments/skill-forge-basic.md
DATASET := pantheon/experiments/pantheon-benchmark.jsonl

help:
	@echo "Pantheon Skills commands:"
	@echo "  make audit      Audit the bundled pantheon skill"
	@echo "  make demo       Run a scaffold-and-audit demo"
	@echo "  make benchmark  Run the local benchmark"
	@echo "  make evolve     Run the evolution loop into /tmp"

audit:
	$(PYTHON) $(PANTHEON) audit pantheon

demo:
	$(PYTHON) $(PANTHEON) experiment --case $(CASE) --workdir /tmp/pantheon-exp

benchmark:
	$(PYTHON) $(PANTHEON) benchmark --dataset $(DATASET) --workdir /tmp/pantheon-bench

evolve:
	$(PYTHON) $(PANTHEON) evolve --brief $(CASE) --workdir /tmp/pantheon-evolve --report /tmp/pantheon-evolve/report.json --svg /tmp/pantheon-evolve/lineage.svg
