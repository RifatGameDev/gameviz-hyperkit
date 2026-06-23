from hyperkit import SaveManager, ScoreManager


def test_score_high_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)

    score.add(5)

    assert score.score == 5
    assert score.value == 5
    assert score.high_score == 5

    score.reset_score()

    assert score.score == 0
    assert score.high_score == 5


def test_score_subtract_does_not_go_below_zero_by_default(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save, initial_score=5)

    score.subtract(10)

    assert score.value == 0


def test_score_subtract_can_allow_negative_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save, initial_score=5)

    score.subtract(10, minimum=None)

    assert score.value == -5


def test_set_score_updates_high_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)

    score.set_score(20)

    assert score.value == 20
    assert score.high_score == 20


def test_reset_high_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)

    score.add(15)
    assert score.high_score == 15

    score.reset_high_score()
    assert score.high_score == 0


def test_is_new_high_score(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)

    score.add(10)
    assert score.high_score == 10

    score.set_score(9)
    assert not score.is_new_high_score()

    score.set_score(11)
    assert score.high_score == 11


def test_score_as_dict(tmp_path):
    save = SaveManager(app_name="test_game", root=tmp_path)
    score = ScoreManager(save=save)

    score.add(7)

    assert score.as_dict() == {
        "score": 7,
        "high_score": 7,
    }
