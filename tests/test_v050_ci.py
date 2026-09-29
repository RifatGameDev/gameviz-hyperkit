from pathlib import Path


WORKFLOW = Path(
    ".github/workflows/ci.yml"
)


def test_v050_ci_workflow_exists():
    assert WORKFLOW.exists()


def test_v050_ci_covers_supported_python_versions():
    content = WORKFLOW.read_text(
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


def test_v050_ci_runs_core_validation_commands():
    content = WORKFLOW.read_text(
        encoding="utf-8"
    )

    required = (
        "pytest -q",
        "hyperkit validate-templates",
        "hyperkit validate-complete-games",
        "hyperkit validate-generated-projects",
        "hyperkit release-check",
    )

    for command in required:
        assert command in content



def test_v050_ci_builds_and_checks_distribution():
    content = WORKFLOW.read_text(
        encoding="utf-8"
    )

    assert "python -m build" in content
    assert "python -m twine check dist/*" in content
