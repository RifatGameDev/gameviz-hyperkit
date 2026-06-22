from __future__ import annotations

from pathlib import Path


BUILDOZER_SPEC_TEMPLATE = """[app]
title = {title}
package.name = {package_name}
package.domain = org.gameviz

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,mp3,ogg

version = 0.1.0
requirements = python3,kivy,gameviz-hyperkit

orientation = portrait
fullscreen = 0

android.permissions = VIBRATE
android.api = 35
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
"""


def normalized_package_name(title: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in title).strip("_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned or "hyperkit_game"


def create_buildozer_spec(path: str | Path = ".", title: str = "HyperKit Game", overwrite: bool = False) -> Path:
    root = Path(path)
    spec_path = root / "buildozer.spec"
    if spec_path.exists() and not overwrite:
        return spec_path

    package_name = normalized_package_name(title)
    spec_path.write_text(
        BUILDOZER_SPEC_TEMPLATE.format(title=title, package_name=package_name),
        encoding="utf-8",
    )
    return spec_path
