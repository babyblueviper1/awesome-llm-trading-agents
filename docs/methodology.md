# Methodology & Common Pitfalls

> How to read any project on this list — and any new one you encounter — without being misled.
>
> This is the section that turns this repository from a list into a teaching resource. It is intentionally long. Most of the field's headline results die when one of the pitfalls below is corrected for. If you only read one section, read [§2](#2-look-ahead-bias-and-the-llm-specific-variant) and [§5](#5-the-five-questions-checklist).

---

## Reading paths

- **First-time reader:** §1 → §2 → §5 → §11.
- **You want to evaluate a specific repo or paper on this list:** §5 (the checklist) → drill into whichever of §2–§9 the project's claims expose it to.
- **You are *building* an LLM trading agent:** the whole document, in order.
- **You are a reviewer for a venue:** §2 → §4 → §6 → §8 → §9.

---

## 1. The shape of the problem

Trading is an unusually hostile environment for ML claims:

- **Non-stationary.** The data-generating process moves; what worked in 2018 stops working in 2022 stops working in 2025. The same model on the same market can have wildly different live performance depending on regime.
- **Adversarial.** Other participants react to and price out any edge you discover. A *publicly-described* edge has a half-life. A *privately-deployed* edge has a longer half-life but is also subject to capacity decay as you trade it.
- **Low signal-to-noise.** Daily return innovations are dominated by idiosyncratic noise; a strategy with a true Sharpe of 0.5 is hard to distinguish from one with a true Sharpe of 0 over fewer than 1,000 trading days.
- **High dimensionality of the strategy space.** Modern stacks let you try millions of strategy variants. The multiple-testing problem is severe and rarely accounted for honestly. (See [Probability of Backtest Overfitting](../entries/03-papers/probability-backtest-overfitting.yaml).)
- **Layered cost structure.** Spreads, fees, market impact, slippage, financing, taxes. A backtest reporting gross return is reporting a number that cannot be earned.

The cumulative effect is that **most published trading strategies' reported backtest performance is not achievable in live trading**. This is not a slur against any particular project; it is a statistical fact about the regime. Your default prior on any new strategy's claimed Sharpe should be skeptical, and the prior tightens as the claim grows.

---

## 2. Look-ahead bias and the LLM-specific variant

**Classic look-ahead bias:** the model sees information at decision time *t* that, in live trading, would not have been available until *t + δ*. Common causes:

