import hyperkit


def test_phase74_firebase_analytics_public_api_exports():
    expected = {
        "AndroidAnalyticsBridge",
        "AndroidAnalyticsBuildRequirements",
        "AndroidAnalyticsProvider",
        "DEFAULT_ANDROID_ANALYTICS_PERMISSIONS",
        "MockAndroidAnalyticsBridge",
        "FIREBASE_ANALYTICS_DEPENDENCY",
        "FIREBASE_ANALYTICS_JAVA_SOURCE",
        "FirebaseAnalyticsAndroidBridge",
        "FirebaseAnalyticsAndroidProvider",
        "FirebaseAnalyticsConfig",
        "configure_firebase_analytics_android_project",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )
