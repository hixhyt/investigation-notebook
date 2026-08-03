from __future__ import annotations

import argparse
from pathlib import Path

from .notebook import add_analysis, add_evidence, add_timeline, load_case, new_case, render_markdown, save_case, set_conclusion


def main() -> None:
    parser = argparse.ArgumentParser(prog="investigation-notebook", description="Structured investigation notebook")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("case_id")
    new.add_argument("--title", required=True)
    evidence = sub.add_parser("evidence")
    evidence.add_argument("case")
    evidence.add_argument("--source", required=True)
    evidence.add_argument("--description", required=True)
    evidence.add_argument("--file")
    timeline = sub.add_parser("timeline")
    timeline.add_argument("case")
    timeline.add_argument("--timestamp", required=True)
    timeline.add_argument("--event", required=True)
    timeline.add_argument("--actor", default="unknown")
    analysis = sub.add_parser("analysis")
    analysis.add_argument("case")
    analysis.add_argument("--note", required=True)
    conclusion = sub.add_parser("conclusion")
    conclusion.add_argument("case")
    conclusion.add_argument("--text", required=True)
    render = sub.add_parser("render")
    render.add_argument("case")
    render.add_argument("--out")
    args = parser.parse_args()

    if args.command == "new":
        path = Path(f"{args.case_id}.json")
        save_case(new_case(args.case_id, args.title), path)
        print(path)
        return
    case = load_case(args.case)
    if args.command == "evidence":
        add_evidence(case, args.source, args.description, args.file)
        save_case(case, args.case)
    elif args.command == "timeline":
        add_timeline(case, args.timestamp, args.event, args.actor)
        save_case(case, args.case)
    elif args.command == "analysis":
        add_analysis(case, args.note)
        save_case(case, args.case)
    elif args.command == "conclusion":
        set_conclusion(case, args.text)
        save_case(case, args.case)
    elif args.command == "render":
        out = Path(args.out or f"{case['case_id']}.md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(case), encoding="utf-8")
        print(out)


if __name__ == "__main__":
    main()
