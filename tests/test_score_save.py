from hyperkit import SaveManager, ScoreManager


def test_score_high_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)
    score.add(5)
    assert score.score == 5
    assert score.high_score == 5

    score.reset_score()
    assert score.score == 0
    assert score.high_score == 5
