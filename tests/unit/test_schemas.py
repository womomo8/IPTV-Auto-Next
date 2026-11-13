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

FORMAT_CHECKER = FormatChecker()
SHA256 = "a" * 64
COMMIT_SHA = "b" * 40


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def make_validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(
        load_schema(name),
        format_checker=FORMAT_CHECKER,
    )


def valid_subscription_info() -> dict:
    return {
        "generated_at": "2026-11-13T00:00:00Z",
        "schema_version": "1",
        "channel_count": 1,
        "line_count": 1,
        "m3u_sha256": SHA256,
        "txt_sha256": "c" * 64,
        "layer1_status": "passed",
        "layer2_status": "unverified",
        "layer3_status": "unverified",
        "layer2_evidence": None,
        "layer3_evidence": None,
    }


def valid_layer2_evidence(result: str = "passed") -> dict:
    return {
        "result": result,
        "m3u_sha256": SHA256,
        "txt_sha256": "c" * 64,
        "verified_at": "2026-11-13T00:00:00Z",
        "network_environment": "test environment",
        "verification_method": "manual verification",
        "evidence_location": "test evidence",
    }


def valid_layer3_evidence(result: str = "passed") -> dict:
    return {
        "result": result,
        "m3u_sha256": SHA256,
        "txt_sha256": "c" * 64,
        "media_url": "https://example.org/live.ts",
        "hls_segment_results": [],
        "verified_at": "2026-11-13T00:00:00Z",
        "network_environment": "test environment",
        "evidence_location": "test evidence",
    }


def valid_candidate_manifest(baselines: dict | None = None) -> dict:
    if baselines is None:
        baselines = {
            "output/iptv.m3u": None,
            "output/iptv.txt": None,
            "output/subscription_info.json": None,
            "output/publish_manifest.json": None,
        }

    return {
        "schema_version": "1",
        "generated_at": "2026-11-13T00:00:00Z",
        "source_commit_sha": COMMIT_SHA,
        "m3u_sha256": SHA256,
        "txt_sha256": "c" * 64,
        "layer1_status": "passed",
        "channel_count": 1,
        "line_count": 1,
        "formal_file_baselines": baselines,
    }


