import hyperkit


def test_phase74_admob_public_api_exports():
    expected = {
        "ADMOB_APPLICATION_ID_META_DATA",
        "ADMOB_SAMPLE_APP_ID",
        "ADMOB_SDK_DEPENDENCY",
        "ADMOB_TEST_BANNER_ID",
        "ADMOB_TEST_INTERSTITIAL_ID",
        "ADMOB_TEST_PLACEMENTS",
        "ADMOB_TEST_REWARDED_ID",
        "AdMobAndroidBridge",
        "AdMobAndroidProvider",
        "configure_admob_android_project",
        "create_admob_config",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )
