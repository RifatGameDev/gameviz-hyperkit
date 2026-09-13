"""Dedicated Android toolchain CLI for GameViz HyperKit."""

from __future__ import annotations

import argparse
import platform
import shutil
import sys
from pathlib import Path

from .android_toolchain import (
    DEFAULT_ANDROID_ACTIVITY,
    AndroidToolchainError,
    build_android,
    deploy_android_artifact,
    find_android_artifacts,
    install_android_artifact,
    launch_android_app,
    list_android_devices,
    read_android_package_id,
    select_android_artifact,
    wsl_has_command,
)


def _print_artifact(
    artifact,
) -> None:
    print(
        f"- {artifact.kind.upper()}: "
        f"{artifact.path}"
    )

    print(
        f"  Size: "
        f"{artifact.size_bytes} bytes"
    )


def cmd_doctor(
    args: argparse.Namespace,
) -> int:
    print(
        "HyperKit Android Toolchain"
    )

    print(
        "--------------------------"
    )

    host = platform.system()

    print(
        f"Host: {host}"
    )

    adb = (
        shutil.which("adb")
    )

    wsl = (
        shutil.which("wsl")
        or shutil.which(
            "wsl.exe"
        )
    )

    buildozer = (
        shutil.which(
            "buildozer"
        )
    )

    print(
        "ADB: "
        f"{adb or 'not found'}"
    )

    print(
        "Local Buildozer: "
        f"{buildozer or 'not found'}"
    )

    print(
        "WSL: "
        f"{wsl or 'not found'}"
    )

    if (
        host.lower()
        == "windows"
        and wsl
    ):
        try:
            available = (
                wsl_has_command(
                    "buildozer",
                    distro=args.distro,
                )
            )

        except AndroidToolchainError:
            available = False

        print(
            "WSL Buildozer: "
            f"{'available' if available else 'not found'}"
        )

    if adb:
        try:
            devices = (
                list_android_devices()
            )

            online = [
                item
                for item in devices
                if item.is_online
            ]

            print(
                "Connected Android "
                f"devices: {len(online)}"
            )

            for device in devices:
                print(
                    f"  {device.serial} "
                    f"[{device.state}] "
                    f"{device.model or ''}"
                    .rstrip()
                )

        except AndroidToolchainError as exc:
            print(
                "ADB check: "
                f"{exc}"
            )

    return 0


def cmd_build(
    args: argparse.Namespace,
) -> int:
    result = build_android(
        args.path,
        mode=args.mode,
        distro=args.distro,
    )

    print(
        "HyperKit Android Build"
    )

    print(
        "----------------------"
    )

    print(
        "Strategy: "
        f"{result.strategy}"
    )

    print(
        "Mode: "
        f"{result.mode}"
    )

    print(
        "Project: "
        f"{result.project_path}"
    )

    if result.staged_workspace:
        print(
            "WSL workspace: "
            f"{result.staged_workspace}"
        )

    if result.returncode != 0:
        print(
            "Build failed with "
            f"exit code "
            f"{result.returncode}.",
            file=sys.stderr,
        )

        return (
            result.returncode
            or 1
        )

    print(
        "Build completed."
    )

    print(
        "Artifacts:"
    )

    for artifact in (
        result.artifacts
    ):
        _print_artifact(
            artifact
        )

    return 0


def cmd_artifacts(
    args: argparse.Namespace,
) -> int:
    artifacts = (
        find_android_artifacts(
            args.path
        )
    )

    print(
        "HyperKit Android Artifacts"
    )

    print(
        "--------------------------"
    )

    if not artifacts:
        print(
            "No APK or AAB "
            "artifacts found."
        )

        return 1

    for artifact in artifacts:
        _print_artifact(
            artifact
        )

    return 0


def cmd_devices(
    args: argparse.Namespace,
) -> int:
    devices = (
        list_android_devices()
    )

    print(
        "HyperKit Android Devices"
    )

    print(
        "------------------------"
    )

    if not devices:
        print(
            "No Android devices found."
        )

        return 1

    for device in devices:
        print(
            f"- {device.serial}"
        )

        print(
            f"  State: "
            f"{device.state}"
        )

        if device.model:
            print(
                f"  Model: "
                f"{device.model}"
            )

        if device.product:
            print(
                f"  Product: "
                f"{device.product}"
            )

    return (
        0
        if any(
            device.is_online
            for device in devices
        )
        else 1
    )


def cmd_install(
    args: argparse.Namespace,
) -> int:
    artifact = (
        select_android_artifact(
            args.path,
            artifact=args.artifact,
            prefer_kind="apk",
        )
    )

    device = (
        install_android_artifact(
            artifact,
            serial=args.serial,
        )
    )

    print(
        "Installed:"
    )

    print(
        f"  {artifact.path}"
    )

    print(
        "Device:"
    )

    print(
        f"  {device.serial}"
    )

    return 0


def cmd_run(
    args: argparse.Namespace,
) -> int:
    package_id = (
        args.package_id
        or read_android_package_id(
            args.path
        )
    )

    device = (
        launch_android_app(
            package_id,
            serial=args.serial,
            activity=args.activity,
        )
    )

    print(
        "Launched:"
    )

    print(
        f"  {package_id}"
    )

    print(
        "Device:"
    )

    print(
        f"  {device.serial}"
    )

    return 0


def cmd_deploy(
    args: argparse.Namespace,
) -> int:
    (
        artifact,
        device,
    ) = deploy_android_artifact(
        args.path,
        artifact=args.artifact,
        serial=args.serial,
        package_id=args.package_id,
        activity=args.activity,
    )

    print(
        "HyperKit Android Deployment"
    )

    print(
        "---------------------------"
    )

    print(
        "APK: "
        f"{artifact.path}"
    )

    print(
        "Device: "
        f"{device.serial}"
    )

    print(
        "Status: installed "
        "and launched"
    )

    return 0


def build_parser(
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hyperkit-android",
        description=(
            "GameViz HyperKit Android "
            "build and deployment toolchain."
        ),
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    doctor = sub.add_parser(
        "doctor",
        help=(
            "Check Android build "
            "and device tooling"
        ),
    )

    doctor.add_argument(
        "--distro",
        default=None,
        help=(
            "Optional WSL "
            "distribution name"
        ),
    )

    doctor.set_defaults(
        func=cmd_doctor
    )

    build = sub.add_parser(
        "build",
        help=(
            "Build an Android "
            "APK/AAB"
        ),
    )

    build.add_argument(
        "--path",
        default=".",
    )

    build.add_argument(
        "--mode",
        choices=[
            "debug",
            "release",
        ],
        default="debug",
    )

    build.add_argument(
        "--distro",
        default=None,
        help=(
            "Optional WSL "
            "distribution name"
        ),
    )

    build.set_defaults(
        func=cmd_build
    )

    artifacts = (
        sub.add_parser(
            "artifacts",
            help=(
                "List Android "
                "build artifacts"
            ),
        )
    )

    artifacts.add_argument(
        "--path",
        default=".",
    )

    artifacts.set_defaults(
        func=cmd_artifacts
    )

    devices = sub.add_parser(
        "devices",
        help=(
            "List ADB-connected "
            "Android devices"
        ),
    )

    devices.set_defaults(
        func=cmd_devices
    )

    install = sub.add_parser(
        "install",
        help=(
            "Install an APK "
            "on a device"
        ),
    )

    install.add_argument(
        "--path",
        default=".",
    )

    install.add_argument(
        "--artifact",
        default=None,
    )

    install.add_argument(
        "--serial",
        default=None,
    )

    install.set_defaults(
        func=cmd_install
    )

    run = sub.add_parser(
        "run",
        help=(
            "Launch the Android "
            "application"
        ),
    )

    run.add_argument(
        "--path",
        default=".",
    )

    run.add_argument(
        "--serial",
        default=None,
    )

    run.add_argument(
        "--package-id",
        default=None,
    )

    run.add_argument(
        "--activity",
        default=(
            DEFAULT_ANDROID_ACTIVITY
        ),
    )

    run.set_defaults(
        func=cmd_run
    )

    deploy = sub.add_parser(
        "deploy",
        help=(
            "Install and launch "
            "an Android APK"
        ),
    )

    deploy.add_argument(
        "--path",
        default=".",
    )

    deploy.add_argument(
        "--artifact",
        default=None,
    )

    deploy.add_argument(
        "--serial",
        default=None,
    )

    deploy.add_argument(
        "--package-id",
        default=None,
    )

    deploy.add_argument(
        "--activity",
        default=(
            DEFAULT_ANDROID_ACTIVITY
        ),
    )

    deploy.set_defaults(
        func=cmd_deploy
    )

    return parser


def main(
    argv=None,
) -> int:
    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    if not hasattr(
        args,
        "func",
    ):
        parser.print_help()

        return 0

    try:
        return args.func(
            args
        )

    except AndroidToolchainError as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )

        return 1

    except KeyboardInterrupt:
        print(
            "",
            file=sys.stderr,
        )

        print(
            "Android operation "
            "cancelled.",
            file=sys.stderr,
        )

        return 130


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
