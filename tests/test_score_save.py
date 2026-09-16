import json

from hyperkit import SaveManager, ScoreManager


def test_score_high_score(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(save=save)

    score.add(5)

    assert score.score == 5
    assert score.value == 5
    assert score.high_score == 5

    score.reset_score()

    assert score.score == 0
    assert score.high_score == 5


def test_score_subtract_does_not_go_below_zero_by_default(
    tmp_path,
):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(
        save=save,
        initial_score=5,
    )

    score.subtract(10)

    assert score.value == 0


def test_score_subtract_can_allow_negative_score(
    tmp_path,
):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(
        save=save,
        initial_score=5,
    )

    score.subtract(
        10,
        minimum=None,
    )

    assert score.value == -5


def test_set_score_updates_high_score(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(save=save)

    score.set_score(20)

    assert score.value == 20
    assert score.high_score == 20


def test_reset_high_score(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(save=save)

    score.add(15)

    assert score.high_score == 15

    score.reset_high_score()

    assert score.high_score == 0


def test_is_new_high_score(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(save=save)

    score.add(10)

    assert score.high_score == 10

    score.set_score(9)

    assert not score.is_new_high_score()

    score.set_score(11)

    assert score.high_score == 11


def test_score_as_dict(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )
    score = ScoreManager(save=save)

    score.add(7)

    assert score.as_dict() == {
        "score": 7,
        "high_score": 7,
    }


def test_save_manager_persists_data(tmp_path):
    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )

    save.set(
        "coins",
        25,
    )

    reloaded = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )

    assert reloaded.get("coins") == 25


def test_save_manager_uses_android_private_storage(
    tmp_path,
    monkeypatch,
):
    android_private = (
        tmp_path
        / "android-private"
    )

    monkeypatch.setenv(
        "ANDROID_PRIVATE",
        str(android_private),
    )
    monkeypatch.setenv(
        "P4A_BOOTSTRAP",
        "SDL2",
    )

    save = SaveManager(
        app_name="test_game",
    )

    expected = (
        android_private
        / ".test_game"
        / "save.json"
    )

    assert save.path == expected
    assert save.path.parent.is_dir()

    save.set(
        "high_score",
        42,
    )

    assert save.path.is_file()

    content = json.loads(
        save.path.read_text(
            encoding="utf-8",
        )
    )

    assert content == {
        "high_score": 42,
    }


def test_explicit_save_root_overrides_android_storage(
    tmp_path,
    monkeypatch,
):
    android_private = (
        tmp_path
        / "android-private"
    )

    explicit_root = (
        tmp_path
        / "custom-save"
    )

    monkeypatch.setenv(
        "ANDROID_PRIVATE",
        str(android_private),
    )
    monkeypatch.setenv(
        "P4A_BOOTSTRAP",
        "SDL2",
    )

    save = SaveManager(
        app_name="test_game",
        root=explicit_root,
    )

    assert save.path == (
        explicit_root
        / "save.json"
    )


def test_android_storage_falls_back_to_android_argument(
    tmp_path,
    monkeypatch,
):
    monkeypatch.delenv(
        "ANDROID_PRIVATE",
        raising=False,
    )

    android_files = (
        tmp_path
        / "data"
        / "files"
    )

    android_app = (
        android_files
        / "app"
    )

    android_app.mkdir(
        parents=True,
    )

    monkeypatch.setenv(
        "ANDROID_ARGUMENT",
        str(android_app),
    )
    monkeypatch.setenv(
        "P4A_BOOTSTRAP",
        "SDL2",
    )

    save = SaveManager(
        app_name="test_game",
    )

    assert save.path == (
        android_files
        / ".test_game"
        / "save.json"
    )


def test_save_manager_recovers_from_invalid_json(
    tmp_path,
):
    save_file = (
        tmp_path
        / "save.json"
    )

    save_file.write_text(
        "{this-is-not-json",
        encoding="utf-8",
    )

    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )

    assert save.data == {}


def test_save_manager_rejects_non_dictionary_json_as_save_data(
    tmp_path,
):
    save_file = (
        tmp_path
        / "save.json"
    )

    save_file.write_text(
        '["unexpected", "list"]',
        encoding="utf-8",
    )

    save = SaveManager(
        app_name="test_game",
        root=tmp_path,
    )

    assert save.data == {}
