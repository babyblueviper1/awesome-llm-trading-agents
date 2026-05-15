# Phase 0 — THINK

> Purpose: establish the landscape, the taxonomy, the seed list, the annotation methodology, the verification plan, the risk log, and the open questions before any code is written.

---

## 1. Landscape scan

The LLM-trading-agent space coalesced rapidly between late 2023 (FinMem, FinGPT) and 2026 (TradingAgents at 73k+ GitHub stars, paper revisions through v7). It now spans six distinguishable sub-fields:

### 1.1 Multi-agent LLM trading frameworks (the gravity well)
- **TradingAgents** (Xiao, Sun, Luo, Wang — arXiv 2412.20138, v7 on 2025‑06‑03; repo `TauricResearch/TradingAgents`). Specialized agents (fundamental / sentiment / technical / bull‑bear researchers / trader / risk manager) coordinated via LangGraph. 73.7k stars as of search time.
- **FinCon** (arXiv 2407.06567, NeurIPS 2024). Manager‑analyst hierarchy + conceptual verbal reinforcement; introduced episodic self‑critique to update systematic beliefs.
- **FinAgent** (arXiv 2402.18485). Multimodal foundation trading agent — numerical + textual + visual market data with tool augmentation.
- **FinRobot** (`AI4Finance-Foundation/FinRobot`). Platform-style: combines LLMs, RL, and quantitative analytics across forecasting / document-analysis / strategy agents.
- **QuantAgent** (`Y-Research-SBU/QuantAgent`). HFT-oriented; four specialized agents (Indicator/Pattern/Trend/Risk) over chart images.
- **AlphaAgents** (arXiv 2508.11152). Multi-agent equity portfolio construction via collaborative debate.
- **StockAgent** (`MingyuJ666/Stockagent`). LLM agents in a *simulated* market — evaluates trading behavior under external factors, not real-money returns.

### 1.2 Single‑agent LLM trading systems
- **FinMem** (Yu, Li et al. — arXiv 2311.13743; `pipiku915/FinMem-LLM-StockTrading`). Single agent with profiling + layered memory (with decay) + decision module. Foundational paper for memory‑aware LLM traders.
- **Fin-R1** (arXiv 2503.16252; `SUFE-AIFLM-Lab/Fin-R1`). 7B reasoning model, Qwen2.5 base, SFT + GRPO on Fin-R1-Data. Strong on FinQA / ConvFinQA but a financial *reasoning* model, not a live trading agent.

### 1.3 Reinforcement-learning trading libraries (the non-LLM peer category that LLM agents must be compared against)
- **FinRL** / **FinRL-X** (`AI4Finance-Foundation/FinRL`, NeurIPS 2020 paper arXiv 2011.09607).
- **Qlib** (`microsoft/qlib`). Full ML pipeline; supports RL via the `RD-Agent` extension.

### 1.4 Backtesting and execution libraries (essential infrastructure)
- **Backtrader**, **Zipline-Reloaded**, **VectorBT** / **VectorBT PRO**, **NautilusTrader**, **Backtesting.py**.

### 1.5 Benchmarks and datasets
- **PIXIU / FLARE** (arXiv 2306.05443; `The-FinAI/PIXIU`). Instruction data + benchmark for financial LLMs; foundational.
- **FinBen** (arXiv 2402.12659, NeurIPS 2024 D&B Track). 42 datasets / 24 tasks / 8 aspects.
- **FinanceBench** (Patronus AI / arXiv 2311.11944). 10k+ verified QA triplets from US public filings.
- **INVESTORBENCH** (arXiv 2412.18174, ACL 2025). First benchmark explicitly for *LLM-based agents* in financial decision-making (stocks / crypto / ETF).
- **StockBench** (arXiv 2510.02209). Contamination-controlled multi-month live-market trading benchmark; finds most LLM agents fail to beat buy-and-hold.
- **Agent Market Arena** (arXiv 2510.11695). Live multi-market trading benchmark — finds agent *architecture* dominates LLM backbone choice for profitability.
- **FNSPID** (large-scale financial news+stock-price corpus for LLM finance research).

