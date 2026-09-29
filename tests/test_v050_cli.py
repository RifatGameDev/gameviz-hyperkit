from hyperkit.cli import (
    create_project,
    main,
)


def test_diagnostics_command_accepts_generated_project(
    tmp_path,
    capsys,
):
    project = (
        tmp_path
        / "diagnostics_game"
    )

    create_project(
        "diagnostics_game",
        "tap-counter",
        project,
    )

    result = main(
        [
            "diagnostics",
            "--path",
            str(project),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "HyperKit Project Diagnostics" in output
    assert "Project status: valid" in output
    assert "Template: tap-counter" in output


def test_validate_complete_games_cli(
    capsys,
):
    result = main(
        [
            "validate-complete-games",
            "--path",
            ".",
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "Passed: 54/54" in output
    assert "Complete game validation status: PASS" in output



def test_validate_project_rejects_invalid_main_syntax(
    tmp_path,
):
    from hyperkit.cli import validate_project

    project = (
        tmp_path
        / "broken_game"
    )
    create_project(
        "broken_game",
        "tap-counter",
        project,
    )

    (
        project
        / "main.py"
    ).write_text(
        "def broken(:\n    pass\n",
        encoding="utf-8",
    )

    valid, issues = validate_project(
        project
    )

    assert not valid
    assert any(
        issue.startswith(
            "Invalid main.py syntax:"
        )
        for issue in issues
    )


def test_doctor_reports_generated_project_status(
    tmp_path,
    capsys,
):
    project = (
        tmp_path
        / "doctor_game"
    )
    create_project(
        "doctor_game",
        "tap-counter",
        project,
    )

    result = main(
        [
            "doctor",
            "--path",
            str(project),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "Project: valid" in output
    assert "Project path:" in output
