import hyperkit


def test_phase74_package_version():
    assert hyperkit.__version__ == "1.0.0"


def test_phase74_public_api_exports():
    expected = {
        "AdConfig",
        "AdProvider",
        "AdResult",
        "AdStatus",
        "AdType",
        "MockAdProvider",
        "NoOpAdProvider",
        "AnalyticsEvent",
        "AnalyticsProvider",
        "AnalyticsResult",
        "MockAnalyticsProvider",
        "NoOpAnalyticsProvider",
        "GameSession",
        "GameSystems",
        "ProgressionTracker",
        "SessionState",
        "SessionTracker",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(hyperkit, name)
