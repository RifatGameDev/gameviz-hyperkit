from pathlib import Path

from hyperkit import format_health_report, generate_health_report


def test_health_report_passes_for_project_root():
    report = generate_health_report(".")

    assert report.total > 0
    assert report.passed_count > 0
    assert report.failed_count == 0
    assert report.passed is True


def test_health_report_has_required_docs():
    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "README.md" in paths
    assert "CHANGELOG.md" in paths
    assert "docs/TEMPLATES.md" in paths
    assert "docs/TEMPLATE_HELPERS.md" in paths
    assert "docs/RELEASE_READINESS_CHECKLIST.md" in paths
    assert "docs/PROJECT_HEALTH_REPORT.md" in paths


def test_health_report_checks_templates():
    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "src/hyperkit/templates/tap_counter/main.py" in paths
    assert "src/hyperkit/templates/flappy_mini/main.py" in paths
    assert "src/hyperkit/templates/swipe_runner/main.py" in paths
    assert "src/hyperkit/templates/puzzle_game/main.py" in paths
    assert "src/hyperkit/templates/quiz_game/main.py" in paths
    assert "src/hyperkit/templates/simple_physics/main.py" in paths


def test_health_report_format_contains_summary():
    report = generate_health_report(".")
    output = format_health_report(report)

    assert "HyperKit Project Health Report" in output
    assert "Passed:" in output
    assert "Failed:" in output
    assert "Project health status: PASS" in output


def test_health_report_detects_missing_files(tmp_path):
    report = generate_health_report(tmp_path)
    output = format_health_report(report)

    assert report.failed_count > 0
    assert report.passed is False
    assert "Project health status: FAIL" in output


def test_project_health_doc_exists():
    path = Path("docs/PROJECT_HEALTH_REPORT.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Project Health Report" in content
    assert "hyperkit health" in content