### 1.6 Market-simulation environments
- **ABIDES / ABIDES-Markets / ABIDES-Gym** (`jpmorganchase/abides-jpmc-public`). High-fidelity multi-agent discrete-event market simulator; the standard for non-LLM agent research and increasingly the substrate for LLM agent experiments.

### 1.7 Methodology / critical literature (the teaching layer)
- López de Prado: *Probability of Backtest Overfitting*, *Deflated Sharpe Ratio*, *Combinatorial Purged Cross-Validation* — the canonical statistical critique of "looked great in backtest, died live".
- Recent LLM-specific bias literature: arXiv 2512.06607 (LAP test), 2512.23847 (look-ahead bias in LLM forecasts), arXiv 2505.07078 (do LLM strategies outperform long-run?). These directly attack the trap that an LLM "predicting" 2022 returns may simply have memorized 2022 from training.

### 1.8 Related existing lists (link generously)
- `georgezouq/awesome-ai-in-finance` — broad AI-in-finance, mostly framework-level.
- `Sasha-Cui/Awesome-Applied-Agents-for-Investment` — closest competitor, ~80 paper-focused entries across 6 sections, one-line descriptions, no critical annotations and no engineering/dataset/benchmark coverage.
- `DataArcTech/Awesome-FinLLMs` — bilingual EN/中, FinLLM-focused, includes papers/models/datasets.
- `hyp1231/awesome-llm-powered-agent` — general LLM agents (parent category).
- `wilsonfreitas/awesome-quant` — general quant (grandparent category).

**Conclusion:** there is **no comprehensive, verification-rigorous, honestly-annotated** directory that spans frameworks + papers + datasets + benchmarks + tooling + methodology together. The closest analog (Sasha-Cui) is paper-only and uncritical. This is the niche.

---

## 2. Taxonomy (the directory's spine)

Eight top-level categories. Order is deliberate: the framework section is where readers land, the methodology section is what they leave changed.

```
1. Multi-Agent LLM Trading Frameworks
2. Single-Agent / Memory-Augmented LLM Traders
3. Foundational & Influential Papers
   3a. Surveys
   3b. Multi-agent system papers
   3c. Memory / reasoning / planning papers
   3d. LLM-specific bias & evaluation papers
4. Financial Datasets
5. Benchmarks & Evaluations (the most safety-relevant section)
6. Backtesting & Execution Infrastructure
7. Market-Simulation Environments
8. Methodology & Common Pitfalls   (links to docs/methodology.md)
9. Related Lists
```

Optional sub-section under (3): "Reasoning-LLM Finance Models" (Fin-R1, Fino1, Agentar-Fin-R1) — these are model artifacts, not agents, so include with a clear note that they answer financial questions, they don't trade.

---

## 3. Seed list (Phase 0 confidence-bucketed — each must be re-verified in Phase 2)

**Confidence A (verified during Phase 0 web research, exists, factually known):**

Frameworks: TradingAgents, FinRobot, FinMem, FinCon (paper-only unless code released), FinAgent (paper), QuantAgent, AlphaAgents (paper), StockAgent, FinGPT.
Single-agent / RL libraries: FinRL, FinRL-X, Qlib.
Reasoning LLMs: Fin-R1, Fino1.
Backtesters: Backtrader, Zipline-Reloaded, VectorBT (community open-source), NautilusTrader, Backtesting.py.
Simulators: ABIDES (jpmorganchase/abides-jpmc-public).
Datasets / benchmarks: PIXIU/FLARE, FinBen, FinanceBench, INVESTORBENCH, StockBench, Agent Market Arena, FNSPID.
Methodology: López de Prado — *Probability of Backtest Overfitting*, *Deflated Sharpe Ratio*; *A Test of Lookahead Bias in LLM Forecasts* (arXiv 2512.23847); *A Fast and Effective Solution to Look-ahead Bias in LLMs* (arXiv 2512.06607); *Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?* (arXiv 2505.07078).
Related lists: awesome-ai-in-finance, Awesome-Applied-Agents-for-Investment, Awesome-FinLLMs, awesome-llm-powered-agent, awesome-quant.

