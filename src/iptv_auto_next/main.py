"""Command-line entry point for the initial project foundation."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC

from iptv_auto_next.models import RunReport


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iptv-auto-next")
    parser.add_argument(
        "--mode",
        choices=("test",),
        default="test",
        help="Run the non-networking foundation test mode.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = RunReport(run_id=str(uuid.uuid4()), mode=args.mode)
    report.finish("success")

    payload = {
        "run_id": report.run_id,
        "mode": report.mode,
        "started_at": report.started_at.isoformat().replace("+00:00", "Z"),
        "finished_at": report.finished_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "status": report.status,
        "errors": report.errors,
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
