from __future__ import annotations

import ast
import os
from pathlib import Path

import pytest

from hyperkit.android import (
    DEFAULT_ACCEPT_SDK_LICENSE,
    DEFAULT_ANDROID_API,
    DEFAULT_ANDROID_ARCHS,
    DEFAULT_ANDROID_HOST_PYTHON_VERSION,
    DEFAULT_ANDROID_MIN_API,
    DEFAULT_ANDROID_PYTHON_VERSION,
    create_buildozer_spec,
    generate_android_readiness_report,
)
from hyperkit.cli import create_project


ANDROID_TEMPLATES = (
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
)


def generate_project(
    tmp_path: Path,
    template_name: str,
) -> Path:
    """
    Generate one HyperKit project using the same project-generation
    path used by the existing generated-project smoke tests.
    """

    project_name = (
        f"phase73_{template_name}"
    )

    project_path = (
        tmp_path
        / project_name
    )

    current_dir = Path.cwd()

    try:
        os.chdir(tmp_path)

        create_project(
            project_name,
            template_name,
            project_path,
        )

    finally:
        os.chdir(current_dir)

    assert project_path.is_dir()

    return project_path


def android_package_name(
    template_name: str,
) -> str:
    """
    Create a deterministic Android-safe package name for a template.

    Example:
        tap_counter -> phase73tapcounter
    """

    compact = template_name.replace(
        "_",
        "",
    )

    return f"phase73{compact}"


def configure_android_project(
    project_path: Path,
    template_name: str,
) -> Path:
    """
    Generate buildozer.spec using HyperKit's validated Phase 73
    Android defaults.
    """

    readable_title = (
        template_name
        .replace("_", " ")
        .title()
    )

    return create_buildozer_spec(
        project_path,
        title=(
            f"HyperKit {readable_title}"
        ),
        package_name=(
            android_package_name(
                template_name
            )
        ),
        package_domain="org.gameviz",
        overwrite=True,
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_generate_before_android_configuration(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    assert (
        project
        / "main.py"
    ).is_file()

    assert (
        project
        / "README.md"
    ).is_file()

    assert (
        project
        / "hyperkit.toml"
    ).is_file()

    assert (
        project
        / "assets"
    ).is_dir()


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_template_main_files_have_valid_python_syntax(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    main_file = (
        project
        / "main.py"
    )

    content = main_file.read_text(
        encoding="utf-8",
    )

    ast.parse(
        content,
        filename=str(main_file),
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_accept_android_configuration(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    spec = configure_android_project(
        project,
        template_name,
    )

    assert spec.is_file()

    assert (
        spec.name
        == "buildozer.spec"
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_use_validated_android_runtime_defaults(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    spec = configure_android_project(
        project,
        template_name,
    )

    content = spec.read_text(
        encoding="utf-8",
    )

    assert (
        DEFAULT_ANDROID_API
        == 35
    )

    assert (
        DEFAULT_ANDROID_MIN_API
        == 24
    )

    assert (
        DEFAULT_ANDROID_PYTHON_VERSION
        == "3.11.9"
    )

    assert (
        DEFAULT_ANDROID_HOST_PYTHON_VERSION
        == "3.11.9"
    )

    assert (
        DEFAULT_ANDROID_ARCHS
        == (
            "arm64-v8a",
        )
    )

    assert (
        DEFAULT_ACCEPT_SDK_LICENSE
        is True
    )

    assert (
        "android.api = 35"
        in content
    )

    assert (
        "android.minapi = 24"
        in content
    )

    assert (
        "android.archs = arm64-v8a"
        in content
    )

    assert (
        "android.accept_sdk_license = True"
        in content
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_pin_validated_android_python(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    spec = configure_android_project(
        project,
        template_name,
    )

    content = spec.read_text(
        encoding="utf-8",
    )

    expected_requirements = (
        "requirements = "
        "python3==3.11.9,"
        "hostpython3==3.11.9,"
        "kivy,"
        "gameviz-hyperkit"
    )

    assert (
        expected_requirements
        in content
    )

    assert (
        "requirements = python3,kivy"
        not in content
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_generate_safe_android_identity(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    spec = configure_android_project(
        project,
        template_name,
    )

    content = spec.read_text(
        encoding="utf-8",
    )

    expected_package = (
        android_package_name(
            template_name
        )
    )

    assert (
        f"package.name = "
        f"{expected_package}"
        in content
    )

    assert (
        "package.domain = org.gameviz"
        in content
    )

    assert (
        "_" not in expected_package
    )

    assert expected_package.islower()

    assert expected_package.isalnum()


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_pass_non_strict_android_readiness(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    configure_android_project(
        project,
        template_name,
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

    failed_required = {
        check.name
        for check in report.failed_required
    }

    assert (
        failed_required
        == set()
    )


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_templates_keep_required_android_source_files(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    configure_android_project(
        project,
        template_name,
    )

    assert (
        project
        / "main.py"
    ).is_file()

    assert (
        project
        / "hyperkit.toml"
    ).is_file()

    assert (
        project
        / "buildozer.spec"
    ).is_file()

    assert (
        project
        / "assets"
        / "images"
    ).is_dir()

    assert (
        project
        / "assets"
        / "audio"
    ).is_dir()

    assert (
        project
        / "assets"
        / "fonts"
    ).is_dir()

    assert (
        project
        / "assets"
        / "data"
    ).is_dir()


@pytest.mark.parametrize(
    "template_name",
    ANDROID_TEMPLATES,
)
def test_all_android_template_specs_are_free_of_old_phase73_defaults(
    tmp_path,
    template_name,
):
    project = generate_project(
        tmp_path,
        template_name,
    )

    spec = configure_android_project(
        project,
        template_name,
    )

    content = spec.read_text(
        encoding="utf-8",
    )

    assert (
        "android.minapi = 23"
        not in content
    )

    assert (
        "python3==3.14"
        not in content
    )

    assert (
        "hostpython3==3.14"
        not in content
    )

    assert (
        "armeabi-v7a"
        not in content
    )


def test_phase73_android_template_matrix_is_complete():
    assert ANDROID_TEMPLATES == (
        "tap_counter",
        "flappy_mini",
        "swipe_runner",
        "puzzle_game",
        "quiz_game",
        "simple_physics",
    )

    assert (
        len(ANDROID_TEMPLATES)
        == 6
    )

    assert (
        len(set(ANDROID_TEMPLATES))
        == 6
    )
