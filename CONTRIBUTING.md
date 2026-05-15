# Contributing

Thanks for considering a contribution. The value of this list is **verification rigor + honest annotation**, so the contribution flow is built around those two things.

## Adding an entry

1. Pick the category. One of:
   - `01-frameworks` — multi-agent LLM trading frameworks
   - `02-single-agent` — single-agent / memory-augmented LLM traders
   - `03-papers` — foundational / influential papers, surveys, methodology
   - `04-datasets` — financial datasets
   - `05-benchmarks` — held-out evaluations
   - `06-backtesting` — backtesting & execution libraries
   - `07-simulators` — agent-based market simulators
   - `08-related-lists` — neighbouring awesome lists worth linking

2. Create `entries/<category>/<slug>.yaml`. The slug is lowercase-kebab and **must match** the filename. Copy the schema below.

3. Verify the entry. Open the canonical URL and at least one corroborating source (arXiv abstract page, NeurIPS / ACL / OpenReview page, project documentation). Both URLs go into `verification.sources`.

4. Write the honest note. Read [`docs/methodology.md`](docs/methodology.md) first if you haven't — the rules below are condensed from there.

5. Re-generate the README: `python tools/build_readme.py`. Commit both the entry and the README.

6. Run validation locally: `python tools/validate_entries.py` and (optional) `python tools/linkcheck.py`.

7. Open a PR using the template. CI will re-run the validators.

## Entry schema

```yaml
slug: my-entry                            # required, kebab-case, == filename stem
title: My Entry                           # required, official title
type: framework                           # required: framework | paper | dataset | benchmark | tool | environment | list
category: 01-frameworks                   # required, matches directory
subcategory: multi-agent                  # optional, free-form
url: https://github.com/org/repo          # required, canonical URL
paper_url: https://arxiv.org/abs/...      # optional
authors: [Author One, Author Two]         # required for papers; optional otherwise
maintainer: Org Name                      # optional, for repos
year: 2024                                # required for papers
venue: NeurIPS 2024                       # optional but recommended for papers
metrics:                                  # optional
  stars: 1234
  citations: 56
  as_of: "2026-05"
description: >-                          # required, one factual sentence
  Short neutral description of what it is.
note: >-                                  # required, the honest note (1–3 sentences)
  Factual description of what the project's own evaluation shows, plus what a careful
  reader should independently verify.
tags: [multi-agent, stocks]               # optional
verification:
  status: verified                        # verified | pending | dropped
  sources:                                # required for verified entries (>= 1)
    - https://arxiv.org/abs/...
    - https://github.com/org/repo
  verified_on: "2026-05-14"
  notes: null                             # populated only on drop/pending
```

## Rules for the "honest note"

The note is the single most important field. Read these carefully.

1. **Factual.** Describe what the project / paper *is* and what its own evaluation *demonstrates*. If you say "the paper reports X", X should appear in the paper.
2. **Fair.** Describe limitations a careful reader would notice — small universes, short evaluation windows, missing transaction costs, training-cutoff bleed, lack of buy-and-hold comparison. Do **not** assert that the authors mishandled anything or imply dishonesty / incompetence.
3. **Non-promotional.** No "revolutionary", "state-of-the-art", "groundbreaking", "cutting-edge", "world-class". The validator warns on these.
4. **Not advice.** No "buy", "sell", "you should invest". The validator warns on these.
5. **Route critique through the reader.** Phrasing template: *"As with any 2024–25 LLM trading study, readers should independently check {specific risk}."* The risk is named; the authors are not impugned.

## What gets rejected

- Self-promotion entries written by the author of the project without a credible note. (Self-promotion is fine; uncritical self-promotion is not.)
- Entries that re-add a project marked `dropped` in [`PLANNING/02_verification_log.md`](PLANNING/02_verification_log.md) without addressing the reason for the drop.
- Entries with broken canonical URLs or unverifiable claims.
- Entries that drift outside scope (see the README scope statement). Borderline entries can be discussed in the PR.

## Reviewing other people's entries

Apply the same rules to others' contributions that you would want applied to yours. If a note is too credulous, suggest a more skeptical phrasing in a PR review comment; if a note is unfairly harsh on a named project, suggest a more measured one. The standard is *the careful, fair, evidence-based reader*.
