# Verification log

> Every entry in `entries/**/*.yaml` is recorded here with its verification outcome.
> `verified` = both the canonical URL and at least one corroborating source were retrieved and the claims in the description / note were checked against the source. `pending` = staged, needs human review before merge. `dropped` = previously considered but rejected; do not re-add without addressing the reason.

The Phase 0 web research was the primary verification pass; sources for each entry are recorded in the entry's `verification.sources` field. This log is the human-readable summary.

## Phase 2 seed — verified entries (n = 36)

### 01-frameworks
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| tradingagents | arXiv 2412.20138 (v7, 2025-06-03); github.com/TauricResearch/TradingAgents | 2026-05-14 | 73.7k★ as of search; authors Xiao/Sun/Luo/Wang confirmed against arXiv abstract page |
| finrobot | github.com/AI4Finance-Foundation/FinRobot; AI4Finance org page | 2026-05-14 | Active AI4Finance Foundation maintenance; platform-style, not single-purpose agent |
| quantagent | github.com/Y-Research-SBU/QuantAgent; y-research-sbu.github.io/QuantAgent | 2026-05-14 | Authors Xiong/Zhang/Feng/Sun/You confirmed; HFT framing per project page |
| stockagent | github.com/MingyuJ666/Stockagent; ResearchGate publication record | 2026-05-14 | Simulated-market caveat called out in note |
| fingpt | github.com/AI4Finance-Foundation/FinGPT; FinNLP project page | 2026-05-14 | Re-categorised as FinLLM tooling, not standalone trading agent |

### 02-single-agent
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| finmem | arXiv 2311.13743; github.com/pipiku915/FinMem-LLM-StockTrading; OpenReview | 2026-05-14 | Authors per arXiv abstract page; ICLR workshop confirmed |
| fin-r1 | arXiv 2503.16252; github.com/SUFE-AIFLM-Lab/Fin-R1; HF papers | 2026-05-14 | Category-error caveat (reasoning ≠ trading) emphasised in note |
| finrl | arXiv 2011.09607; github.com/AI4Finance-Foundation/FinRL; FinRL docs | 2026-05-14 | NeurIPS 2020 DRL workshop; RL baseline not LLM agent |
| qlib | github.com/microsoft/qlib | 2026-05-14 | Microsoft ownership; ML platform, not LLM agent |

### 03-papers
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| fincon | arXiv 2407.06567; OpenReview dG1HwKMYbC; NeurIPS 2024 proceedings PDF | 2026-05-14 | Authors trimmed from publication record |
| finagent | arXiv 2402.18485; ideas.repec.org alt index | 2026-05-14 | Multimodal foundation-agent framing |
| alphaagents | arXiv 2508.11152; emergentmind paper page | 2026-05-14 | Portfolio construction focus |
| lookahead-bias-llm-forecasts | arXiv 2512.23847 | 2026-05-14 | Methodology paper — LAP test |
| llm-lookahead-solution | arXiv 2512.06607 | 2026-05-14 | Companion mitigation paper |
| llm-investing-longrun | arXiv 2505.07078 | 2026-05-14 | Long-horizon test of LLM strategies |
| probability-backtest-overfitting | SSRN 2326253 | 2026-05-14 | López de Prado et al. — JCF |
| deflated-sharpe-ratio | SSRN 2460551; davidhbailey.com PDF | 2026-05-14 | Bailey & López de Prado — JPM |

### 04-datasets
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| pixiu-flare | arXiv 2306.05443; github.com/The-FinAI/PIXIU; OpenReview | 2026-05-14 | NeurIPS 2023 D&B; authors from publication record |
| fin-r1-data | github.com/SUFE-AIFLM-Lab/Fin-R1; arXiv 2503.16252 | 2026-05-14 | Released with Fin-R1 model |

### 05-benchmarks
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| stockbench | arXiv 2510.02209; OpenReview 9tFRj7cmrS | 2026-05-14 | Contamination-controlled live trading 2025-03-03–2025-06-30 |
| agent-market-arena | arXiv 2510.11695; moonlight review | 2026-05-14 | Architecture-vs-backbone finding flagged as a strong claim |
| investorbench | arXiv 2412.18174; ACL 2025 anthology | 2026-05-14 | First explicit LLM-agent decision-making benchmark |
| finben | arXiv 2402.12659; thefin.ai; NeurIPS 2024 D&B poster page | 2026-05-14 | 42 datasets / 24 tasks / 8 aspects |
| financebench | arXiv 2311.11944; emergentmind | 2026-05-14 | Patronus AI; QA-only, not trading |

### 06-backtesting
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| backtrader | github.com/mementum/backtrader | 2026-05-14 | Maintenance-quiet; community-supported |
| zipline-reloaded | github.com/stefan-jansen/zipline-reloaded | 2026-05-14 | Active fork of Quantopian Zipline |
| vectorbt | github.com/polakowo/vectorbt | 2026-05-14 | Vectorised; PRO variant exists commercially — we list the OSS edition |
| nautilus-trader | github.com/nautechsystems/nautilus_trader | 2026-05-14 | Rust core + Python API |
| backtesting-py | github.com/kernc/backtesting.py | 2026-05-14 | Lightweight single-asset |

### 07-simulators
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| abides | github.com/jpmorganchase/abides-jpmc-public; NSF par.nsf.gov PDF | 2026-05-14 | JPM AI Research; three-package split (Core/Markets/Gym) |

### 08-related-lists
| Slug | Sources | Verified | Notes |
|---|---|---|---|
| awesome-applied-agents-investment | github.com/Sasha-Cui/Awesome-Applied-Agents-for-Investment | 2026-05-14 | Closest neighbour; paper-only |
| awesome-ai-in-finance | github.com/georgezouq/awesome-ai-in-finance | 2026-05-14 | Parent category (AI in finance generally) |
| awesome-finllms | github.com/DataArcTech/Awesome-FinLLMs | 2026-05-14 | Bilingual EN/中 FinLLM list |
| awesome-llm-powered-agent | github.com/hyp1231/awesome-llm-powered-agent | 2026-05-14 | Grandparent category (LLM agents generally) |
| awesome-quant | github.com/wilsonfreitas/awesome-quant | 2026-05-14 | Plumbing-layer reference |

## Dropped (n = 0 in Phase 2)

None yet. Candidates for Phase 3 drop review: any project whose canonical URL 404s, any preprint with no public code 12+ months after submission and no follow-up, and any project that turns out to be a thin wrapper of an entry already on the list.

## Pending (carry-over candidates for Phase 3)

These were considered during Phase 0 research and warrant inclusion if the verification pass passes:
- **FinCon code release** — check whether the NeurIPS 2024 paper has an open-source code repository (paper currently links elsewhere).
- **AlphaForge** (alpha factor discovery framework) — cited by adjacent work, repo to verify.
- **Agentar-Fin-R1** (arXiv 2507.16802) — domain-expert refinement of Fin-R1.
- **Fino1** (github.com/The-FinAI/Fino1) — transferability of reasoning-enhanced LLMs to finance.
- **FNSPID** (financial news + price dataset) — large-scale.
- **TradingGoose** (multi-agent framework spotted in search results).
- **MarketsAgent / TradingGPT / Stock-LLM variants** — verify each individually.
- **FinR1 / Fino1 / Agentar-Fin-R1 lineage** as a separate "reasoning-LLM finance models" sub-section.
- **MarketSim / ICAIF24 market simulators** — agent-based simulators newer than ABIDES.
- **OpenBB** — open-source investment-research platform increasingly used as an LLM-agent data layer.
- **Bloomberg-GPT paper** — historical reference, even though closed-weight.
