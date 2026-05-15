#!/usr/bin/env python3
"""Schema and quality validation for entries/**/*.yaml.

Exit code 0 = clean; 1 = at least one error (warnings do not fail CI).
"""
from __future__ import annotations

import io
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES = REPO_ROOT / "entries"

VALID_TYPES = {"framework", "paper", "dataset", "benchmark", "tool", "environment", "list"}
VALID_STATUSES = {"verified", "pending", "dropped"}
VALID_CATEGORIES = {
    "01-frameworks",
    "02-single-agent",
    "03-papers",
    "04-datasets",
    "05-benchmarks",
    "06-backtesting",
    "07-simulators",
    "08-related-lists",
}
REQUIRED_TOP = {"slug", "title", "type", "category", "url", "description", "note", "verification"}
REQUIRED_VERIF = {"status", "sources", "verified_on"}

MARKETING_WORDS = (
    "revolutionary",
    "state-of-the-art",
    "groundbreaking",
    "breakthrough",
    "cutting-edge",
    "world-class",
    "best-in-class",
)
# Advice-adjacent phrases — match as whole phrases, not substrings, because finance terms like
# "buy-and-hold", "sell-side", and "earnings beat" are legitimate technical vocabulary.
ADVICE_PHRASES = (
    r"\byou should (?:buy|sell|invest|short|long)\b",
    r"\b(?:guaranteed|risk[- ]free)\s+(?:return|profit|gain)s?\b",
    r"\b(?:get[- ]rich|easy money)\b",
)


def load_entries() -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    for path in sorted(ENTRIES.rglob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if data is None:
            continue
        out.append((path, data))
    return out


def validate_one(path: Path, data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = path.relative_to(REPO_ROOT).as_posix()

    missing = REQUIRED_TOP - data.keys()
    if missing:
        errors.append(f"{rel}: missing required keys: {sorted(missing)}")
        return errors, warnings

    if data["type"] not in VALID_TYPES:
        errors.append(f"{rel}: type '{data['type']}' not in {sorted(VALID_TYPES)}")
    if data["category"] not in VALID_CATEGORIES:
        errors.append(f"{rel}: category '{data['category']}' not in {sorted(VALID_CATEGORIES)}")
    parent_dir = path.parent.name
    if data["category"] != parent_dir:
        errors.append(f"{rel}: category '{data['category']}' != parent directory '{parent_dir}'")

    if data["slug"] != path.stem:
        errors.append(f"{rel}: slug '{data['slug']}' != filename stem '{path.stem}'")

    if not isinstance(data["url"], str) or not data["url"].startswith(("http://", "https://")):
        errors.append(f"{rel}: url must be an http(s) URL")

    verif = data["verification"]
    if not isinstance(verif, dict):
        errors.append(f"{rel}: verification must be a mapping")
        return errors, warnings
    vmissing = REQUIRED_VERIF - verif.keys()
    if vmissing:
        errors.append(f"{rel}: verification missing keys: {sorted(vmissing)}")
        return errors, warnings
    if verif["status"] not in VALID_STATUSES:
        errors.append(f"{rel}: verification.status '{verif['status']}' not in {sorted(VALID_STATUSES)}")
    if verif["status"] == "verified":
        if not isinstance(verif.get("sources"), list) or not verif["sources"]:
            errors.append(f"{rel}: verified entries require at least one verification.sources URL")

    note = str(data.get("note") or "")
    note_l = note.lower()
    for w in MARKETING_WORDS:
        if w in note_l:
            warnings.append(f"{rel}: marketing word '{w}' in note - reword to a factual description")
    for pat in ADVICE_PHRASES:
        if re.search(pat, note_l):
            warnings.append(f"{rel}: financial-advice phrase '{pat}' matched in note - strip it")

    desc = str(data.get("description") or "")
    if len(desc.split()) < 5:
        warnings.append(f"{rel}: description is very short (< 5 words)")
    if len(desc) > 400:
        warnings.append(f"{rel}: description > 400 chars; trim for table layout")
    if len(note) > 800:
        warnings.append(f"{rel}: note > 800 chars; trim to 1–3 sentences")

    return errors, warnings


def main() -> int:
    entries = load_entries()
    all_errors: list[str] = []
    all_warnings: list[str] = []

    slug_owner: dict[str, str] = {}
    url_owner: dict[str, str] = defaultdict(list)

    for path, data in entries:
        errs, warns = validate_one(path, data)
        all_errors.extend(errs)
        all_warnings.extend(warns)

        slug = data.get("slug")
        if isinstance(slug, str):
            if slug in slug_owner:
                all_errors.append(
                    f"{path.relative_to(REPO_ROOT)}: duplicate slug '{slug}' (also in {slug_owner[slug]})"
                )
            else:
                slug_owner[slug] = path.relative_to(REPO_ROOT).as_posix()

        url = data.get("url")
        if isinstance(url, str) and data.get("verification", {}).get("status") == "verified":
            url_owner[url].append(path.relative_to(REPO_ROOT).as_posix())

    for url, owners in url_owner.items():
        if len(owners) > 1:
            all_warnings.append(f"duplicate verified URL across entries: {url} → {owners}")

    print(f"Validated {len(entries)} entries.")
    if all_warnings:
        print(f"\n{len(all_warnings)} warning(s):")
        for w in all_warnings:
            print(f"  WARN  {w}")
    if all_errors:
        print(f"\n{len(all_errors)} error(s):")
        for e in all_errors:
            print(f"  ERROR {e}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
