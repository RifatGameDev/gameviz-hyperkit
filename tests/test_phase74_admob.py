from pathlib import Path

from hyperkit.ads import (
    AdStatus,
    AdType,
)
from hyperkit.ads.admob import (
    ADMOB_APPLICATION_ID_META_DATA,
    ADMOB_SAMPLE_APP_ID,
    ADMOB_SDK_DEPENDENCY,
    ADMOB_TEST_BANNER_ID,
    ADMOB_TEST_INTERSTITIAL_ID,
    ADMOB_TEST_REWARDED_ID,
    AdMobAndroidBridge,
    AdMobAndroidProvider,
    configure_admob_android_project,
    create_admob_config,
)
from hyperkit.android import (
    create_buildozer_spec,
)


def test_admob_config_uses_google_demo_units_in_test_mode():
    config = create_admob_config()

    assert config.test_mode
    assert (
        config.placements["banner"]
        == ADMOB_TEST_BANNER_ID
    )
    assert (
        config.placements["interstitial"]
        == ADMOB_TEST_INTERSTITIAL_ID
    )
    assert (
        config.placements["rewarded"]
        == ADMOB_TEST_REWARDED_ID
    )
    assert (
        config.placements["game_over"]
        == ADMOB_TEST_INTERSTITIAL_ID
    )
    assert (
        config.placements["revive"]
        == ADMOB_TEST_REWARDED_ID
    )


def test_admob_config_allows_production_placements():
    config = create_admob_config(
        app_id="ca-app-pub-demo~app",
        test_mode=False,
        placements={
            "game_over": "prod-interstitial",
        },
    )

    assert not config.test_mode
    assert config.placements == {
        "game_over": "prod-interstitial",
    }
    assert (
        config.provider_options["app_id"]
        == "ca-app-pub-demo~app"
    )


def test_admob_bridge_declares_android_build_requirements():
    bridge = AdMobAndroidBridge()

    requirements = (
        bridge.build_requirements
    )

    assert (
        ADMOB_SDK_DEPENDENCY
        in requirements.gradle_dependencies
    )

    assert (
        requirements.meta_data[
            ADMOB_APPLICATION_ID_META_DATA
        ]
        == ADMOB_SAMPLE_APP_ID
    )

    assert (
        "pyjnius"
        in requirements.python_requirements
    )

    assert (
        requirements.java_source_dirs
        == ("android_src",)
    )

    assert requirements.enable_androidx


def test_admob_provider_maps_common_test_placements():
    provider = AdMobAndroidProvider()

    assert (
        provider.config.placement_id(
            "game_over"
        )
        == ADMOB_TEST_INTERSTITIAL_ID
    )

    assert (
        provider.config.placement_id(
            "revive"
        )
        == ADMOB_TEST_REWARDED_ID
    )

    assert provider.provider_name == "admob"


def test_admob_bridge_fails_cleanly_on_desktop():
    bridge = AdMobAndroidBridge()

    result = bridge.initialize(
        create_admob_config()
    )

    assert not result.success
    assert result.status == AdStatus.FAILED
    assert not bridge.initialized


def test_configure_admob_android_project_updates_buildozer_spec(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="AdMob Smoke",
    )

    spec_path, java_path = (
        configure_admob_android_project(
            tmp_path
        )
    )

    content = spec_path.read_text(
        encoding="utf-8",
    )

    assert (
        ADMOB_SDK_DEPENDENCY
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
        "android.meta_data = "
        f"{ADMOB_APPLICATION_ID_META_DATA}"
        f"={ADMOB_SAMPLE_APP_ID}"
        in content
    )

    assert (
        "android.gradle_dependencies = "
        f"{ADMOB_SDK_DEPENDENCY}"
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
        "class HyperKitAdMob"
        in java
    )

    assert (
        "InterstitialAd.load"
        in java
    )

    assert (
        "RewardedAd.load"
        in java
    )

    assert (
        "MobileAds.initialize"
        in java
    )


def test_configure_admob_android_project_is_idempotent(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="AdMob Smoke",
    )

    configure_admob_android_project(
        tmp_path
    )

    configure_admob_android_project(
        tmp_path
    )

    content = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8",
    )

    assert content.count(
        ADMOB_SDK_DEPENDENCY
    ) == 1

    assert content.count(
        "pyjnius"
    ) == 1

    assert content.count(
        ADMOB_APPLICATION_ID_META_DATA
    ) == 1


def test_admob_provider_requires_known_placement_by_default():
    provider = AdMobAndroidProvider(
        placements={
            "menu": ADMOB_TEST_BANNER_ID,
        }
    )

    provider.initialized = True
    provider.bridge.initialized = True

    try:
        provider.is_available(
            AdType.INTERSTITIAL,
            "missing",
        )

    except ValueError as exc:
        assert "not mapped" in str(
            exc
        )

    else:
        raise AssertionError(
            "Expected unmapped placement "
            "to be rejected."
        )
