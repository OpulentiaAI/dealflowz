#!/usr/bin/env python3
"""Validate a Northcliff deal-flow gate packet.

Input is a JSON file shaped like the packet in SKILL.md. The script reports
blocking issues, warnings, and a suggested gate result.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TARGET_STAGES = {
    "New lead",
    "Data enrichment",
    "Primary filter review",
    "Outreach sequence",
    "Owner or broker replied",
    "NDA / CIM / financial request",
    "Financial modeling",
    "Seller or broker call",
    "LOI drafting",
    "Not a target",
    "Inactive / released lead",
}

PRIMARY_FIELDS = [
    "website",
    "source_type",
    "revenue_estimate",
    "ebitda_estimate",
    "years_profitable",
    "geography",
]

CONFIDENCE_VALUES = {"Verified", "Estimated", "Unknown"}
TARGET_GEOGRAPHY_TERMS = ("houston", "san antonio", "austin")


def field(packet: dict[str, Any], name: str) -> dict[str, Any]:
    value = packet.get("fields", {}).get(name)
    if isinstance(value, dict):
        return value
    if value is None and name in packet:
        value = packet.get(name)
    if value is None:
        return {"value": None, "confidence": "Unknown", "source": ""}
    return {"value": value, "confidence": "Unknown", "source": ""}


def numeric_value(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = (
            value.lower()
            .replace("$", "")
            .replace(",", "")
            .replace("mm", "000000")
            .replace("m", "000000")
            .strip()
        )
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def add_missing_primary_field_issues(packet: dict[str, Any], issues: list[str], warnings: list[str]) -> None:
    fields = packet.get("fields")
    if not isinstance(fields, dict):
        issues.append("Missing fields object.")
        return

    for name in PRIMARY_FIELDS:
        item = field(packet, name)
        confidence = item.get("confidence", "Unknown")
        if confidence not in CONFIDENCE_VALUES:
            issues.append(f"{name} has invalid confidence {confidence!r}.")
        if item.get("value") in (None, "") and confidence != "Unknown":
            issues.append(f"{name} has no value but is not marked Unknown.")
        if confidence in {"Verified", "Estimated"} and not item.get("source"):
            warnings.append(f"{name} has {confidence} confidence but no source.")


def primary_filter(packet: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    unknown = False

    revenue = numeric_value(field(packet, "revenue_estimate").get("value"))
    if revenue is None:
        unknown = True
    elif not 5_000_000 <= revenue <= 25_000_000:
        reasons.append("Revenue outside $5mm to $25mm.")

    ebitda = numeric_value(field(packet, "ebitda_estimate").get("value"))
    if ebitda is None:
        unknown = True
    elif not 1_000_000 <= ebitda <= 5_000_000:
        reasons.append("EBITDA outside $1mm to $5mm.")

    years_profitable = numeric_value(field(packet, "years_profitable").get("value"))
    if years_profitable is None:
        unknown = True
    elif years_profitable < 3:
        reasons.append("Profitability history below 3 years.")

    geography = str(field(packet, "geography").get("value") or "").lower()
    if not geography:
        unknown = True
    elif not any(term in geography for term in TARGET_GEOGRAPHY_TERMS):
        reasons.append("Geography outside Houston, San Antonio, or Austin.")

    if reasons:
        return "fail", reasons
    if unknown:
        return "review", ["One or more primary filter fields are unknown."]
    return "pass", ["Primary objective filters appear in range."]


def validate(packet: dict[str, Any]) -> tuple[list[str], list[str], str, list[str]]:
    issues: list[str] = []
    warnings: list[str] = []

    if not packet.get("company"):
        issues.append("Missing company name.")

    stage = packet.get("stage")
    if stage not in TARGET_STAGES:
        issues.append(f"Stage must be one of: {', '.join(sorted(TARGET_STAGES))}.")

    add_missing_primary_field_issues(packet, issues, warnings)

    decision, reasons = primary_filter(packet)

    tasks = packet.get("tasks", [])
    target_status = packet.get("target_status")
    if stage not in {"Not a target", "Inactive / released lead"} and not tasks:
        warnings.append("No next task is present for an active lead.")

    if stage == "Not a target":
        not_target_reason = packet.get("not_target_reason") or field(packet, "not_target_reason").get("value")
        if not not_target_reason:
            issues.append("Not a target stage requires a not-target reason.")
        if target_status != "not target":
            warnings.append("Not a target stage should use target_status 'not target'.")

    if stage in {"Financial modeling", "Seller or broker call", "LOI drafting"}:
        review_items = packet.get("human_review", [])
        if not review_items:
            issues.append(f"{stage} requires human_review items.")

    documents = packet.get("documents", [])
    if stage in {"Financial modeling", "Seller or broker call", "LOI drafting"} and not documents:
        warnings.append(f"{stage} usually requires linked diligence documents.")

    return issues, warnings, decision, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Northcliff deal-flow gate packet.")
    parser.add_argument("packet", help="Path to a JSON packet file.")
    args = parser.parse_args()

    path = Path(args.packet)
    try:
        packet = json.loads(path.read_text())
    except Exception as exc:
        print(f"ERROR: could not read JSON packet: {exc}", file=sys.stderr)
        return 2

    if not isinstance(packet, dict):
        print("ERROR: packet root must be a JSON object.", file=sys.stderr)
        return 2

    issues, warnings, decision, reasons = validate(packet)

    print(f"Gate decision: {decision}")
    for reason in reasons:
        print(f"- {reason}")

    if issues:
        print("\nBlocking issues:")
        for issue in issues:
            print(f"- {issue}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
