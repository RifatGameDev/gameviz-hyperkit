import json
import tomllib
from pathlib import Path


PYPROJECT = Path("pyproject.toml")
CHANGELOG = Path("CHANGELOG.md")

EVIDENCE_ROOT = Path("docs/release-evidence/phase68")
REPORT = EVIDENCE_ROOT / "STABLE_RELEASE_READINESS.md"
RESULT = EVIDENCE_ROOT / "stable-validation.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_stable_project_metadata():
    with PYPROJECT.open("rb") as file:
        project = tomllib.load(file)["project"]

    assert project["version"] == "0.1.2"
    assert project["requires-python"] == ">=3.9"

    urls = project["urls"]
    expected_repo = "https://github.com/RifatGameDev/gameviz-hyperkit"

    assert urls["Homepage"] == expected_repo
    assert urls["Repository"] == expected_repo
    assert urls["Issues"] == f"{expected_repo}/issues"

    assert any(
        requirement.startswith("tomli")
        and "python_version < '3.11'" in requirement
        for requirement in project["dependencies"]
    )


def test_stable_version_is_documented():
    assert "## 0.1.1" in read(CHANGELOG)


def test_phase68_evidence_exists():
    assert REPORT.exists()
    assert RESULT.exists()


def test_stable_readiness_report_passed():
    content = read(REPORT)

    assert "Phase 68 result: PASS" in content
    assert "Stable artifacts approved: Yes" in content
    assert "Ready for PyPI.org publication: Yes" in content
    assert "PyPI.org publication completed: No" in content


def test_stable_validation_json_passed():
    result = json.loads(read(RESULT))

    assert result["phase"] == 68
    assert result["version"] == "0.1.1"
    assert result["status"] == "pass"

    assert result["python_matrix"] == {
        "3.9": "pass",
        "3.10": "pass",
        "3.11": "pass",
        "3.12": "pass",
    }

    assert result["release_blocking_issues"] == []
    assert result["stable_artifacts_approved"] is True
    assert result["ready_for_pypi"] is True
    assert result["published_to_pypi"] is False


def test_phase68_evidence_has_no_local_paths_or_tokens():
    forbidden = [
        "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
        "gameviz-hyperkit" + "\\src",
        "/" + "mnt/data",
        "pypi-" + "AgEI",
    ]

    for path in [REPORT, RESULT]:
        content = read(path)

        for term in forbidden:
            assert term not in content
