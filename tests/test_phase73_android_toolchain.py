from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from hyperkit.android_cli import (
    build_parser,
    main,
)
from hyperkit.android_toolchain import (
    AndroidArtifact,
    AndroidDevice,
    AndroidToolchainError,
    find_android_artifacts,
    parse_adb_devices,
    read_android_package_id,
    select_android_artifact,
    select_android_device,
    windows_path_to_wsl,
)


def test_parse_adb_devices():
    output = """
List of devices attached
emulator-5554 device product:sdk model:Pixel_8 device:emu transport_id:1
ABC123 unauthorized usb:1-1 transport_id:2
"""

    devices = (
        parse_adb_devices(
            output
        )
    )

    assert len(devices) == 2

    assert (
        devices[0].serial
        == "emulator-5554"
    )

    assert (
        devices[0].state
        == "device"
    )

    assert (
        devices[0].model
        == "Pixel_8"
    )

    assert (
        devices[1].state
        == "unauthorized"
    )


def test_select_single_online_device():
    devices = (
        AndroidDevice(
            serial="A",
            state="device",
        ),
        AndroidDevice(
            serial="B",
            state="offline",
        ),
    )

    selected = (
        select_android_device(
            devices
        )
    )

    assert (
        selected.serial
        == "A"
    )


def test_multiple_devices_require_serial():
    devices = (
        AndroidDevice(
            serial="A",
            state="device",
        ),
        AndroidDevice(
            serial="B",
            state="device",
        ),
    )

    with pytest.raises(
        AndroidToolchainError,
        match="Multiple Android devices",
    ):
        select_android_device(
            devices
        )


def test_explicit_serial_selects_device():
    devices = (
        AndroidDevice(
            serial="A",
            state="device",
        ),
        AndroidDevice(
            serial="B",
            state="device",
        ),
    )

    selected = (
        select_android_device(
            devices,
            serial="B",
        )
    )

    assert (
        selected.serial
        == "B"
    )


def test_find_android_artifacts_newest_first(
    tmp_path,
):
    bin_path = (
        tmp_path
        / "bin"
    )

    bin_path.mkdir()

    first = (
        bin_path
        / "first.apk"
    )

    second = (
        bin_path
        / "second.aab"
    )

    first.write_bytes(
        b"apk"
    )

    second.write_bytes(
        b"aab"
    )

    first.touch()

    second.touch()

    artifacts = (
        find_android_artifacts(
            tmp_path
        )
    )

    assert len(
        artifacts
    ) == 2

    assert {
        item.kind
        for item in artifacts
    } == {
        "apk",
        "aab",
    }


def test_select_android_artifact_prefers_apk(
    tmp_path,
):
    bin_path = (
        tmp_path
        / "bin"
    )

    bin_path.mkdir()

    apk = (
        bin_path
        / "game.apk"
    )

    aab = (
        bin_path
        / "game.aab"
    )

    apk.write_bytes(
        b"apk"
    )

    aab.write_bytes(
        b"aab"
    )

    selected = (
        select_android_artifact(
            tmp_path,
            prefer_kind="apk",
        )
    )

    assert (
        selected.kind
        == "apk"
    )


def test_invalid_explicit_artifact_fails(
    tmp_path,
):
    file_path = (
        tmp_path
        / "game.txt"
    )

    file_path.write_text(
        "invalid",
        encoding="utf-8",
    )

    with pytest.raises(
        AndroidToolchainError,
        match="APK or AAB",
    ):
        select_android_artifact(
            tmp_path,
            artifact=file_path,
        )


def test_read_android_package_id(
    tmp_path,
):
    (
        tmp_path
        / "buildozer.spec"
    ).write_text(
        """
[app]
title = Test Game
package.name = test_game
package.domain = com.gameviz

[buildozer]
log_level = 2
""",
        encoding="utf-8",
    )

    assert (
        read_android_package_id(
            tmp_path
        )
        == "com.gameviz.test_game"
    )


def test_cli_parser_build_command():
    parser = build_parser()

    args = parser.parse_args(
        [
            "build",
            "--mode",
            "release",
        ]
    )

    assert (
        args.command
        == "build"
    )

    assert (
        args.mode
        == "release"
    )


def test_cli_artifacts_reports_missing(
    tmp_path,
    capsys,
):
    result = main(
        [
            "artifacts",
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
        "No APK or AAB "
        "artifacts found."
        in output
    )


def test_cli_artifacts_reports_apk(
    tmp_path,
    capsys,
):
    bin_path = (
        tmp_path
        / "bin"
    )

    bin_path.mkdir()

    (
        bin_path
        / "test.apk"
    ).write_bytes(
        b"apk"
    )

    result = main(
        [
            "artifacts",
            "--path",
            str(tmp_path),
        ]
    )

    output = (
        capsys
        .readouterr()
        .out
    )

    assert result == 0

    assert (
        "test.apk"
        in output
    )

    assert (
        "APK"
        in output
    )


def test_windows_path_to_wsl(
    monkeypatch,
    tmp_path,
):
    def fake_run(
        command,
        **kwargs,
    ):
        assert (
            "wslpath"
            in command
        )

        return SimpleNamespace(
            returncode=0,
            stdout="/mnt/d/game\n",
            stderr="",
        )

    monkeypatch.setattr(
        "hyperkit.android_toolchain."
        "subprocess.run",
        fake_run,
    )

    monkeypatch.setattr(
        "hyperkit.android_toolchain."
        "resolve_wsl_executable",
        lambda executable=None: (
            "wsl.exe"
        ),
    )

    result = (
        windows_path_to_wsl(
            tmp_path
        )
    )

    assert (
        result
        == "/mnt/d/game"
    )


def test_android_artifact_dataclass():
    artifact = AndroidArtifact(
        path=Path(
            "game.apk"
        ),
        kind="apk",
        size_bytes=100,
        modified_time=1.0,
    )

    assert (
        artifact.name
        == "game.apk"
    )
