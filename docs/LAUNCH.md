# Launch plan

> Internal launch playbook. Not part of the public list.

## Strategic framing

This is a **companion-launch** repo. Curated lists tend to spike on the launch day, then plateau. The growth strategy is:

1. **Launch in the same week as a working repo** (`agent-backtest-lab` or similar — a runnable LLM trading-agent harness with an honest evaluation). Cross-link the two so the curated list captures category-search traffic and funnels readers to the working repo; the working repo gives the list a permanent referral source.
2. **Lead with the methodology section, not the list.** "Here are 60+ LLM-trading-agent projects" is content. "Here is how to know which ones to take seriously" is a magnet.
3. **Time the launch with a TradingAgents release window.** TradingAgents (73.7k★) gets disproportionate community attention around release notes; piggyback by cross-referencing into our list from related forum threads.

## Channel drafts

### Show HN

**Title:** *Show HN: A verified, honestly-annotated map of the LLM-trading-agent field*

**Body:**

> The LLM-trading-agent category has a 73k-star anchor (TradingAgents), several major academic frameworks (FinCon, FinAgent, FinMem, QuantAgent, AlphaAgents), and a maturing benchmark ecosystem (StockBench, INVESTORBENCH, Agent Market Arena). It also has a lot of projects whose attractive backtests don't survive contact with live markets.
>
> I built a curated, verification-rigorous directory of the field — 60+ frameworks, papers, datasets, benchmarks, and tools — with an honest one-paragraph note on each entry. Every entry has at least one corroborating verification source; weekly CI runs a link-checker.
>
> The most useful part is probably `docs/methodology.md` — a teaching guide on how to read any LLM-trading paper critically: look-ahead bias (made worse by LLMs), backtest overfitting, multiple-testing, the gross-vs-net cost gap, the difference between "out-of-sample" and "actually out-of-sample."
>
> Curated by a PhD candidate at HKU; CC0 list, MIT tools. PRs welcome; entry contributions require a verification source and a non-promotional honest note.
>
> https://github.com/bettyguo/awesome-llm-trading-agents

### X / Twitter thread (8 tweets, lead with the sharpest methodology insight)

1. *"Predicting" Apple's Q3 2022 earnings using GPT-4 (training cutoff: late 2023) is not prediction. It is, at best, recall. This single failure mode invalidates a surprising fraction of LLM-trading backtests. A thread on what to actually trust →*
2. *Most published LLM-trading strategies' backtests do not survive contact with live markets. Not because the authors did anything wrong — because the regime is hostile to ML claims. Today I'm releasing a curated, honestly-annotated map of the field that takes this seriously: 🧵*
3. *60+ verified frameworks, papers, datasets, benchmarks. Every entry has a one-paragraph honest note — what it is, what its own evaluation actually shows, what to be skeptical of. No marketing words; no financial advice; no inflated stars.*
4. *Anchor of the field: TradingAgents (73k stars, NeurIPS-track paper, LangGraph-based). Major sibling frameworks: FinMem, FinCon, FinAgent, FinRobot, QuantAgent, AlphaAgents. Major benchmarks: StockBench, Agent Market Arena, INVESTORBENCH.*
5. *The single most useful section is the methodology guide: how to critically read any LLM-trading paper. Look-ahead bias (especially the LLM-specific variant), backtest overfitting, the gross-vs-net cost gap, the meaning of "out-of-sample" when your model has trained on the world's text.*
6. *Key finding (per Agent Market Arena, 2025): in live trading, agent ARCHITECTURE — not LLM backbone choice — dominates profitability. If true, this is load-bearing for the whole field. Replication-worthy claim.*
7. *Tooling: weekly CI link-check; schema validation on every PR; auto-generated README from YAML entries; honest-note rules enforced by linter. Built so contributions stay rigorous.*
8. *Link: github.com/bettyguo/awesome-llm-trading-agents — CC0 list, MIT tools. PRs welcome, especially for entries from non-English-language research groups. If something is missing, open an issue.*