def valid_publish_manifest() -> dict:
    return {
        "schema_version": "1",
        "generated_at": "2026-11-13T00:00:00Z",
        "source_commit_sha": COMMIT_SHA,
        "candidate_commit_sha": None,
        "files": {
            "iptv.m3u": {
                "path": "output/iptv.m3u",
                "size_bytes": 100,
                "sha256": SHA256,
            },
            "iptv.txt": {
                "path": "output/iptv.txt",
                "size_bytes": 80,
                "sha256": "c" * 64,
            },
            "subscription_info.json": {
                "path": "output/subscription_info.json",
                "size_bytes": 200,
                "sha256": "d" * 64,
            },
        },
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


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_schema_is_valid_draft_2020_12(schema_name: str) -> None:
    Draft202012Validator.check_schema(load_schema(schema_name))


def test_sources_schema_accepts_empty_arrays() -> None:
    validator = make_validator("sources.schema.json")

    validator.validate(
        {
            "manual_single": [],
            "carriers": [],
            "discovery": [],
        }
    )


def test_sources_schema_accepts_valid_sources() -> None:
    validator = make_validator("sources.schema.json")

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
    validator = make_validator("sources.schema.json")

    assert not validator.is_valid(
        {
            "manual_single": [],
            "carriers": [],
        }
    )


def test_sources_schema_rejects_unknown_field() -> None:
    validator = make_validator("sources.schema.json")

    assert not validator.is_valid(
        {
            "manual_single": [],
            "carriers": [],
            "discovery": [],
            "unexpected": True,
        }
    )


def test_sources_schema_rejects_url_userinfo() -> None:
    validator = make_validator("sources.schema.json")

    assert not validator.is_valid(
        {
            "manual_single": [
                {
                    "id": "manual-001",
                    "tvg_id": "CCTV5.cn",
                    "url": "https://user:password@example.org/live.ts",
                }
            ],
            "carriers": [],
            "discovery": [],
        }
    )


def test_channels_schema_accepts_valid_channel() -> None:
    validator = make_validator("channels.schema.json")

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
    validator = make_validator("channels.schema.json")

    assert not validator.is_valid({"channels": []})


def test_channels_schema_rejects_missing_aliases() -> None:
    validator = make_validator("channels.schema.json")

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


def test_candidate_manifest_accepts_all_null_baselines() -> None:
    validator = make_validator("candidate_manifest.schema.json")

    validator.validate(valid_candidate_manifest())


def test_candidate_manifest_accepts_all_present_baselines() -> None:
    validator = make_validator("candidate_manifest.schema.json")
    baselines = {
        "output/iptv.m3u": SHA256,
        "output/iptv.txt": "c" * 64,
        "output/subscription_info.json": "d" * 64,
        "output/publish_manifest.json": "e" * 64,
    }

    validator.validate(valid_candidate_manifest(baselines))


def test_candidate_manifest_rejects_partial_baselines() -> None:
    validator = make_validator("candidate_manifest.schema.json")
    baselines = {
        "output/iptv.m3u": SHA256,
        "output/iptv.txt": None,
        "output/subscription_info.json": "d" * 64,
        "output/publish_manifest.json": None,
    }

    assert not validator.is_valid(valid_candidate_manifest(baselines))


def test_candidate_manifest_rejects_invalid_hash() -> None:
    validator = make_validator("candidate_manifest.schema.json")
    data = valid_candidate_manifest()
    data["m3u_sha256"] = "invalid"

    assert not validator.is_valid(data)


def test_subscription_info_accepts_unverified_without_evidence() -> None:
    validator = make_validator("subscription_info.schema.json")

    validator.validate(valid_subscription_info())


def test_subscription_info_requires_evidence_for_passed_layer2() -> None:
    validator = make_validator("subscription_info.schema.json")
    data = valid_subscription_info()
    data["layer2_status"] = "passed"

    assert not validator.is_valid(data)

    data["layer2_evidence"] = valid_layer2_evidence("passed")
    validator.validate(data)


def test_subscription_info_rejects_layer2_result_mismatch() -> None:
    validator = make_validator("subscription_info.schema.json")
    data = valid_subscription_info()
    data["layer2_status"] = "passed"
    data["layer2_evidence"] = valid_layer2_evidence("failed")

    assert not validator.is_valid(data)


def test_subscription_info_requires_evidence_for_failed_layer3() -> None:
    validator = make_validator("subscription_info.schema.json")
    data = valid_subscription_info()
    data["layer3_status"] = "failed"

    assert not validator.is_valid(data)

    data["layer3_evidence"] = valid_layer3_evidence("failed")
    validator.validate(data)


def test_subscription_info_requires_hls_segment_results_field() -> None:
    validator = make_validator("subscription_info.schema.json")
    data = valid_subscription_info()
    evidence = valid_layer3_evidence()
    del evidence["hls_segment_results"]
    data["layer3_status"] = "passed"
    data["layer3_evidence"] = evidence

    assert not validator.is_valid(data)


def test_subscription_info_rejects_evidence_when_unverified() -> None:
    validator = make_validator("subscription_info.schema.json")
    data = valid_subscription_info()
    data["layer2_evidence"] = valid_layer2_evidence()

    assert not validator.is_valid(data)


def test_publish_manifest_accepts_valid_manifest() -> None:
    validator = make_validator("publish_manifest.schema.json")

    validator.validate(valid_publish_manifest())


def test_publish_manifest_rejects_wrong_file_path() -> None:
    validator = make_validator("publish_manifest.schema.json")
    data = valid_publish_manifest()
    data["files"]["iptv.m3u"]["path"] = "wrong/path.m3u"

    assert not validator.is_valid(data)


def test_publish_manifest_rejects_only_one_previous_count() -> None:
    validator = make_validator("publish_manifest.schema.json")
    data = valid_publish_manifest()
    data["previous_channel_count"] = 10

    assert not validator.is_valid(data)


def test_publish_manifest_requires_reason_when_blocked() -> None:
    validator = make_validator("publish_manifest.schema.json")
    data = valid_publish_manifest()
    data["publish_blocked"] = True

    assert not validator.is_valid(data)

    data["publish_block_reason"] = "test block reason"
    validator.validate(data)


def test_run_report_rejects_incomplete_report() -> None:
    validator = make_validator("run_report.schema.json")

    assert not validator.is_valid(
        {
            "run_id": "test",
            "mode": "test",
        }
    )
