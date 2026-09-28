from pathlib import Path

import pytest

from hyperkit.analytics import (
    AnalyticsEvent,
)
from hyperkit.analytics.firebase import (
    FIREBASE_ANALYTICS_DEPENDENCY,
    FirebaseAnalyticsAndroidBridge,
    FirebaseAnalyticsAndroidProvider,
    FirebaseAnalyticsConfig,
    configure_firebase_analytics_android_project,
)
from hyperkit.android import (
    create_buildozer_spec,
)


def test_firebase_config_requires_all_values():
    with pytest.raises(
        ValueError,
        match="api_key",
    ):
        FirebaseAnalyticsConfig(
            application_id="app-id",
            api_key="",
            project_id="project-id",
        )


def test_firebase_bridge_declares_android_build_requirements():
    bridge = FirebaseAnalyticsAndroidBridge(
        FirebaseAnalyticsConfig(
            application_id="app-id",
            api_key="api-key",
            project_id="project-id",
        )
    )

    requirements = (
        bridge.build_requirements
    )

    assert (
        FIREBASE_ANALYTICS_DEPENDENCY
        in requirements.gradle_dependencies
    )

    assert (
        "pyjnius"
        in requirements.python_requirements
    )

    assert (
        requirements.permissions
        == (
            "INTERNET",
            "ACCESS_NETWORK_STATE",
        )
    )

    assert (
        requirements.java_source_dirs
        == ("android_src",)
    )

    assert requirements.enable_androidx


def test_firebase_provider_keeps_project_config():
    provider = (
        FirebaseAnalyticsAndroidProvider(
            application_id="app-id",
            api_key="api-key",
            project_id="project-id",
        )
    )

    assert (
        provider.provider_name
        == "firebase-analytics"
    )

    assert (
        provider.config.project_id
        == "project-id"
    )


def test_firebase_bridge_fails_cleanly_on_desktop():
    bridge = FirebaseAnalyticsAndroidBridge(
        FirebaseAnalyticsConfig(
            application_id="app-id",
            api_key="api-key",
            project_id="project-id",
        )
    )

    result = bridge.initialize()

    assert not result.success
    assert not bridge.initialized


def test_firebase_bridge_rejects_event_before_initialize():
    bridge = FirebaseAnalyticsAndroidBridge(
        FirebaseAnalyticsConfig(
            application_id="app-id",
            api_key="api-key",
            project_id="project-id",
        )
    )

    result = bridge.track_event(
        AnalyticsEvent(
            "game_start"
        )
    )

    assert not result.success


def test_configure_firebase_analytics_android_project(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="Firebase Smoke",
    )

    spec_path, java_path = (
        configure_firebase_analytics_android_project(
            tmp_path
        )
    )

    content = spec_path.read_text(
        encoding="utf-8",
    )

    assert (
        FIREBASE_ANALYTICS_DEPENDENCY
        in content
    )

    assert (
        "requirements = "
        "python3==3.11.9,"
        "hostpython3==3.11.9,"
        "kivy,"
        "gameviz-hyperkit,"
        "pyjnius"
        in content
    )

    assert (
        "android.permissions = "
        "VIBRATE,INTERNET,"
        "ACCESS_NETWORK_STATE"
        in content
    )

    assert (
        "android.add_src = android_src"
        in content
    )

    assert (
        "android.enable_androidx = True"
        in content
    )

    assert java_path.is_file()

    java = java_path.read_text(
        encoding="utf-8",
    )

    assert (
        "FirebaseOptions.Builder"
        in java
    )

    assert (
        "FirebaseAnalytics.getInstance"
        in java
    )

    assert (
        "analytics.logEvent"
        in java
    )


def test_configure_firebase_analytics_with_google_services_writes_resources(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="Firebase Smoke",
    )

    google_services = (
        tmp_path
        / "google-services.json"
    )

    google_services.write_text(
        """{
  "project_info": {
    "project_id": "hyperkit-test-project"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:123:android:abc",
        "android_client_info": {
          "package_name": "org.gameviz.demo"
        }
      },
      "api_key": [
        {
          "current_key": "api-key-123"
        }
      ]
    }
  ]
}
""",
        encoding="utf-8",
    )

    spec_path, _ = (
        configure_firebase_analytics_android_project(
            tmp_path,
            google_services_path=(
                google_services
            ),
            package_name=(
                "org.gameviz.demo"
            ),
        )
    )

    content = spec_path.read_text(
        encoding="utf-8",
    )

    assert (
        "android.add_resources = android_resources"
        in content
    )

    resource = (
        tmp_path
        / "android_resources"
        / "values"
        / "firebase_analytics.xml"
    )

    assert resource.is_file()

    xml = resource.read_text(
        encoding="utf-8",
    )

    assert (
        "google_app_id"
        in xml
    )
    assert (
        "1:123:android:abc"
        in xml
    )
    assert (
        "google_api_key"
        in xml
    )
    assert (
        "api-key-123"
        in xml
    )
    assert (
        "project_id"
        in xml
    )
    assert (
        "hyperkit-test-project"
        in xml
    )


def test_configure_firebase_analytics_is_idempotent(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="Firebase Smoke",
    )

    configure_firebase_analytics_android_project(
        tmp_path
    )

    configure_firebase_analytics_android_project(
        tmp_path
    )

    content = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8",
    )

    assert content.count(
        FIREBASE_ANALYTICS_DEPENDENCY
    ) == 1

    assert content.count(
        "pyjnius"
    ) == 1