### r/MachineLearning post

**Title:** *[R] A verified, honestly-annotated directory of the LLM-trading-agent field (with a methodology section on look-ahead bias in LLMs)*

**Body:**

> Released today: a curated map of LLM-powered trading agents — multi-agent frameworks (TradingAgents, FinCon, FinMem, FinAgent, QuantAgent, AlphaAgents), single-agent / memory-augmented systems, foundational papers, datasets (PIXIU/FLARE, FinBen, FinQA, FNSPID), benchmarks (StockBench, INVESTORBENCH, Agent Market Arena), backtesting infrastructure, market simulators (ABIDES, PyMarketSim, JAX-LOB), and a teaching section on how to evaluate any such project critically.
>
> The methodology section may be of independent interest — it covers the LLM-specific variant of look-ahead bias (a 2025 result), the multiple-testing problem in prompt-engineering, the meaning of "out-of-sample" when your backbone was pre-trained on text through 2024, capacity / market impact, and a five-question checklist.
>
> Every entry has at least one corroborating verification source; weekly CI link-checks. CC0 list content, MIT tooling code.
>
> Link: https://github.com/bettyguo/awesome-llm-trading-agents

### r/algotrading post

**Title:** *Curated map of LLM trading agents + a "what to be skeptical of" section*

**Body:**

> If you have been following the LLM-trading-agent space (TradingAgents, FinGPT, FinRobot, etc.), here is a verified directory of 60+ projects across frameworks, papers, datasets, and benchmarks — with honest one-paragraph notes on each that try to be straight about what the project's own evaluation actually demonstrates and what to verify yourself.
>
> Two things that may be useful:
>
> 1. A methodology section on the LLM-specific failure modes — most importantly, the look-ahead bias from training on data that overlaps the backtest window. Most published LLM-trading papers from 2023–2024 have this problem and most do not address it.
> 2. A list of the credible benchmarks (StockBench, Agent Market Arena, INVESTORBENCH) so you can find out which projects actually deliver on real out-of-sample data.
>
> Not financial advice. CC0 list. PRs welcome.
>
> https://github.com/bettyguo/awesome-llm-trading-agents

### Newsletter / mailing-list outreach paragraph

> Curated, verified, honestly-annotated directory of the LLM-trading-agent ecosystem (60+ entries across frameworks, papers, datasets, benchmarks, simulators, tooling) with a methodology section on the LLM-specific failure modes in trading backtests. Released CC0; tooling MIT. From Betty Guo (PhD candidate at HKU). Link: github.com/bettyguo/awesome-llm-trading-agents

## Pre-launch checks

- [ ] All entries verified (`PLANNING/02_verification_log.md`).
- [ ] Link-check passes (`python tools/linkcheck.py`).
- [ ] Validator passes (`python tools/validate_entries.py`).
- [ ] README is fresh (`python tools/build_readme.py --check`).
- [ ] No marketing words in any note.
- [ ] Methodology document is the right length — long enough to be useful, short enough to be read.
- [ ] Banner renders in light + dark GitHub themes.
- [ ] The not-advice disclaimer is the first content block after the title.
- [ ] Curator attribution + ORCID present.
- [ ] LICENSE files both present.

## Post-launch monitoring

- Day 1–7: respond to PRs and corrections fast; the early "you missed X" signal is the best entry-discovery channel.
- Week 2–4: opportunistic cross-links from the methodology section into the relevant entries.
- Quarterly: re-run the verification pass on the top 20 stars-bearing entries.

## Companion repo

Plan to launch alongside `agent-backtest-lab` (or equivalent working repo) — a small, runnable LLM-trading-agent harness that uses the methodology section's checklist as evaluation primitives. The pairing produces: list pulls traffic, working repo converts traffic into engagement, methodology section is the glue.

The list does not block on the companion repo being ready, but the launch *thread* should mention both.
