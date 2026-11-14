from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]

CHANNELS_PATH = ROOT / "data" / "global_channels" / "channels.json"
FILTER_PATH = ROOT / "data" / "global_channels" / "channel_filter.json"
SOURCES_PATH = ROOT / "config" / "sources.json"
SUMMARY_PATH = ROOT / "data" / "global_channels" / "validation_summary.json"

SCHEMA_PATHS = {
    "sources.schema.json": ROOT / "schemas" / "sources.schema.json",
    "run_report.schema.json": ROOT / "schemas" / "run_report.schema.json",
    "publish_manifest.schema.json": ROOT / "schemas" / "publish_manifest.schema.json",
    "candidate_manifest.schema.json": ROOT / "schemas" / "candidate_manifest.schema.json",
    "subscription_info.schema.json": ROOT / "schemas" / "subscription_info.schema.json",
    "global_channels.schema.json": (ROOT / "data" / "global_channels" / "channels.schema.json"),
    "channel_filter.schema.json": (
        ROOT / "data" / "global_channels" / "channel_filter.schema.json"
    ),
}

FORMAT_CHECKER = FormatChecker()
SHA256 = "a" * 64
COMMIT_SHA = "b" * 40
SELECTED_COUNTRIES = ("CN", "HK", "MO", "TW")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema(name: str) -> dict:
    return load_json(SCHEMA_PATHS[name])


def make_validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(
        load_schema(name),
        format_checker=FORMAT_CHECKER,
    )


def normalize_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip().lower()


def selected_country_conflicts(channels: list[dict]) -> dict[str, int]:
    result = {}

    for country in SELECTED_COUNTRIES:
        name_to_ids: dict[str, set[str]] = {}

        for channel in channels:
            if channel["country"] != country:
                continue

            names = [channel["canonical_name"], *channel["aliases"]]

            for name in names:
                key = normalize_name(name)
                if key:
                    name_to_ids.setdefault(key, set()).add(channel["tvg_id"])

        result[country] = sum(1 for channel_ids in name_to_ids.values() if len(channel_ids) > 1)

    return result


def valid_global_channel() -> dict:
    return {
        "tvg_id": "CCTV5.cn",
        "canonical_name": "CCTV-5",
        "aliases": ["CCTV5", "中央五套"],
        "country": "CN",
        "categories": ["sports"],
    }


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


@pytest.mark.parametrize("schema_name", list(SCHEMA_PATHS))
def test_schema_is_valid_draft_2020_12(schema_name: str) -> None:
    Draft202012Validator.check_schema(load_schema(schema_name))


def test_global_channel_data_matches_schema() -> None:
    data = load_json(CHANNELS_PATH)
    make_validator("global_channels.schema.json").validate(data)


def test_global_channel_ids_are_nonempty_and_globally_unique() -> None:
    data = load_json(CHANNELS_PATH)
    channels = data["channels"]
    ids = [channel["tvg_id"] for channel in channels]

    assert all(isinstance(channel_id, str) and channel_id.strip() for channel_id in ids)
    assert len(ids) == len(set(ids))


def test_global_channel_names_contain_no_forbidden_characters() -> None:
    channels = load_json(CHANNELS_PATH)["channels"]

    for channel in channels:
        names = [channel["canonical_name"], *channel["aliases"]]

        for name in names:
            assert '"' not in name
            assert "\r" not in name
            assert "\n" not in name


def test_channel_filter_config_matches_schema() -> None:
    make_validator("channel_filter.schema.json").validate(load_json(FILTER_PATH))


def test_sources_config_matches_schema() -> None:
    make_validator("sources.schema.json").validate(load_json(SOURCES_PATH))


def test_source_ids_are_globally_unique() -> None:
    sources = load_json(SOURCES_PATH)
    source_ids = [
        source["id"]
        for group in ("manual_single", "carriers", "discovery")
        for source in sources[group]
    ]

    assert len(source_ids) == len(set(source_ids))


def test_validation_summary_matches_actual_global_channel_data() -> None:
    channels = load_json(CHANNELS_PATH)["channels"]
    summary = load_json(SUMMARY_PATH)

    ids = {channel["tvg_id"] for channel in channels}
    countries = {channel["country"] for channel in channels}
    categories = {category for channel in channels for category in channel["categories"]}

    country_counts = {
        country: sum(1 for channel in channels if channel["country"] == country)
        for country in SELECTED_COUNTRIES
    }

    empty_categories = sum(1 for channel in channels if not channel["categories"])

    assert summary["channels"] == len(channels)
    assert summary["unique_tvg_ids"] == len(ids)
    assert summary["countries"] == len(countries)
    assert summary["category_values"] == len(categories)
    assert summary["country_counts"] == country_counts
    assert summary["empty_categories"] == empty_categories
    assert summary["json_bytes"] == CHANNELS_PATH.stat().st_size
    assert summary["selected_country_name_conflict_keys"] == (selected_country_conflicts(channels))


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


def test_global_channels_schema_accepts_valid_channel() -> None:
    validator = make_validator("global_channels.schema.json")

    validator.validate({"channels": [valid_global_channel()]})


def test_global_channels_schema_rejects_empty_channels() -> None:
    validator = make_validator("global_channels.schema.json")

    assert not validator.is_valid({"channels": []})


def test_global_channels_schema_rejects_missing_aliases() -> None:
    validator = make_validator("global_channels.schema.json")
    channel = valid_global_channel()
    del channel["aliases"]

    assert not validator.is_valid({"channels": [channel]})


def test_global_channels_schema_rejects_duplicate_aliases() -> None:
    validator = make_validator("global_channels.schema.json")
    channel = valid_global_channel()
    channel["aliases"] = ["CCTV5", "CCTV5"]

    assert not validator.is_valid({"channels": [channel]})


def test_channel_filter_schema_accepts_specific_countries() -> None:
    validator = make_validator("channel_filter.schema.json")

    validator.validate(
        {
            "countries": ["CN", "HK", "MO", "TW"],
            "categories": ["sports", "news"],
        }
    )


def test_channel_filter_schema_accepts_all_countries() -> None:
    validator = make_validator("channel_filter.schema.json")

    validator.validate(
        {
            "countries": ["*"],
            "categories": [],
        }
    )


def test_channel_filter_schema_rejects_wildcard_with_other_countries() -> None:
    validator = make_validator("channel_filter.schema.json")

    assert not validator.is_valid(
        {
            "countries": ["*", "CN"],
            "categories": [],
        }
    )


def test_channel_filter_schema_rejects_invalid_country_code() -> None:
    validator = make_validator("channel_filter.schema.json")

    assert not validator.is_valid(
        {
            "countries": ["China"],
            "categories": [],
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


def test_run_report_rejects_incomplete_report() -> None:
    validator = make_validator("run_report.schema.json")

    assert not validator.is_valid(
        {
            "run_id": "test",
            "mode": "test",
        }
    )
