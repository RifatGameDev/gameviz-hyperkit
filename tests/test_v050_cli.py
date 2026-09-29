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
