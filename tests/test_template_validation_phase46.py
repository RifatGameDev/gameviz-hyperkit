from pathlib import Path

from hyperkit import (
    format_template_validation_report,
    generate_template_validation_report,
)
from hyperkit.cli import main


EXPECTED_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def test_template_validation_report_passes_for_repo_root():
    report = generate_template_validation_report(".")

    assert report.total > 0
    assert report.failed_count == 0
    assert report.passed is True


def test_template_validation_report_checks_all_templates():
    report = generate_template_validation_report(".")
    checked_templates = {check.template for check in report.checks}

    for template in EXPECTED_TEMPLATES:
        assert template in checked_templates


def test_template_validation_report_format_contains_summary():
    report = generate_template_validation_report(".")
    output = format_template_validation_report(report)

    assert "HyperKit Template Validation Report" in output
    assert "Passed:" in output
    assert "Failed: 0" in output
    assert "Template validation status: PASS" in output


def test_template_validation_command_passes(capsys):
    exit_code = main(["validate-templates"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "HyperKit Template Validation Report" in captured.out
    assert "Template validation status: PASS" in captured.out


def test_template_validation_command_fails_for_missing_root(tmp_path, capsys):
    exit_code = main(["validate-templates", "--path", str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Template validation status: FAIL" in captured.out


def test_template_validation_docs_exist():
    path = Path("docs/TEMPLATE_VALIDATION.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Template Validation" in content
    assert "hyperkit validate-templates" in content
    assert "main.py has valid Python syntax" in content


def test_readme_links_template_validation_docs():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Template Validation" in content
    assert "docs/TEMPLATE_VALIDATION.md" in content
    assert "hyperkit validate-templates" in content


def test_health_checks_include_template_validation_docs():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "src/hyperkit/template_validation.py" in paths
    assert "docs/TEMPLATE_VALIDATION.md" in paths
    assert "tests/test_template_validation_phase46.py" in paths


def test_release_checks_include_template_validation_docs():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/TEMPLATE_VALIDATION.md" in check_names
    assert "Required release test: tests/test_template_validation_phase46.py" in check_names


def test_template_validation_detects_missing_templates(tmp_path):
    report = generate_template_validation_report(tmp_path)

    assert report.failed_count > 0
    assert report.passed is False