**Confidence B (likely real, need verification before publishing):** FinCon repo release status, AlphaForge, Agentar-Fin-R1, TradingGoose, plus any FinAgent code repo (paper may not have an open repo).

**Confidence C (mentioned but not yet verified):** FinVerse (no result), various "Trading*GPT" variants — drop unless found and verified.

Target launch size: 100–200 entries with quality bias. Expansion in Phase 3 via the TradingAgents citation graph, GitHub `topic:trading + topic:llm`, finance-AI survey reference lists, and the AI4Finance ecosystem.

---

## 4. Annotation methodology

Every published entry carries a structured "honest note" of 1–3 sentences. The note must be:

1. **Evidence-based.** Cite what the project itself says it does, or what the paper's own evaluation shows; do not assert performance claims we cannot verify.
2. **Fair.** Describe limitations the project itself acknowledges, methodological gaps a careful reader would notice, or category mismatches (e.g. "this is a financial reasoning model, not a trading agent — comparing it to TradingAgents is a category error"). Never assert dishonesty or impugn competence.
3. **Non-promotional.** Strip marketing claims. "X *aims to* improve trading performance" → describe the architecture; let the reader judge.
4. **Useful.** The reader should be able to decide *whether to spend an hour on this* from the note alone.

**Standard note template (internal — do not appear verbatim in entries):**

> *What it is:* one phrase.
> *What it actually demonstrates (per its own paper / docs):* one phrase.
> *What to be cautious about / what to verify yourself:* one phrase, optional. Common categories: look-ahead bias risk if backtest uses pre-cutoff data with a recent LLM; toy universe (single ticker, short horizon); no comparison to buy-and-hold or to a sensible non-LLM baseline; reproducibility (closed weights, missing seeds); claimed returns gross of costs.

Worked example (TradingAgents):

> Multi-agent LLM trading framework on LangGraph with specialised analyst/researcher/trader/risk roles. The paper reports superior cumulative returns, Sharpe, and max drawdown vs. baselines on a stock-trading task; methodology and full result tables are in arXiv 2412.20138 (v7). As with any 2024–25 LLM trading study, readers should independently check whether the evaluation window post-dates the model's training cutoff and whether transaction costs are modelled.

Note the tone: factual, points the reader at what to check themselves, does not assert that the authors mishandled anything.

---

## 5. Verification plan

**Per entry, before it enters `entries/` as `status: verified`:**
1. URL resolves (HTTP 200) — `tools/linkcheck.py` enforces this in CI.
2. Title / authors / venue / year cross-checked against the source page (arXiv abstract page, GitHub repo header, or publisher landing page).
3. Star count or citation count is *approximate* and labelled "as of YYYY-MM" — never asserted as live.
4. The honest note has at minimum: one factual descriptor, one source for any non-trivial claim.
5. Logged in `PLANNING/02_verification_log.md` with the date of verification and the source URL(s) consulted.

**Authoritative sources:**
- arXiv abstract pages for papers.
- GitHub repo pages (via `gh api` or WebFetch) for code.
- HuggingFace / OpenReview / NeurIPS / ACL Anthology / IEEE Xplore for venue confirmation.
- Project documentation sites (only as secondary corroboration).

**What counts as "verification failure" → drop:** any entry where the link 404s; the project is a thin reimplementation with no original contribution; the paper has been retracted or significantly contested; the project is essentially a fork claiming originality. Drops are recorded in the verification log so they don't get re-added by future expansion.

---

## 6. Risk log

