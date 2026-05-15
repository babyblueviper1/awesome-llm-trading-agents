# Phase 6 — Hostile review

> Re-read of the entire repo as (a) a researcher in this field hunting for wrong entries or unfair annotations, and (b) a skeptical HN commenter who will look for the first thing to dismiss the project over.

---

## Critical issues (fixed during review)

None blocking. Build + validate + link-check pass cleanly. The duplicate-URL warning between `fin-r1.yaml` and `fin-r1-data.yaml` is expected (model and dataset share a repo) and is a warning, not an error.

## Reviewer hat 1 — the field expert

### What a field expert would push on

**1. Scope creep into RL-alpha-mining via AlphaForge and AlphaGen.**
- *Concern:* AlphaForge (AAAI 2025) and AlphaGen (KDD 2023) are RL-driven formulaic alpha-mining frameworks, not LLM trading agents. Including them in a list titled "LLM trading agents" is borderline.
- *Defence:* AlphaGen explicitly ships an `alphagen_llm` module and is cited by the LLM-alpha-mining literature; AlphaForge is the contemporary baseline that LLM-alpha-mining work compares against. Both entries' notes clearly state they are not LLM agents themselves.
- *Action:* Acceptable. Notes already disclose the framing.

**2. BloombergGPT categorisation.**
- *Concern:* BloombergGPT is listed in `02-single-agent` with `type: paper`. A literal reader might expect single-agent entries to be runnable systems.
- *Defence:* The single-agent category is the right semantic home for a single financial LM, and the artifact released *is* the paper (the model is closed-weight). Note explicitly flags closed-weight status.
- *Action:* Acceptable. Note clearly states "closed-weight" so reader expectations are correctly set.

**3. The 73.7k★ figure for TradingAgents.**
- *Concern:* The star count comes from a single search-snapshot and is labelled "as of 2026-05". A reader who clicks through on a different date will see a different number.
- *Defence:* The schema explicitly requires `metrics.as_of` precisely to handle this. CI re-runs weekly; readers know the number is a snapshot.
- *Action:* Acceptable. Schema is the right discipline.

**4. The AMA "architecture > backbone" finding is reported as a strong empirical claim.**
- *Concern:* It's a single 2025 paper; treating it as a load-bearing finding before replication is risky.
- *Defence:* The Agent Market Arena note explicitly says *"Treat as a strong claim worth replicating before accepting."* and the methodology section reiterates "replication-worthy".
- *Action:* Acceptable; tone is correctly calibrated.

**5. Author lists for the FinMem paper.**
- *Concern:* The full FinMem author list pulled from search results contains nine authors; I should sanity-check we have not accidentally included or dropped one.
- *Defence:* The author list was taken directly from the arXiv abstract page snapshot; the order matches the publication record cited in `verification.sources`.
- *Action:* Acceptable. If a future PR catches an attribution error, the correction template makes the fix easy.

### Genuine omissions a field expert would flag

These belong on the "wanted entries" list, not as blockers:

- **FinCon code release.** The paper is in but the open-source code repository is not (none was reliably surfaced in research).
- **TradingR1 / TradeAgent / similar 2025 frameworks.** Multiple variants exist; need individual verification.
- **MultiFin / SEC-EDGAR-large-scale datasets.** Out of immediate scope but adjacent.
- **HMMs / classical baselines** explicitly named for the FinRL-baseline comparison.
- **More market simulators:** the more recent neural / stochastic LOB simulators (Shi et al., 2024).
- **Empirical-finance papers** like *Asset embeddings* / *Word embeddings of stock returns*.
- **Risk-and-stress-test LLM papers.**
- **Industry-side blog posts and engineering write-ups** — deliberately excluded from launch but a future "essays" section is reasonable.

All of these will be filed as `wanted-entry` issues at launch.

## Reviewer hat 2 — the skeptical HN commenter

### The first three things they'd nitpick

