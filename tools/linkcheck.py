#!/usr/bin/env python3
"""Verify every URL in entries/**/*.yaml resolves.

Exit code 0 if every verified entry's URL returns 2xx/3xx; 1 otherwise.
Pending and dropped entries are checked but do not fail the run.
"""
from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES = REPO_ROOT / "entries"

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 15
RETRIES_ON_5XX = 1
HEADERS = {
    "User-Agent": "awesome-llm-trading-agents linkcheck/1.0 (+https://github.com/bettyguo/awesome-llm-trading-agents)",
    "Accept": "*/*",
}


def collect_urls() -> list[dict]:
    items: list[dict] = []
    for path in sorted(ENTRIES.rglob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not data:
            continue
        slug = data.get("slug", path.stem)
        status = data.get("verification", {}).get("status", "pending")
        urls: list[str] = []
        if isinstance(data.get("url"), str):
            urls.append(data["url"])
        if isinstance(data.get("paper_url"), str):
            urls.append(data["paper_url"])
        for s in data.get("verification", {}).get("sources") or []:
            if isinstance(s, str):
                urls.append(s)
        seen = set()
        for u in urls:
            if u in seen:
                continue
            seen.add(u)
            items.append({"slug": slug, "url": u, "status": status})
    return items


def check_one(url: str) -> tuple[int | None, int, str]:
    start = time.time()
    try:
        r = requests.head(url, allow_redirects=True, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), headers=HEADERS)
        if r.status_code == 405 or r.status_code >= 500:
            for _ in range(RETRIES_ON_5XX + 1):
                r = requests.get(
                    url,
                    allow_redirects=True,
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                    headers=HEADERS,
                    stream=True,
                )
                if r.status_code < 500:
                    break
        return r.status_code, int((time.time() - start) * 1000), ""
    except requests.RequestException as e:
        return None, int((time.time() - start) * 1000), type(e).__name__


def main() -> int:
    items = collect_urls()
    print(f"Checking {len(items)} URL(s) across {len({i['slug'] for i in items})} entries...\n")
    print(f"{'status':>6}  {'latency':>7}  {'verif':>9}  url  [slug]")
    print("-" * 88)

    failures: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check_one, it["url"]): it for it in items}
        for fut in as_completed(futures):
            it = futures[fut]
            code, ms, err = fut.result()
            ok = code is not None and 200 <= code < 400
            mark = "OK" if ok else "FAIL"
            shown = f"{code}" if code is not None else err or "ERR"
            print(f"{shown:>6}  {ms:>5}ms  {it['status']:>9}  {it['url']}  [{it['slug']}]")
            if not ok:
                it_failed = dict(it)
                it_failed["code"] = code
                it_failed["error"] = err
                failures.append(it_failed)
                _ = mark  # for future structured output

    print("-" * 88)
    if failures:
        print(f"\n{len(failures)} failing URL(s):")
        verified_failures = [f for f in failures if f["status"] == "verified"]
        for f in failures:
            print(f"  {f['status']:>9}  {f['url']}  [{f['slug']}]  -> {f.get('code') or f.get('error')}")
        if verified_failures:
            print(f"\n{len(verified_failures)} of these belong to 'verified' entries — failing the run.")
            return 1
        print("All failures are on non-verified entries; not failing the run.")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