| # | Risk | Mitigation |
|---|---|---|
| R1 | A wrong entry / wrong attribution under an academic identity is reputational damage. | Two-step verification per entry; verification log; weekly CI link-check; pre-launch hostile review (Phase 6). |
| R2 | Honest annotation can read as unfair to a named project's authors. | Annotation rules in §4 are strict on "describe, don't accuse"; cite the project's own statements; route any criticism through *what a careful reader should verify themselves*, not *what the authors got wrong*. |
| R3 | Pure curated lists tend to spike on launch then plateau, undermining the 90-day growth goal. | Companion-launch coupling with a working repo (see `docs/LAUNCH.md`); the `docs/methodology.md` teaching section turns the repo into a shareable artifact in its own right and seeds long-tail SEO. |
| R4 | The list duplicates existing competitors (notably Sasha-Cui's and DataArcTech's). | Explicit IN/OUT scope (LLM trading agents specifically, not all FinLLMs nor all AI-in-finance); engineering frameworks + benchmarks + datasets, not paper-only; honest annotations; methodology section; link competitors generously in §9. |
| R5 | LLM-trading is a hype zone — readers expect the curator to recommend get-rich code. | Top-of-README disclaimer block (this is a research map, not financial advice); methodology section emphasises why most published results don't survive contact with live markets. |
| R6 | Entries decay (stars change, repos go unmaintained, papers get revised). | Weekly automated link-check; quarterly manual review cadence documented in `CONTRIBUTING.md`; star/citation numbers always labelled "as of YYYY-MM". |
| R7 | Scale-creep: trying to cover all of AI-in-finance instead of LLM trading agents. | Scope statement enforced by `validate_entries.py` (entries declare which of the 8 categories they live in; cross-cutting tags allowed but the entry must justify the primary category). |

---

## 7. Open questions (assumptions logged for autonomous execution)

The execution prompt says "work without stopping for clarifying questions". The following defaults are assumed; flag any in the closing report so the user can override.

1. **Curator naming.** Display Betty Guo (Dongxin Guo) with HKU + Prof. Siu-Ming Yiu affiliation and ORCID 0009-0000-2388-1072. **Assumption:** display name is "Betty Guo (Dongxin Guo)", advisor name is shown.
2. **License.** CC0 for the list content, MIT for the tooling code (`tools/`). **Assumption:** apply both via two LICENSE files at the repo root: `LICENSE` (MIT for code) and `LICENSE-list` (CC0 for entries). Cross-reference in README.
3. **Launch target size.** Aim for **~140 verified entries** as the launch target — comfortably inside the 100–200 band and leaves headroom for community contributions.
4. **Hero banner.** Lightweight SVG / text-based banner in `assets/` — no AI-generated imagery to avoid licensing ambiguity.
5. **Companion repo.** `agent-backtest-lab` is mentioned but does not yet exist in this directory. Treat as external; cross-link in `docs/LAUNCH.md` but do not block on its readiness.
6. **CI scheduler.** Weekly link-check via GitHub Actions `schedule: cron`. Tools must run on Python 3.11+ and need only stdlib + `requests` + `pyyaml`.
7. **Entry source format.** YAML, one file per entry under `entries/<category>/<slug>.yaml` — easier diff-review for PRs than a single mega-file.
8. **Verification log granularity.** One Markdown table per category, with one row per entry: slug, status, source URL, verified-on date, notes / drop reason if applicable.

---

## 8. Strategic positioning (one paragraph)

The LLM-trading-agent category has critical mass (a 73k-star anchor framework, multiple NeurIPS/ICLR/ACL papers, a maturing benchmark ecosystem) and an obvious gap: a comprehensive, verified, honestly-annotated map that distinguishes the methodologically serious from the aspirational, and teaches readers to make that distinction themselves. The 73k-star anchor supplies traffic gravity; the methodology section supplies a reason to stay and to share. The closest competitor (Sasha-Cui) is paper-only, uncritical, and ~80 entries. We ship at ~140 entries with engineering + research + evaluation coverage and a teaching layer, then ride the category.

---

*End of Phase 0.*
