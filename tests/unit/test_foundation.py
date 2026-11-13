from __future__ import annotations

import json
import subprocess
import sys

from iptv_auto_next.models import RunReport


def test_run_report_finishes_with_utc_timestamp() -> None:
    report = RunReport(run_id="test-run", mode="test")

    report.finish("success")

    assert report.status == "success"
    assert report.finished_at is not None
    assert report.finished_at.tzinfo is not None
    assert report.finished_at.utcoffset().total_seconds() == 0


def test_test_mode_emits_json_report() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "iptv_auto_next.main", "--mode", "test"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["mode"] == "test"
    assert report["status"] == "success"
    assert report["errors"] == []