- Restated or revised data (fundamentals, earnings) joined back in time without point-in-time-correct snapshots.
- Forward-fill of a missing value with a value that was later observed.
- Survivorship-biased universes (today's S&P 500 backtested over a 20-year window in which several index members did not exist).
- Cross-sectional ranks computed using close-of-day data and then traded on the same day's close.

**LLM-specific look-ahead bias** is more insidious and is the single most underrated failure mode in this category:

> *A frontier LLM's weights were trained on text through some cutoff date C. When you backtest the LLM on data from before C, the LLM is being evaluated on what it already, in some sense, knows. "Predicting" Apple's Q3 2022 earnings using GPT-4 (training cutoff late 2023) is not prediction — it is, at worst, recall.*

The cleanest evidence for this comes from arXiv 2512.23847 ([entry](../entries/03-papers/lookahead-bias-llm-forecasts.yaml)), which finds that LLMs' apparent predictive power on news-headline-→-return and earnings-call-→-capex tasks partly reflects memorization. Mitigations exist (arXiv 2512.06607, [entry](../entries/03-papers/llm-lookahead-solution.yaml)), but the burden of proof is on the project, not the reader.

**Checklist for LLM look-ahead bias:**

- [ ] Is every evaluation timestamp *strictly after* the backbone LLM's training cutoff? (Check the model card.)
- [ ] Does the prompt include any element — a date, a ticker's full corporate history, an analyst's by-name attribution — that a date-blinded model couldn't have known at time *t*?
- [ ] If the paper claims to use older data, did it use the LAP-style test (or a comparable randomisation) to detect memorisation?
- [ ] Did the project also report results on a clean post-cutoff window, however short?

The cleanest single mitigation is to evaluate on a window that *starts after* the backbone's training cutoff. [StockBench](../entries/05-benchmarks/stockbench.yaml) does this explicitly. Few other benchmarks do.

---

## 3. Backtest overfitting and the multiple-testing problem

The "I tried 1,000 prompts and reported the best Sharpe" workflow is exactly the workflow that López de Prado & Bailey formalised as **the probability of backtest overfitting**. The intuition:

> *In an exhaustive search over N strategy variants on a fixed in-sample dataset, the in-sample-best variant has out-of-sample performance close to the median of all variants — not the best.*

The Sharpe ratio you report after selecting from N trials is **not** an unbiased estimator of the true Sharpe. It is the maximum of N draws and is biased upward by a factor that grows with N.

**Practical implications for LLM trading agents:**

- Every prompt-engineering iteration is a trial. If you iterated on the prompt 30 times and reported the best one, you ran 30 trials.
- Every hyperparameter sweep is a trial.
- Every "we tried tool A, tool B, and tool C; tool C worked best" is three trials.
- Every backtest window you peeked at is a trial.

**Mitigations:**

- **Deflated Sharpe Ratio** (DSR). Reports the Sharpe net of selection bias and non-normality. [Entry](../entries/03-papers/deflated-sharpe-ratio.yaml).
- **Combinatorial Purged Cross-Validation** (CPCV). The standard time-series-aware CV for finance. Provides a *distribution* of out-of-sample Sharpes rather than one. Implementations: [skfolio](../entries/06-backtesting/skfolio.yaml) (`CombinatorialPurgedCV`).
- **Strict pre-registration.** Decide the strategy spec, the evaluation window, the metrics, and the buy/sell rules *before* seeing any out-of-sample data. The discipline is hard.

When a paper reports a single Sharpe with no trial count and no DSR, you are looking at the best of an unknown number of draws.

---

## 4. Train / test / live: the three different things people call "out-of-sample"

The most-overloaded term in this field. Distinguish carefully:

1. **In-sample.** The data the model saw during training (LLM pre-training, fine-tuning, or both). For frontier LLMs, this is "everything up to the cutoff".
2. **Held-out (researcher-determined).** A slice of data the researcher decided to hold out. Useful for hyperparameter selection. **Not** a substitute for out-of-sample.
3. **Out-of-sample (time-forward).** A window that *strictly post-dates* both (a) any data used for training the model, and (b) any decision made by the researcher. The only kind that matters.
4. **Live / paper-traded.** Real or paper-trading execution against a real exchange feed with realistic latency and order types. The only kind that is fully honest about every implementation detail.

Most LLM-trading papers report on type 2 and call it "out-of-sample". Read carefully: type 2 with an LLM is essentially in-sample because the LLM saw the data during pre-training. Insist on type 3 — and prefer type 4 when possible.

---

## 5. The five questions checklist

When you encounter a new project on this list (or anywhere else), ask these five questions before forming an opinion:

### Q1. What window did they evaluate on, and does it post-date the backbone LLM's training cutoff?

If no, the result may reflect memorisation. If yes, how long is the window? Sub-six-month windows are vulnerable to regime luck.

### Q2. How many trials did they implicitly run, and is the reported Sharpe deflated?

If no trial count: ask. If no DSR: discount the headline Sharpe by ~30% as a rough rule of thumb (the exact discount depends on the trial count; see [Bailey & López de Prado](../entries/03-papers/deflated-sharpe-ratio.yaml)).

### Q3. What baseline are they comparing to, and does it include buy-and-hold?

"Beats GPT-3.5 baseline" is not a meaningful comparison for trading. "Beats buy-and-hold of the same universe over the same window with the same costs" is.

### Q4. Are transaction costs and market impact modelled?

A backtest reporting *gross* returns is reporting an unattainable number. The cost discount on real strategies is 30–80% of gross alpha depending on turnover and capacity. If costs are not modelled, assume the realised Sharpe is roughly half the reported one.

### Q5. Is the universe and the time window large enough to be statistically meaningful?

A single stock over 60 trading days is a case study, not a backtest. Insist on a defensible universe (at least 50 names, ideally a recognisable index) and at least 250 trading days (one year). For "outperforms" claims, more is needed; the t-statistic on a Sharpe of 1.0 over 250 days is about 1.0.

---

## 6. The "compared to baseline" trap

A surprising number of papers in this list report wins over baselines that no serious trader would use:

- **GPT-3.5 single-prompt baselines** for a multi-agent system built around GPT-4. You learn that GPT-4 multi-agent > GPT-3.5 single-agent. You do not learn that the *architecture* helped.
- **Untuned RL baselines** for an LLM agent. You learn that an untuned baseline is bad. Compare to *tuned* PPO/SAC ([FinRL](../entries/02-single-agent/finrl.yaml) provides this).
- **No buy-and-hold.** The simplest baseline of all. [StockBench](../entries/05-benchmarks/stockbench.yaml) reports that most LLM agents in fact fail to beat it.

The credible architectural-contribution claim is: *the multi-agent decomposition outperforms the same LLM in a single-prompt configuration on the same task with the same data*. [Agent Market Arena](../entries/05-benchmarks/agent-market-arena.yaml) reports that **agent architecture, not backbone choice, dominates profitability** — but this is one paper and replication is warranted before treating it as load-bearing.

---

## 7. Survivorship and selection biases in the universe

The universe you backtest on changes over time:

- Index constituents are added and removed.
- Companies are acquired, delisted, or go bankrupt.
- Datasets (e.g. KOSPI200 in 2010, S&P500 in 2024) silently drift.

Backtesting today's S&P 500 from 2010 to 2025 omits every company that fell out of the index — a survivorship-biased universe that systematically inflates returns. The fix is **point-in-time universe** snapshots, which most public datasets do not provide. [Qlib](../entries/02-single-agent/qlib.yaml) and a few commercial providers offer them.

For LLM agents reading news and filings, there is an additional selection bias: the *body of text the LLM was pre-trained on* is itself biased — survivors leave more documentary trail. The LLM may "know" things about today's surviving constituents that it does not "know" about delisted companies, and your evaluation on a survivorship-biased universe interacts with this in subtle ways.

---

## 8. Capacity and market impact

A strategy with a reported Sharpe of 3 on $10M of equity may have a Sharpe of 0.5 on $1B and a Sharpe of -0.5 on $10B. Capacity is the dollar size at which the strategy stops working — its market impact begins to consume the alpha.

Most LLM trading papers do not discuss capacity. The implicit assumption is that the strategy is run at a size at which it does not move the market. For backtest claims to be informative about live deployment, this assumption needs to be either modelled (with a fill-impact model) or explicit (the paper says "this strategy is capacity-limited to $X").

Capacity scales roughly with: market depth × frequency of rebalance × √strategy edge. LLM-decided strategies on daily-bar S&P 500 names are typically capacity-rich. LLM-decided HFT strategies (per [QuantAgent](../entries/01-frameworks/quantagent.yaml)) are capacity-constrained and are also operationally constrained by inference latency.

---

## 9. Reproducibility checklist for LLM agents

LLMs introduce reproducibility risks that classical ML did not:

- **Closed-weight backbones.** A paper relying on `gpt-4-2024-08` is irreproducible the day the snapshot is deprecated. Prefer open-weight baselines, or at minimum a version-pinned snapshot you can re-call.
- **Non-zero temperature.** Many LLM-agent papers use sampling. Reproducibility requires a fixed seed and a deterministic backend; some providers do not offer one. Run a sensitivity analysis.
- **Prompt drift.** Subtle prompt edits change outputs materially. Pin and version-control prompts as carefully as code.
- **Tool-call versions.** A "search the web" tool that calls a particular Bing index in 2024 returns different content in 2026.

Treat any LLM agent paper without a pinned model version, fixed temperature, version-controlled prompts, and frozen tool responses as a *demonstration*, not a *replicable claim*.

---

## 10. What a credible evaluation looks like

A trading-agent paper that takes evaluation seriously typically has all of the following:

1. **Post-cutoff window.** Evaluation strictly after the backbone LLM's training data.
2. **Defensible universe.** At least 50 names, recognisable construction (point-in-time index or a published rule).
3. **Sufficient horizon.** At least 250 trading days, ideally several years.
4. **Honest baselines.** Buy-and-hold and a tuned RL agent at minimum; ideally also a single-prompt LLM and a no-LLM factor model.
5. **Transaction costs.** A specified, defensible cost model.
6. **Multiple-testing correction.** DSR, or a pre-registered single trial.
7. **Time-series CV.** CPCV or walk-forward, with purging and embargoing.
8. **Reproducibility.** Pinned model, pinned prompts, fixed seeds, archived tool responses.
9. **Discussion of capacity.** At least a sentence.
10. **A null result somewhere.** Real evaluations have things that didn't work. Papers in which everything works are suspicious.

You will find very few projects on this list that satisfy *all ten*. That is not an indictment of the projects; it is a characterisation of the state of the field.

---

## 11. The minimal viable check (for the reader in a hurry)

If you only have five minutes to evaluate a project, do this:

1. **Open the project's evaluation section.** What window did they use?
2. **Subtract the backbone LLM's training cutoff** from the *start* of that window. If the difference is negative or near zero, downgrade your confidence sharply.
3. **Search the paper or README for "transaction cost" / "fee" / "slippage".** If absent, halve the headline Sharpe.
4. **Search for "buy-and-hold" or "B&H".** If absent, halve again.
5. **Check the universe size and horizon** against §5 Q5.

After this five-minute pass, you will have a calibrated view of whether the project's headline claim is robust, partially robust, or aspirational. Most fall in the second category; some fall in the third. Very few are unconditionally robust.

---

## 12. A note on tone

This document is skeptical because the field invites skepticism. It is not hostile to any project on the list. Almost every paper and repo here is doing serious work and contributing knowledge — the discipline of asking the right questions is what separates "this project is interesting" from "this project's backtest is bankable."

If you are an author of a project on this list and feel an entry's note is unfair, open an issue with the specific claim and evidence; the note will be revised. If you are a reader who feels we have been too generous to a project, do the same.

---

## Further reading (the methodology canon)

In order of how useful they are to the LLM-trading-agent reader:

1. *The Probability of Backtest Overfitting* — Bailey, Borwein, López de Prado, Zhu. [Entry](../entries/03-papers/probability-backtest-overfitting.yaml).
2. *The Deflated Sharpe Ratio* — Bailey & López de Prado. [Entry](../entries/03-papers/deflated-sharpe-ratio.yaml).
3. *A Test of Lookahead Bias in LLM Forecasts* — arXiv 2512.23847. [Entry](../entries/03-papers/lookahead-bias-llm-forecasts.yaml).
4. *A Fast and Effective Solution to Look-ahead Bias in LLMs* — arXiv 2512.06607. [Entry](../entries/03-papers/llm-lookahead-solution.yaml).
5. *Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?* — arXiv 2505.07078. [Entry](../entries/03-papers/llm-investing-longrun.yaml).
6. *StockBench: Can LLM Agents Trade Stocks Profitably In Real-world Markets?* — arXiv 2510.02209. [Entry](../entries/05-benchmarks/stockbench.yaml).

If you take one thing from this document: **the question is not "did this LLM agent's backtest beat the benchmark?". The question is "would this LLM agent's backtest beat the benchmark if I corrected for everything above?"**. Almost always, the answer to the second question is much closer to zero than the headline number suggests.
