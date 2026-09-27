import hyperkit


def test_phase74_android_ads_public_api_exports():
    expected = {
        "AndroidAdBridge",
        "AndroidAdBuildRequirements",
        "AndroidAdProvider",
        "DEFAULT_ANDROID_AD_PERMISSIONS",
        "MockAndroidAdBridge",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )


def test_phase74_android_ads_are_available_from_ads_package():
    from hyperkit.ads import (
        AndroidAdBridge,
        AndroidAdBuildRequirements,
        AndroidAdProvider,
        DEFAULT_ANDROID_AD_PERMISSIONS,
        MockAndroidAdBridge,
    )

    assert (
        AndroidAdBridge
        is hyperkit.AndroidAdBridge
    )

    assert (
        AndroidAdBuildRequirements
        is hyperkit.AndroidAdBuildRequirements
    )

    assert (
        AndroidAdProvider
        is hyperkit.AndroidAdProvider
    )

    assert (
        DEFAULT_ANDROID_AD_PERMISSIONS
        is hyperkit.DEFAULT_ANDROID_AD_PERMISSIONS
    )

    assert (
        MockAndroidAdBridge
        is hyperkit.MockAndroidAdBridge
    )