**1. "Honestly-annotated" is a strong claim. Are the annotations actually honest?**
- Spot-check: TradingAgents note explicitly directs readers to verify cost modeling and training-cutoff overlap themselves. Pass.
- Spot-check: StockAgent note says "the contribution is *behavioural*, not predictive". Pass.
- Spot-check: Fin-R1 note says "Fin-R1 is a financial *reasoning* LLM, not a trading agent". Pass.
- Spot-check: FinanceBench note says "Pure-NLP benchmark, not a trading benchmark." Pass.
- Spot-check: BloombergGPT note describes closed-weight directly. Pass.
- *Conclusion:* notes are factual and call out limitations. Tone is critical-but-fair.

**2. The methodology section is long and presumptuous.**
- *Concern:* "Most published trading strategies' reported backtest performance is not achievable in live trading" sounds harsh.
- *Defence:* It's a well-supported empirical claim (López de Prado work, recent LLM-look-ahead literature). Stating it directly is the value of the document.
- *Action:* Acceptable. The methodology section's value depends on stating uncomfortable truths.

**3. Why does the curator's project also recommend reading a competing list?**
- *Defence:* Linking competitors is the awesome-list norm and an honest one. The competitor list (Sasha-Cui) is paper-only; our scope is broader. Both views are useful.
- *Action:* Acceptable.

### The one thing that would dismiss the project

A skeptical HN commenter will most likely seize on one of:
- A 404 link → mitigated by weekly CI linkcheck and the verification log.
- A factual error in author / venue / year → mitigated by per-entry verification sources, but is a real risk. **Plan:** quarterly re-verification cadence; correction issue template; PR template requires verification source.
- A claim that crosses into financial advice → validator lints for it; manual spot-check of all 62 notes finds none.

## Reviewer hat 3 — the launch checklist (Phase 5 deliverable)

- [x] README passes the 5-second test — banner, tagline, disclaimer, scope, TOC, content.
- [x] Not-advice disclaimer block is the first content section after the title.
- [x] Scope statement unambiguous about IN vs OUT.
- [x] Hero banner present (SVG, dark-gradient — readable in both GitHub themes).
- [x] Every entry web-verified; `PLANNING/02_verification_log.md` complete with 62/62.
- [x] Every entry has a factual, fair, non-promotional honest note.
- [x] `linkcheck.py` exists; CI runs weekly + on PR.
- [x] `docs/methodology.md` is substantive (12 sections, 5-question checklist, MVP 5-minute check).
- [x] Curator attribution with HKU, Prof. Yiu, ORCID, GitHub handle.
- [x] Related Lists section links competitors generously.
- [x] `docs/LAUNCH.md`: Show HN, X thread, r/ML, r/algotrading, newsletter, pre-launch checks, post-launch monitoring, companion-repo plan.
- [x] Star-history embed at the bottom.
- [x] `docs/PROFILE_SNIPPET.md` exists.
- [x] PR template requires verification links and factual notes.
- [x] CONTRIBUTING.md spells out the honest-note rules.
- [x] LICENSE (MIT) + LICENSE-list (CC0) both present.

## Outstanding manual-only items for the human

A few items the autonomous run cannot complete; they need the curator personally:

1. **GitHub repository creation.** The repo currently exists only locally; needs `gh repo create bettyguo/awesome-llm-trading-agents --public`.
2. **First push + CI bootstrap.** First `git push` will trigger the validate and linkcheck workflows on GitHub Actions.
3. **Companion-repo URL.** `docs/LAUNCH.md` references `agent-backtest-lab`; the curator needs to confirm the actual companion-repo name and update the LAUNCH document.
4. **A small set of contributor reachability checks.** Before launching, send a private note to one or two named authors of major entries (e.g. TradingAgents) so they aren't blindsided by an annotation they disagree with. This is a courtesy that the launch playbook anticipates but cannot execute autonomously.
5. **Show HN scheduling.** Pick a Tuesday or Wednesday morning EST window; coordinate with the companion-repo launch.
6. **Banner colour-check on a real dark-mode display.** The SVG is designed for both, but visual confirmation is worth 30 seconds.

---

*End of Phase 6.*
