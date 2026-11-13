
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"

SCHEMA_NAMES = [
    "sources.schema.json",
    "channels.schema.json",
    "run_report.schema.json",
    "publish_manifest.schema.json",
    "candidate_manifest.schema.json",
    "subscription_info.schema.json",
]


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_schema_is_valid_draft_2020_12(schema_name: str) -> None:
    schema = load_schema(schema_name)
    Draft202012Validator.check_schema(schema)


def test_sources_schema_accepts_empty_arrays() -> None:
    validator = Draft202012Validator(
        load_schema("sources.schema.json"),
        format_checker=FormatChecker(),
    )

    validator.validate(
        {
            "manual_single": [],
            "carriers": [],
            "discovery": [],
        }
    )


def test_sources_schema_accepts_valid_sources() -> None:
    validator = Draft202012Validator(
        load_schema("sources.schema.json"),
        format_checker=FormatChecker(),
    )

    validator.validate(
        {
            "manual_single": [
                {
                    "id": "manual-001",
                    "tvg_id": "CCTV5.cn",
                    "url": "https://example.org/live.ts",
                }
            ],
            "carriers": [
                {
                    "id": "carrier-001",
                    "url": "https://example.org/carrier.m3u",
                    "enabled": True,
                }
            ],
            "discovery": [
                {
                    "id": "discovery-001",
                    "url": "https://example.org/discovery.m3u",
                    "enabled": False,
                }
            ],
        }
    )


def test_sources_schema_rejects_missing_array() -> None:
    validator = Draft202012Validator(load_schema("sources.schema.json"))

    assert not validator.is_valid(
        {
            "manual_single": [],
            "carriers": [],
        }
    )


def test_sources_schema_rejects_unknown_field() -> None:
    validator = Draft202012Validator(load_schema("sources.schema.json"))

    assert not validator.is_valid(
        {
            "manual_single": [],
            "carriers": [],
            "discovery": [],
            "unexpected": True,
        }
    )


def test_channels_schema_accepts_valid_channel() -> None:
    validator = Draft202012Validator(load_schema("channels.schema.json"))

    validator.validate(
        {
            "channels": [
                {
                    "tvg_id": "CCTV5.cn",
                    "canonical_name": "CCTV-5",
                    "aliases": ["CCTV5", "中央五套"],
                }
            ]
        }
    )


def test_channels_schema_rejects_empty_channels() -> None:
    validator = Draft202012Validator(load_schema("channels.schema.json"))

    assert not validator.is_valid({"channels": []})


def test_channels_schema_rejects_missing_aliases() -> None:
    validator = Draft202012Validator(load_schema("channels.schema.json"))

    assert not validator.is_valid(
        {
            "channels": [
                {
                    "tvg_id": "CCTV5.cn",
                    "canonical_name": "CCTV-5",
                }
            ]
        }
    )


def test_candidate_manifest_rejects_invalid_hash() -> None:
    validator = Draft202012Validator(
        load_schema("candidate_manifest.schema.json"),
        format_checker=FormatChecker(),
    )

    assert not validator.is_valid(
        {
            "schema_version": "1",
            "generated_at": "2026-11-13T00:00:00Z",
            "source_commit_sha": "abc",
            "m3u_sha256": "invalid",
            "txt_sha256": "invalid",
            "layer1_status": "passed",
            "channel_count": 1,
            "line_count": 1,
            "formal_file_baselines": {
                "output/iptv.m3u": None,
                "output/iptv.txt": None,
                "output/subscription_info.json": None,
                "output/publish_manifest.json": None,
            },
        }
    )


def test_subscription_info_requires_null_evidence_when_unverified() -> None:
    validator = Draft202012Validator(
        load_schema("subscription_info.schema.json"),
        format_checker=FormatChecker(),
    )

    data = {
        "generated_at": "2026-11-13T00:00:00Z",
        "schema_version": "1",
        "channel_count": 1,
        "line_count": 1,
        "m3u_sha256": "a" * 64,
        "txt_sha256": "b" * 64,
        "layer1_status": "passed",
        "layer2_status": "unverified",
        "layer3_status": "unverified",
        "layer2_evidence": None,
        "layer3_evidence": None,
    }

    validator.validate(data)

    data["layer2_evidence"] = {
        "result": "passed"
    }

    assert not validator.is_valid(data)


def test_publish_manifest_rejects_missing_file_record() -> None:
    validator = Draft202012Validator(
        load_schema("publish_manifest.schema.json"),
        format_checker=FormatChecker(),
    )

    assert not validator.is_valid(
        {
            "schema_version": "1",
            "generated_at": "2026-11-13T00:00:00Z",
            "source_commit_sha": "abc",
            "candidate_commit_sha": None,
            "files": {},
            "channel_count": 1,
            "line_count": 1,
            "previous_channel_count": None,
            "previous_line_count": None,
            "last_successful_daily_update_at": None,
            "last_successful_daily_target_slot": None,
            "publish_blocked": False,
            "publish_block_reason": None,
            "layer1_status": "passed",
            "layer2_status": "unverified",
            "layer3_status": "unverified",
        }
    )


def test_run_report_rejects_incomplete_report() -> None:
    validator = Draft202012Validator(
        load_schema("run_report.schema.json"),
        format_checker=FormatChecker(),
    )

    assert not validator.is_valid(
        {
            "run_id": "test",
            "mode": "test",
        }
    )
