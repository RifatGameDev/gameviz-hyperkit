from hyperkit.analytics import (
    AnalyticsEvent,
    AnalyticsService,
)
from hyperkit.analytics.android import (
    AndroidAnalyticsBuildRequirements,
    AndroidAnalyticsProvider,
    DEFAULT_ANDROID_ANALYTICS_PERMISSIONS,
    MockAndroidAnalyticsBridge,
)


def test_android_analytics_build_requirements_have_network_permissions():
    requirements = (
        AndroidAnalyticsBuildRequirements()
    )

    assert (
        requirements.permissions
        == DEFAULT_ANDROID_ANALYTICS_PERMISSIONS
    )

    assert (
        requirements.permissions
        == (
            "INTERNET",
            "ACCESS_NETWORK_STATE",
        )
    )


def test_android_analytics_provider_initializes_bridge():
    bridge = MockAndroidAnalyticsBridge()
    provider = AndroidAnalyticsProvider(
        bridge
    )

    result = provider.initialize()

    assert result.success
    assert provider.initialized
    assert (
        provider.bridge_name
        == "mock-android-analytics"
    )


def test_android_analytics_provider_tracks_events():
    bridge = MockAndroidAnalyticsBridge()
    provider = AndroidAnalyticsProvider(
        bridge
    )

    provider.initialize()

    result = provider.track_event(
        AnalyticsEvent(
            "level_complete",
            {
                "level": 3,
                "score": 120,
            },
        )
    )

    assert result.success
    assert len(bridge.events) == 1
    assert (
        bridge.events[0].name
        == "level_complete"
    )


def test_android_analytics_provider_is_safe_before_initialize():
    provider = AndroidAnalyticsProvider(
        MockAndroidAnalyticsBridge()
    )

    result = provider.track_event(
        AnalyticsEvent(
            "game_start"
        )
    )

    assert not result.success


def test_analytics_service_can_use_android_provider_on_desktop():
    bridge = MockAndroidAnalyticsBridge()

    analytics = AnalyticsService(
        AndroidAnalyticsProvider(
            bridge
        )
    )

    result = analytics.game_start(
        mode="runner"
    )

    assert result.success
    assert (
        bridge.events[0]
        .properties
    ) == {
        "mode": "runner",
    }


def test_android_analytics_provider_flushes_bridge():
    bridge = MockAndroidAnalyticsBridge()
    provider = AndroidAnalyticsProvider(
        bridge
    )

    provider.initialize()

    assert provider.flush().success
    assert bridge.flush_count == 1


def test_android_analytics_provider_exposes_build_requirements():
    requirements = (
        AndroidAnalyticsBuildRequirements(
            permissions=(
                "INTERNET",
            ),
            python_requirements=(
                "pyjnius",
            ),
            gradle_dependencies=(
                "com.example:analytics:1.0",
            ),
            java_source_dirs=(
                "android_src",
            ),
            enable_androidx=True,
        )
    )

    provider = AndroidAnalyticsProvider(
        MockAndroidAnalyticsBridge(
            build_requirements=(
                requirements
            )
        )
    )

    assert (
        provider.build_requirements
        == requirements
    )
