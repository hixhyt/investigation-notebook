from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any


def new_case(case_id: str, title: str) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "title": title,
        "created_utc": dt.datetime.now(dt.UTC).isoformat(),
        "evidence": [],
        "timeline": [],
        "analysis": [],
        "conclusion": "",
    }


def load_case(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_case(case: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(case, indent=2), encoding="utf-8")


def add_evidence(case: dict[str, Any], source: str, description: str, file_path: str | None = None) -> dict[str, Any]:
    item = {"source": source, "description": description, "added_utc": dt.datetime.now(dt.UTC).isoformat()}
    if file_path:
        data = Path(file_path).read_bytes()
        item["file_path"] = file_path
        item["sha256"] = hashlib.sha256(data).hexdigest()
        item["size_bytes"] = len(data)
    case.setdefault("evidence", []).append(item)
    return item


def add_timeline(case: dict[str, Any], timestamp: str, event: str, actor: str = "unknown") -> dict[str, str]:
    item = {"timestamp": timestamp, "actor": actor, "event": event}
    case.setdefault("timeline", []).append(item)
    case["timeline"] = sorted(case["timeline"], key=lambda row: row["timestamp"])
    return item


def add_analysis(case: dict[str, Any], note: str) -> dict[str, str]:
    item = {"created_utc": dt.datetime.now(dt.UTC).isoformat(), "note": note}
    case.setdefault("analysis", []).append(item)
    return item


def set_conclusion(case: dict[str, Any], conclusion: str) -> None:
    case["conclusion"] = conclusion


def render_markdown(case: dict[str, Any]) -> str:
    lines = [
        f"# {case['case_id']}: {case['title']}",
        "",
        f"Created UTC: `{case.get('created_utc', '')}`",
        "",
        "## Evidence",
    ]
    for item in case.get("evidence", []):
        hash_text = f" sha256 `{item['sha256']}`" if item.get("sha256") else ""
        lines.append(f"- {item['source']}: {item['description']}{hash_text}")
    lines.extend(["", "## Timeline"])
    for item in case.get("timeline", []):
        lines.append(f"- {item['timestamp']} - {item.get('actor', 'unknown')}: {item['event']}")
    lines.extend(["", "## Analysis"])
    for item in case.get("analysis", []):
        lines.append(f"- {item['note']}")
    lines.extend(["", "## Conclusion", "", case.get("conclusion", "Pending.") or "Pending."])
    return "\n".join(lines) + "\n"
