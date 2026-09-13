from __future__ import annotations

from hyperkit.cli import (
    build_parser,
    main,
)


def test_cli_exposes_android_doctor():
    parser = build_parser()

    args = parser.parse_args(
        [
            "android-doctor",
        ]
    )

    assert (
        args.command
        == "android-doctor"
    )

    assert (
        args.strict
        is False
    )


def test_cli_init_android_accepts_mobile_options(
    tmp_path,
):
    result = main(
        [
            "init-android",
            "--path",
            str(tmp_path),
            "--title",
            "Mobile Test",
            "--package-domain",
            "com.gameviz",
            "--app-version",
            "1.0.0",
            "--orientation",
            "landscape",
            "--fullscreen",
            "--permission",
            "INTERNET",
            "--permission",
            "VIBRATE",
            "--android-api",
            "35",
            "--min-api",
            "23",
            "--arch",
            "arm64-v8a",
        ]
    )

    assert result == 0

    content = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "title = Mobile Test"
        in content
    )

    assert (
        "package.domain = com.gameviz"
        in content
    )

    assert (
        "version = 1.0.0"
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
        "android.archs = arm64-v8a"
        in content
    )


def test_android_doctor_reports_missing_project_requirements(
    tmp_path,
    capsys,
):
    result = main(
        [
            "android-doctor",
            "--path",
            str(tmp_path),
        ]
    )

    output = (
        capsys
        .readouterr()
        .out
    )

    assert result == 1

    assert (
        "HyperKit Android Readiness"
        in output
    )

    assert (
        "Missing main.py"
        in output
    )

    assert (
        "Missing hyperkit.toml"
        in output
    )

    assert (
        "Missing buildozer.spec"
        in output
    )


def test_android_doctor_passes_after_project_and_spec_exist(
    tmp_path,
    capsys,
):
    (
        tmp_path
        / "main.py"
    ).write_text(
        "print('game')\n",
        encoding="utf-8",
    )

    (
        tmp_path
        / "hyperkit.toml"
    ).write_text(
        (
            '[project]\n'
            'name = "mobile-test"\n'
            'template = "tap-counter"\n'
        ),
        encoding="utf-8",
    )

    init_result = main(
        [
            "init-android",
            "--path",
            str(tmp_path),
            "--title",
            "Mobile Test",
        ]
    )

    assert (
        init_result
        == 0
    )

    capsys.readouterr()

    doctor_result = main(
        [
            "android-doctor",
            "--path",
            str(tmp_path),
        ]
    )

    output = (
        capsys
        .readouterr()
        .out
    )

    assert (
        doctor_result
        == 0
    )

    assert (
        "Android readiness: PASS"
        in output
    )


def test_build_parser_supports_debug_and_release_android_modes():
    parser = build_parser()

    debug_args = (
        parser.parse_args(
            [
                "build",
                "android",
            ]
        )
    )

    release_args = (
        parser.parse_args(
            [
                "build",
                "android",
                "--mode",
                "release",
            ]
        )
    )

    assert (
        debug_args.mode
        == "debug"
    )

    assert (
        release_args.mode
        == "release"
    )
