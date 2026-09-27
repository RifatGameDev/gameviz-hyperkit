import json
from pathlib import Path

import pytest

from hyperkit.analytics.firebase import (
    FirebaseAnalyticsAndroidProvider,
    load_firebase_analytics_config,
)


def _write_google_services(
    path: Path,
    *,
    clients: list[dict],
) -> Path:
    payload = {
        "project_info": {
            "project_id": "hyperkit-test-project",
        },
        "client": clients,
    }

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    return path


def _client(
    package_name: str,
    app_id: str,
    api_key: str,
) -> dict:
    return {
        "client_info": {
            "mobilesdk_app_id": app_id,
            "android_client_info": {
                "package_name": package_name,
            },
        },
        "api_key": [
            {
                "current_key": api_key,
            }
        ],
    }


def test_load_firebase_config_from_single_client_json(
    tmp_path: Path,
):
    path = _write_google_services(
        tmp_path / "google-services.json",
        clients=[
            _client(
                "org.gameviz.demo",
                "1:123:android:abc",
                "api-key-123",
            ),
        ],
    )

    config = load_firebase_analytics_config(
        path
    )

    assert (
        config.application_id
        == "1:123:android:abc"
    )
    assert config.api_key == "api-key-123"
    assert (
        config.project_id
        == "hyperkit-test-project"
    )


def test_load_firebase_config_selects_requested_package(
    tmp_path: Path,
):
    path = _write_google_services(
        tmp_path / "google-services.json",
        clients=[
            _client(
                "org.gameviz.first",
                "1:first:android:abc",
                "first-key",
            ),
            _client(
                "org.gameviz.second",
                "1:second:android:def",
                "second-key",
            ),
        ],
    )

    config = load_firebase_analytics_config(
        path,
        package_name="org.gameviz.second",
    )

    assert (
        config.application_id
        == "1:second:android:def"
    )
    assert config.api_key == "second-key"


def test_load_firebase_config_requires_package_for_multiple_clients(
    tmp_path: Path,
):
    path = _write_google_services(
        tmp_path / "google-services.json",
        clients=[
            _client(
                "org.gameviz.first",
                "1:first:android:abc",
                "first-key",
            ),
            _client(
                "org.gameviz.second",
                "1:second:android:def",
                "second-key",
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="multiple clients",
    ):
        load_firebase_analytics_config(
            path
        )


def test_firebase_provider_can_be_created_from_google_services_json(
    tmp_path: Path,
):
    path = _write_google_services(
        tmp_path / "google-services.json",
        clients=[
            _client(
                "org.gameviz.demo",
                "1:123:android:abc",
                "api-key-123",
            ),
        ],
    )

    provider = (
        FirebaseAnalyticsAndroidProvider
        .from_google_services_json(
            path
        )
    )

    assert (
        provider.config.application_id
        == "1:123:android:abc"
    )
    assert (
        provider.config.project_id
        == "hyperkit-test-project"
    )


def test_load_firebase_config_rejects_missing_package(
    tmp_path: Path,
):
    path = _write_google_services(
        tmp_path / "google-services.json",
        clients=[
            _client(
                "org.gameviz.demo",
                "1:123:android:abc",
                "api-key-123",
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="does not contain package",
    ):
        load_firebase_analytics_config(
            path,
            package_name="org.gameviz.missing",
        )
