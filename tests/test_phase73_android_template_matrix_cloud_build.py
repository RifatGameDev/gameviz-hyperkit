from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "phase73-android-template-matrix.yml"
)


def read_workflow() -> str:
    assert WORKFLOW.is_file(), (
        f"Missing workflow: {WORKFLOW}"
    )

    return WORKFLOW.read_text(
        encoding="utf-8",
    )


def test_android_template_matrix_workflow_exists():
    assert WORKFLOW.is_file()


def test_android_template_matrix_is_manual():
    text = read_workflow()

    assert "workflow_dispatch:" in text


def test_android_template_matrix_does_not_replace_tap_counter_smoke():
    text = read_workflow()

    assert "template: tap-counter" not in text


def test_android_template_matrix_contains_remaining_five_templates():
    text = read_workflow()

    expected = (
        "flappy-mini",
        "swipe-runner",
        "puzzle-game",
        "quiz-game",
        "simple-physics",
    )

    for template in expected:
        assert (
            f"template: {template}"
            in text
        )


def test_android_template_matrix_has_exactly_five_templates():
    text = read_workflow()

    assert (
        text.count("          - template:")
        == 5
    )


def test_android_template_matrix_does_not_fail_fast():
    text = read_workflow()

    assert "fail-fast: false" in text


def test_android_template_matrix_uses_ubuntu():
    text = read_workflow()

    assert "runs-on: ubuntu-24.04" in text


def test_android_template_matrix_uses_python_311():
    text = read_workflow()

    assert 'python-version: "3.11"' in text


def test_android_template_matrix_installs_buildozer():
    text = read_workflow()

    assert (
        'python -m pip install "cython==0.29.34" buildozer'
        in text
    )


def test_android_template_matrix_installs_required_linux_packages():
    text = read_workflow()

    required = (
        "openjdk-17-jdk",
        "autoconf",
        "automake",
        "autopoint",
        "libtool",
        "libltdl-dev",
        "pkg-config",
        "zlib1g-dev",
        "cmake",
        "libffi-dev",
        "libssl-dev",
    )

    for package in required:
        assert package in text


def test_android_template_matrix_uses_safe_hyperkit_version_check():
    text = read_workflow()

    assert "hyperkit --version" not in text

    assert (
        "from importlib.metadata import version"
        in text
    )


def test_android_template_matrix_generates_projects():
    text = read_workflow()

    assert (
        'hyperkit new "${{ matrix.project }}"'
        in text
    )

    assert (
        '--template "${{ matrix.template }}"'
        in text
    )


def test_android_template_matrix_generates_android_configuration():
    text = read_workflow()

    assert "hyperkit init-android" in text

    assert (
        '--package-domain org.gameviz'
        in text
    )

    assert (
        "--orientation portrait"
        in text
    )

    assert "--fullscreen" in text

    assert (
        "--arch arm64-v8a"
        in text
    )


def test_android_template_matrix_checks_validated_api_levels():
    text = read_workflow()

    assert (
        "android.api = 35"
        in text
    )

    assert (
        "android.minapi = 24"
        in text
    )


def test_android_template_matrix_checks_arm64():
    text = read_workflow()

    assert (
        "android.archs = arm64-v8a"
        in text
    )


def test_android_template_matrix_checks_sdk_license():
    text = read_workflow()

    assert (
        "android.accept_sdk_license = True"
        in text
    )


def test_android_template_matrix_checks_validated_python_runtime():
    text = read_workflow()

    expected = (
        "python3==3.11.9,"
        "hostpython3==3.11.9,"
        "kivy,"
        "gameviz-hyperkit"
    )

    assert expected in text


def test_android_template_matrix_bundles_current_sdk():
    text = read_workflow()

    assert (
        'cp -a src/hyperkit "${{ matrix.project }}/hyperkit"'
        in text
    )


def test_android_template_matrix_removes_public_package_for_ci():
    text = read_workflow()

    assert (
        '"gameviz-hyperkit"'
        in text
    )

    assert (
        '"requirements = "'
        in text
    )

    assert (
        '"kivy"'
        in text
    )


def test_android_template_matrix_builds_debug_apk():
    text = read_workflow()

    assert (
        "buildozer -v android debug"
        in text
    )


def test_android_template_matrix_requires_generated_apk():
    text = read_workflow()

    assert (
        'find bin -maxdepth 1 -type f -name "*.apk"'
        in text
    )

    assert (
        "No APK was generated."
        in text
    )


def test_android_template_matrix_uploads_each_apk():
    text = read_workflow()

    assert "actions/upload-artifact@v4" in text

    assert (
        "hyperkit-${{ matrix.template }}-android-apk"
        in text
    )

    assert (
        "${{ matrix.project }}/bin/*.apk"
        in text
    )


def test_android_template_packages_are_android_safe():
    text = read_workflow()

    expected_packages = (
        "phase73flappymini",
        "phase73swiperunner",
        "phase73puzzlegame",
        "phase73quizgame",
        "phase73simplephysics",
    )

    for package in expected_packages:
        assert (
            f"package: {package}"
            in text
        )
