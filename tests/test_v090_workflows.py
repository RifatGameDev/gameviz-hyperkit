from pathlib import Path


BETA_WORKFLOW = Path(
    ".github/workflows/public-beta.yml"
)


def test_v090_public_beta_workflow_exists():
    assert BETA_WORKFLOW.is_file()


def test_v090_public_beta_workflow_is_manual():
    content = BETA_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in content
    assert "publish_testpypi:" in content


def test_v090_public_beta_runs_python_matrix():
    content = BETA_WORKFLOW.read_text(
        encoding="utf-8"
    )

    for version in (
        "3.9",
        "3.10",
        "3.11",
        "3.12",
    ):
        assert (
            f'"{version}"'
            in content
        )


def test_v090_public_beta_runs_freeze_and_release_gates():
    content = BETA_WORKFLOW.read_text(
        encoding="utf-8"
    )

    required = (
        "pytest -q",
        "hyperkit api-freeze-check",
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
        "hyperkit publish-check --target testpypi",
    )

    for command in required:
        assert command in content


def test_v090_public_beta_can_publish_only_to_testpypi():
    content = BETA_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert (
        "pypa/gh-action-pypi-publish@release/v1"
        in content
    )
    assert (
        "repository-url: https://test.pypi.org/legacy/"
        in content
    )
    assert "environment: testpypi" in content
    assert "id-token: write" in content
    assert "environment: pypi" not in content
    assert (
        "https://upload.pypi.org"
        not in content
    )


def test_v090_public_beta_requires_beta_identity():
    content = BETA_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert (
        "__version__.startswith('0.9.0b')"
        in content
    )
    assert (
        "hyperkit.API_VERSION == '1.0'"
        in content
    )
