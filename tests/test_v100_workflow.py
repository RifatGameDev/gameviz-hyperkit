from pathlib import Path


STABLE_WORKFLOW = Path(
    ".github/workflows/stable-release.yml"
)
CI_WORKFLOW = Path(
    ".github/workflows/ci.yml"
)
PACKAGE_WORKFLOW = Path(
    ".github/workflows/release-package.yml"
)


def test_v100_stable_workflow_exists_and_is_manual():
    content = STABLE_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in content
    assert "publish_pypi:" in content
    assert "default: false" in content


def test_v100_stable_workflow_runs_python_matrix():
    content = STABLE_WORKFLOW.read_text(
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


def test_v100_stable_workflow_runs_all_release_gates():
    content = STABLE_WORKFLOW.read_text(
        encoding="utf-8"
    )

    required = (
        "pytest -q",
        "hyperkit api-freeze-check",
        "hyperkit stable-release-check",
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
        "hyperkit publish-check --target pypi",
        "stable-release-certificate.json",
    )

    for command in required:
        assert command in content


def test_v100_stable_workflow_protects_real_pypi_publish():
    content = STABLE_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert 'refs/tags/v1.0.1' in content
    assert "environment: pypi" in content
    assert "id-token: write" in content
    assert (
        "pypa/gh-action-pypi-publish@release/v1"
        in content
    )
    assert "password:" not in content
    assert "api-token" not in content.lower()


def test_v100_ci_enforces_stable_certification():
    content = CI_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert (
        "hyperkit stable-release-check"
        in content
    )


def test_v100_generic_release_enforces_stable_certification():
    content = PACKAGE_WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert (
        "hyperkit stable-release-check"
        in content
    )
