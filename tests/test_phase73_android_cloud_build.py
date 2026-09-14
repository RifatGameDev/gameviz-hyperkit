from __future__ import annotations

from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "phase73-android-smoke.yml"
)


def read_workflow() -> str:
    assert WORKFLOW.is_file()

    return WORKFLOW.read_text(
        encoding="utf-8"
    )


def test_android_cloud_workflow_exists():
    assert WORKFLOW.is_file()


def test_android_cloud_workflow_is_manual():
    text = read_workflow()

    assert (
        "workflow_dispatch:"
        in text
    )


def test_android_cloud_uses_ubuntu_2404():
    text = read_workflow()

    assert (
        "runs-on: ubuntu-24.04"
        in text
    )


def test_android_cloud_uses_python_311():
    text = read_workflow()

    assert (
        'python-version: "3.11"'
        in text
    )


def test_android_cloud_installs_java_17():
    text = read_workflow()

    assert (
        "openjdk-17-jdk"
        in text
    )


def test_android_cloud_installs_buildozer():
    text = read_workflow()

    assert (
        "buildozer"
        in text
    )

    assert (
        "cython==0.29.34"
        in text
    )


def test_android_cloud_generates_hyperkit_project():
    text = read_workflow()

    assert (
        "hyperkit new "
        "phase73-android-smoke"
        in text
    )

    assert (
        "--template tap-counter"
        in text
    )


def test_android_cloud_uses_safe_package_name():
    text = read_workflow()

    assert (
        "--package-name phase73smoke"
        in text
    )

    assert (
        "--package-domain org.gameviz"
        in text
    )


def test_android_cloud_builds_single_arm64_target():
    text = read_workflow()

    assert (
        "--arch arm64-v8a"
        in text
    )


def test_android_cloud_bundles_current_sdk():
    text = read_workflow()

    assert (
        "cp -a src/hyperkit "
        "phase73-android-smoke/hyperkit"
        in text
    )

    assert (
        '"gameviz-hyperkit"'
        in text
    )


def test_android_cloud_builds_debug_apk():
    text = read_workflow()

    assert (
        "buildozer -v android debug"
        in text
    )


def test_android_cloud_uploads_apk():
    text = read_workflow()

    assert (
        "actions/upload-artifact@v4"
        in text
    )

    assert (
        "phase73-android-smoke/bin/*.apk"
        in text
    )

    assert (
        "hyperkit-phase73-android-smoke-apk"
        in text
    )


def test_android_cloud_runs_on_phase73_branch():
    text = read_workflow()

    assert (
        "push:"
        in text
    )

    assert (
        "feature/phase73-android-mobile"
        in text
    )
