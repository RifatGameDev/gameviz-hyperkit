from __future__ import annotations

from pathlib import Path

import pytest

from hyperkit.android import (
    AndroidBuildConfig,
    create_buildozer_spec,
    format_android_readiness_report,
    generate_android_readiness_report,
    normalize_archs,
    normalize_permissions,
    normalized_package_domain,
    normalized_package_name,
    render_buildozer_spec,
)


def make_project(
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
        "print('hello')\n",
        encoding="utf-8",
    )

    (
        root
        / "hyperkit.toml"
    ).write_text(
        (
            '[project]\n'
            'name = "test-game"\n'
            'template = "tap-counter"\n'
        ),
        encoding="utf-8",
    )

    return root


def test_normalized_package_name():
    assert (
        normalized_package_name(
            "Tap Counter Game"
        )
        == "tap_counter_game"
    )

    assert (
        normalized_package_name(
            "123 Game"
        )
        == "game_123_game"
    )

    assert (
        normalized_package_name(
            "!!!"
        )
        == "hyperkit_game"
    )


def test_normalized_package_domain():
    assert (
        normalized_package_domain(
            "org.GameViz"
        )
        == "org.gameviz"
    )

    assert (
        normalized_package_domain(
            "gameviz"
        )
        == "org.gameviz"
    )

    assert (
        normalized_package_domain(
            ""
        )
        == "org.gameviz"
    )


def test_normalize_permissions_and_archs():
    assert (
        normalize_permissions(
            [
                " internet ",
                "VIBRATE",
                "internet",
                "",
            ]
        )
        == (
            "INTERNET",
            "VIBRATE",
        )
    )

    assert (
        normalize_archs(
            [
                "arm64-v8a",
                " armeabi-v7a ",
                "arm64-v8a",
            ]
        )
        == (
            "arm64-v8a",
            "armeabi-v7a",
        )
    )


def test_android_build_config_validates_orientation():
    with pytest.raises(
        ValueError,
        match=(
            "Unsupported "
            "Android orientation"
        ),
    ):
        AndroidBuildConfig(
            orientation="sideways"
        )


def test_android_build_config_rejects_invalid_api_range():
    with pytest.raises(
        ValueError,
        match=(
            "min_api cannot "
            "be greater"
        ),
    ):
        AndroidBuildConfig(
            android_api=23,
            min_api=24,
        )


def test_render_buildozer_spec_contains_mobile_settings():
    config = AndroidBuildConfig(
        title="Tap Counter",
        package_domain="com.gameviz",
        version="1.2.3",
        orientation="landscape",
        fullscreen=True,
        permissions=(
            "INTERNET",
            "VIBRATE",
        ),
        android_api=35,
        min_api=23,
        archs=(
            "arm64-v8a",
        ),
    )

    content = render_buildozer_spec(
        config
    )

    assert (
        "title = Tap Counter"
        in content
    )

    assert (
        "package.name = tap_counter"
        in content
    )

    assert (
        "package.domain = com.gameviz"
        in content
    )

    assert (
        "version = 1.2.3"
        in content
    )

    assert (
        "requirements = "
        "python3,kivy,gameviz-hyperkit"
        in content
    )

    assert (
        "orientation = landscape"
        in content
    )

    assert (
        "fullscreen = 1"
        in content
    )

    assert (
        "android.permissions = "
        "INTERNET,VIBRATE"
        in content
    )

    assert (
        "android.api = 35"
        in content
    )

    assert (
        "android.minapi = 23"
        in content
    )

    assert (
        "android.archs = arm64-v8a"
        in content
    )

    assert (
        "android.ndk ="
        not in content
    )


def test_create_buildozer_spec(
    tmp_path,
):
    path = create_buildozer_spec(
        tmp_path,
        title="Tap Counter",
    )

    assert path.exists()

    content = path.read_text(
        encoding="utf-8"
    )

    assert (
        "package.name = tap_counter"
        in content
    )

    assert (
        "package.domain = org.gameviz"
        in content
    )

    assert (
        "requirements = "
        "python3,kivy,gameviz-hyperkit"
        in content
    )

    assert (
        "orientation = portrait"
        in content
    )

    assert (
        "fullscreen = 0"
        in content
    )

    assert (
        "android.permissions = VIBRATE"
        in content
    )


def test_create_buildozer_spec_supports_custom_mobile_config(
    tmp_path,
):
    path = create_buildozer_spec(
        tmp_path,
        title="Runner Pro",
        package_name="runner_pro",
        package_domain="com.gameviz",
        version="2.0.0",
        orientation="landscape",
        fullscreen=True,
        permissions=(
            "INTERNET",
            "VIBRATE",
        ),
        android_api=35,
        min_api=24,
        ndk="25b",
        archs=(
            "arm64-v8a",
        ),
    )

    content = path.read_text(
        encoding="utf-8"
    )

    assert (
        "package.name = runner_pro"
        in content
    )

    assert (
        "package.domain = com.gameviz"
        in content
    )

    assert (
        "version = 2.0.0"
        in content
    )

    assert (
        "orientation = landscape"
        in content
    )

    assert (
        "fullscreen = 1"
        in content
    )

    assert (
        "android.permissions = "
        "INTERNET,VIBRATE"
        in content
    )

    assert (
        "android.minapi = 24"
        in content
    )

    assert (
        "android.ndk = 25b"
        in content
    )

    assert (
        "android.archs = arm64-v8a"
        in content
    )


def test_create_buildozer_spec_does_not_overwrite_by_default(
    tmp_path,
):
    spec = (
        tmp_path
        / "buildozer.spec"
    )

    spec.write_text(
        "original\n",
        encoding="utf-8",
    )

    returned = create_buildozer_spec(
        tmp_path,
        title="Replacement",
    )

    assert returned == spec

    assert (
        spec.read_text(
            encoding="utf-8"
        )
        == "original\n"
    )


def test_create_buildozer_spec_can_overwrite(
    tmp_path,
):
    spec = (
        tmp_path
        / "buildozer.spec"
    )

    spec.write_text(
        "original\n",
        encoding="utf-8",
    )

    create_buildozer_spec(
        tmp_path,
        title="Replacement",
        overwrite=True,
    )

    content = spec.read_text(
        encoding="utf-8"
    )

    assert (
        "title = Replacement"
        in content
    )

    assert (
        content
        != "original\n"
    )


def test_android_readiness_passes_project_configuration_without_strict_tools(
    tmp_path,
):
    project = make_project(
        tmp_path
        / "game"
    )

    create_buildozer_spec(
        project,
        title="Game",
    )

    report = (
        generate_android_readiness_report(
            project,
            require_build_tools=False,
        )
    )

    assert (
        report.passed
        is True
    )

    output = (
        format_android_readiness_report(
            report
        )
    )

    assert (
        "HyperKit Android Readiness"
        in output
    )

    assert (
        "Buildozer configuration"
        in output
    )

    assert (
        "Android readiness: PASS"
        in output
    )


def test_android_readiness_fails_when_project_files_are_missing(
    tmp_path,
):
    report = (
        generate_android_readiness_report(
            tmp_path,
            require_build_tools=False,
        )
    )

    assert (
        report.passed
        is False
    )

    failed_names = {
        check.name
        for check
        in report.failed_required
    }

    assert (
        "Main entry point"
        in failed_names
    )

    assert (
        "HyperKit project metadata"
        in failed_names
    )

    assert (
        "Buildozer configuration"
        in failed_names
    )
