from pathlib import Path


CI = Path(
    ".github/workflows/ci.yml"
)
PACKAGE_RELEASE = Path(
    ".github/workflows/release-package.yml"
)
ANDROID_RELEASE = Path(
    ".github/workflows/android-production-release.yml"
)


def test_v080_ci_runs_distribution_and_clean_install_gates():
    content = CI.read_text(
        encoding="utf-8"
    )

    required = (
        "hyperkit verify-dist",
        "hyperkit release-manifest",
        "hyperkit verify-clean-install",
        "actions/upload-artifact@v4",
    )

    for term in required:
        assert term in content


def test_v080_package_release_workflow_is_manual_and_gated():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in content
    assert "publish_target:" in content
    assert "confirm_pypi:" in content
    assert "testpypi" in content
    assert "pypi" in content
    assert (
        "inputs.confirm_pypi == true"
        in content
    )


def test_v080_package_release_runs_full_verification():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    required = (
        "pytest -q",
        "hyperkit health",
        "hyperkit validate-templates",
        "hyperkit validate-complete-games",
        "hyperkit validate-generated-projects",
        "hyperkit release-check",
        "hyperkit pre-release-audit",
        "python -m build",
        "python -m twine check dist/*",
        "hyperkit verify-dist",
        "hyperkit release-manifest",
        "hyperkit verify-clean-install",
    )

    for command in required:
        assert command in content


def test_v080_package_release_uses_trusted_publishing():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    assert (
        "pypa/gh-action-pypi-publish@release/v1"
        in content
    )
    assert "id-token: write" in content
    assert "environment: testpypi" in content
    assert "environment: pypi" in content
    assert "password:" not in content
    assert "api-token" not in content.lower()


def test_v080_publish_jobs_upload_only_python_distributions():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    assert "mkdir -p publish-dist" in content
    assert "cp dist/*.whl publish-dist/" in content
    assert "cp dist/*.tar.gz publish-dist/" in content
    assert content.count(
        "packages-dir: publish-dist/"
    ) == 2


def test_v080_real_pypi_requires_stable_version_and_matching_tag():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    assert "hyperkit publish-check --target" in content
    assert 'EXPECTED_REF="refs/tags/v$VERSION"' in content
    assert 'if [ "$GITHUB_REF" != "$EXPECTED_REF" ]' in content


def test_v080_package_release_controls_build_inputs():
    content = PACKAGE_RELEASE.read_text(
        encoding="utf-8"
    )

    assert "SOURCE_DATE_EPOCH" in content
    assert "PYTHONHASHSEED=0" in content
    assert "rm -rf build dist" in content
    assert "SHA256SUMS" in content
    assert "release-manifest.json" in content


def test_v080_android_release_workflow_is_manual_and_protected():
    content = ANDROID_RELEASE.read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in content
    assert "environment: android-production" in content
    assert "--production" in content
    assert "android-release-doctor" in content


def test_v080_android_release_targets_current_store_profile():
    content = ANDROID_RELEASE.read_text(
        encoding="utf-8"
    )

    required = (
        "android.api = 36",
        "android.ndk = 29",
        "android.release_artifact = aab",
        "p4a.branch = develop",
        'python-version: "3.14"',
        "buildozer -v android release",
    )

    for term in required:
        assert term in content


def test_v080_android_release_uses_protected_signing_inputs():
    content = ANDROID_RELEASE.read_text(
        encoding="utf-8"
    )

    required = (
        "ANDROID_KEYSTORE_BASE64",
        "ANDROID_KEYSTORE_PASSWORD",
        "ANDROID_KEY_ALIAS",
        "ANDROID_KEY_ALIAS_PASSWORD",
        "P4A_RELEASE_KEYSTORE",
        "P4A_RELEASE_KEYSTORE_PASSWD",
        "P4A_RELEASE_KEYALIAS",
        "P4A_RELEASE_KEYALIAS_PASSWD",
    )

    for term in required:
        assert term in content

    upload_section = content.split(
        "Upload signed production artifact",
        1,
    )[1]

    assert "release.keystore" not in upload_section
    assert "*.aab" in upload_section
    assert "SHA256SUMS" in upload_section
