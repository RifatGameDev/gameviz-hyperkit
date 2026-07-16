from pathlib import Path

from hyperkit import format_release_report, generate_release_report


def test_release_report_passes_for_project_root():
    report = generate_release_report(".")

    assert report.total > 0
    assert report.failed_count == 0
    assert report.passed is True


def test_release_report_contains_required_files():
    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: README.md" in check_names
    assert "Required release file: CHANGELOG.md" in check_names
    assert "Required release file: pyproject.toml" in check_names
    assert "Required release file: docs/RELEASE_READINESS_CHECKLIST.md" in check_names
    assert "Required release file: docs/RELEASE_BUILD_AUTOMATION.md" in check_names


def test_release_report_contains_required_tests():
    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release test: tests/test_template_quality_phase34.py" in check_names
    assert "Required release test: tests/test_release_readiness_phase35.py" in check_names
    assert "Required release test: tests/test_generated_project_smoke_phase37.py" in check_names
    assert "Required release test: tests/test_health_phase38.py" in check_names


def test_release_report_format_contains_summary():
    report = generate_release_report(".")
    output = format_release_report(report)

    assert "HyperKit Release Readiness Report" in output
    assert "Passed:" in output
    assert "Failed: 0" in output
    assert "Release readiness status: PASS" in output


def test_release_build_automation_doc_exists():
    path = Path("docs/RELEASE_BUILD_AUTOMATION.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Release Build Automation" in content
    assert "hyperkit release-check" in content
    assert "python -m build" in content
    assert "twine check dist/*" in content


def test_main_readme_links_release_build_automation():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Release Build Automation" in content
    assert "docs/RELEASE_BUILD_AUTOMATION.md" in content
