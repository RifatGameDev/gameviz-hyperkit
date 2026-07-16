from pathlib import Path

from hyperkit import (
    format_pre_release_audit_report,
    generate_pre_release_audit_report,
)


def test_pre_release_audit_passes_for_project_root():
    report = generate_pre_release_audit_report(".")

    assert report.total > 0
    assert report.failed_count == 0
    assert report.passed is True


def test_pre_release_audit_contains_core_checks():
    report = generate_pre_release_audit_report(".")
    check_names = {check.name for check in report.checks}

    assert "Release readiness report" in check_names
    assert "No temporary cleanup scripts" in check_names
    assert "No local machine paths leaked" in check_names
    assert "Markdown code fences are balanced" in check_names
    assert "README links important docs" in check_names


def test_pre_release_audit_format_contains_summary():
    report = generate_pre_release_audit_report(".")
    output = format_pre_release_audit_report(report)

    assert "HyperKit Final Pre-release Audit" in output
    assert "Passed:" in output
    assert "Failed: 0" in output
    assert "Final pre-release audit status: PASS" in output


def test_pre_release_audit_detects_missing_project(tmp_path):
    report = generate_pre_release_audit_report(tmp_path)
    output = format_pre_release_audit_report(report)

    assert report.failed_count > 0
    assert report.passed is False
    assert "Final pre-release audit status: FAIL" in output


def test_final_pre_release_audit_doc_exists():
    path = Path("docs/FINAL_PRE_RELEASE_AUDIT.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Final Pre-release Audit" in content
    assert "hyperkit pre-release-audit" in content
    assert "twine check dist/*" in content


def test_main_readme_links_final_pre_release_audit():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Final Pre-release Audit" in content
    assert "docs/FINAL_PRE_RELEASE_AUDIT.md" in content


def test_readme_has_no_literal_escaped_newline_artifacts():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "\\n" not in content
