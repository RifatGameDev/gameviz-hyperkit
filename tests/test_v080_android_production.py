from pathlib import Path

from hyperkit.android import (
    DEFAULT_ANDROID_API,
    PRODUCTION_ANDROID_API,
    PRODUCTION_ANDROID_NDK,
    PRODUCTION_P4A_BRANCH,
    PRODUCTION_RELEASE_ARTIFACT,
    PRODUCTION_REQUIREMENTS,
    AndroidBuildConfig,
    create_production_buildozer_spec,
)
from hyperkit.android_release import (
    P4A_RELEASE_SIGNING_VARIABLES,
    generate_android_production_readiness_report,
)


def create_project(
    root: Path,
) -> Path:
    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        root
        / "main.py"
    ).write_text(
        "print('game')\n",
        encoding="utf-8",
    )

    (
        root
        / "hyperkit.toml"
    ).write_text(
        (
            "[project]\n"
            'name = "game"\n'
            'template = "tap-counter"\n'
        ),
        encoding="utf-8",
    )

    return root


def test_v080_preserves_validated_debug_default():
    assert DEFAULT_ANDROID_API == 35

    config = AndroidBuildConfig()

    assert config.android_api == 35


def test_v080_production_android_constants():
    assert PRODUCTION_ANDROID_API == 36
    assert PRODUCTION_ANDROID_NDK == "29"
    assert PRODUCTION_P4A_BRANCH == "develop"
    assert PRODUCTION_RELEASE_ARTIFACT == "aab"
    assert PRODUCTION_REQUIREMENTS == (
        "python3",
        "kivy",
        "gameviz-hyperkit",
    )


def test_production_buildozer_spec_uses_store_profile(
    tmp_path: Path,
):
    project = create_project(
        tmp_path
        / "game"
    )

    spec = create_production_buildozer_spec(
        project,
        title="Release Game",
        package_name="releasegame",
        package_domain="com.gameviz",
        version="1.0.0",
        overwrite=True,
    )

    text = spec.read_text(
        encoding="utf-8"
    )

    assert "android.api = 36" in text
    assert "android.minapi = 24" in text
    assert "android.ndk = 29" in text
    assert "android.release_artifact = aab" in text
    assert "p4a.branch = develop" in text
    assert (
        "requirements = "
        "python3,kivy,gameviz-hyperkit"
        in text
    )


def test_production_readiness_passes_with_signing_inputs(
    tmp_path: Path,
):
    project = create_project(
        tmp_path
        / "game"
    )
    create_production_buildozer_spec(
        project,
        overwrite=True,
    )

    keystore = (
        tmp_path
        / "release.keystore"
    )
    keystore.write_bytes(
        b"fake-keystore"
    )

    environment = {
        "P4A_RELEASE_KEYSTORE": (
            str(
                keystore
            )
        ),
        "P4A_RELEASE_KEYSTORE_PASSWD": "secret",
        "P4A_RELEASE_KEYALIAS": "release",
        "P4A_RELEASE_KEYALIAS_PASSWD": "secret",
    }

    report = (
        generate_android_production_readiness_report(
            project,
            environment=environment,
        )
    )

    assert report.passed
    assert not report.failed_checks


def test_production_readiness_never_requires_secret_values_in_messages(
    tmp_path: Path,
):
    project = create_project(
        tmp_path
        / "game"
    )
    create_production_buildozer_spec(
        project,
        overwrite=True,
    )

    environment = {
        name: ""
        for name
        in P4A_RELEASE_SIGNING_VARIABLES
    }

    report = (
        generate_android_production_readiness_report(
            project,
            environment=environment,
        )
    )

    assert not report.passed

    messages = "\n".join(
        check.message
        for check in report.checks
    )

    assert "secret" not in messages.lower()
    assert "P4A_RELEASE_KEYSTORE" in messages


def test_android_build_config_rejects_invalid_release_artifact():
    try:
        AndroidBuildConfig(
            release_artifact="zip"
        )
    except ValueError as exc:
        assert "release_artifact" in str(
            exc
        )
    else:
        raise AssertionError(
            "Expected invalid release artifact to fail"
        )
