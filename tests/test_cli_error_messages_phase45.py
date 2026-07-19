import pytest

from hyperkit.cli import (
    main,
    suggest_template_name,
    validate_template_name,
)


def test_template_suggestion_for_close_name():
    assert suggest_template_name("tapcounter") == "tap-counter"


def test_invalid_template_error_has_suggestion():
    with pytest.raises(ValueError) as exc_info:
        validate_template_name("tapcounter")

    message = str(exc_info.value)

    assert "Unknown template 'tapcounter'" in message
    assert "Available templates:" in message
    assert "Did you mean 'tap-counter'?" in message
    assert "hyperkit list-templates" in message


def test_empty_template_error_is_clear():
    with pytest.raises(ValueError) as exc_info:
        validate_template_name("")

    message = str(exc_info.value)

    assert "Template name is required" in message
    assert "hyperkit list-templates" in message


def test_cli_new_invalid_template_prints_helpful_error(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["new", "demo-game", "--template", "tapcounter"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown template 'tapcounter'" in captured.err
    assert "Did you mean 'tap-counter'?" in captured.err


def test_cli_run_missing_project_path_prints_tip(capsys, tmp_path):
    missing_path = tmp_path / "missing-project"

    exit_code = main(["run", "--path", str(missing_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Project path does not exist" in captured.err
    assert "hyperkit run --path path/to/project" in captured.err


def test_cli_run_missing_main_file_prints_tip(capsys, tmp_path):
    exit_code = main(["run", "--path", str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Could not find main.py" in captured.err
    assert "generated HyperKit project" in captured.err
    assert "hyperkit run --path path/to/project" in captured.err


def test_cli_error_docs_exist():
    from pathlib import Path

    path = Path("docs/CLI_ERROR_MESSAGES.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "CLI Error Messages" in content
    assert "Unknown Template" in content
    assert "Missing main.py" in content
    assert "hyperkit list-templates" in content


def test_readme_links_cli_error_docs():
    from pathlib import Path

    content = Path("README.md").read_text(encoding="utf-8")

    assert "CLI Error Messages" in content
    assert "docs/CLI_ERROR_MESSAGES.md" in content


def test_health_checks_include_cli_error_docs():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/CLI_ERROR_MESSAGES.md" in paths
    assert "tests/test_cli_error_messages_phase45.py" in paths


def test_release_checks_include_cli_error_docs():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/CLI_ERROR_MESSAGES.md" in check_names
    assert "Required release test: tests/test_cli_error_messages_phase45.py" in check_names
