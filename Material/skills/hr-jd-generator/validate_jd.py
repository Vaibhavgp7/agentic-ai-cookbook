#!/usr/bin/env python3
"""Lightweight JD draft checker for the hr-jd-generator skill."""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Job Title",
    "Company",
    "Role Overview",
    "Key Responsibilities",
    "Required Skills",
    "Preferred Skills",
    "Experience",
    "Location",
]

BIASED_TERMS = [
    "rockstar",
    "ninja",
    "guru",
    "young and energetic",
    "native english speaker",
    "iit-only",
    "tier-1 only",
    "culture fit",
]


def validate(text: str):
    errors = []

    for section in REQUIRED_SECTIONS:
        if section.lower() not in text.lower():
            errors.append(f"Missing section: {section}")

    lowered = text.lower()
    for term in BIASED_TERMS:
        if term in lowered:
            errors.append(f"Biased or non-inclusive term found: {term!r}")

    must_have = re.search(
        r"required skills|must-have", text, re.IGNORECASE
    )
    preferred = re.search(
        r"preferred skills|good-to-have", text, re.IGNORECASE
    )
    if must_have and preferred:
        start = must_have.start()
        end = preferred.start()
        if end > start:
            must_block = text[start:end].lower()
            if "preferred" in must_block or "good-to-have" in must_block:
                errors.append(
                    "Preferred skills appear inside the must-have section"
                )

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_jd.py <draft-jd.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    errors = validate(path.read_text(encoding="utf-8"))
    if errors:
        print("JD validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("JD validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())