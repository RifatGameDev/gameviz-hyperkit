from hyperkit import (
    COMPLETE_GAME_TEMPLATES,
    format_complete_game_report,
    generate_complete_game_report,
)


EXPECTED_TEMPLATES = {
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
}


def test_complete_game_template_inventory():
    assert set(
        COMPLETE_GAME_TEMPLATES
    ) == EXPECTED_TEMPLATES


def test_all_builtin_games_pass_completion_validation():
    report = generate_complete_game_report(
        "."
    )

    assert report.total == 54
    assert report.failed_count == 0
    assert report.passed


def test_every_complete_game_has_restart_and_game_over():
    report = generate_complete_game_report(
        "."
    )

    relevant = [
        check
        for check in report.checks
        if check.name in {
            "game-over state exists",
            "restart flow exists",
        }
    ]

    assert len(relevant) == 12
    assert all(
        check.passed
        for check in relevant
    )


def test_complete_game_report_format():
    report = generate_complete_game_report(
        "."
    )
    output = format_complete_game_report(
        report
    )

    assert "HyperKit Complete Game Validation" in output
    assert "Passed: 54/54" in output
    assert "Failed: 0" in output
    assert "Complete game validation status: PASS" in output



def test_complete_game_validation_falls_back_to_installed_templates(
    tmp_path,
):
    report = generate_complete_game_report(
        tmp_path
    )

    assert report.total == 54
    assert report.passed
