from pathlib import Path

import pytest

from hyperkit import AudioLoadError, AudioManager


class FakeSound:
    def __init__(self, path: str):
        self.path = path
        self.volume = 1.0
        self.loop = False
        self.play_count = 0
        self.stop_count = 0
        self.state = "stop"

    def play(self):
        self.play_count += 1
        self.state = "play"

    def stop(self):
        self.stop_count += 1
        self.state = "stop"


class FakeSoundLoader:
    def __init__(self):
        self.loaded_paths = []

    def load(self, path: str):
        self.loaded_paths.append(path)

        if "missing" in path:
            return None

        return FakeSound(path)


def test_audio_manager_play_sound_loads_and_plays_audio(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    sound = audio.play_sound(tmp_path / "click.wav")

    assert sound.play_count == 1
    assert sound.volume == 1.0
    assert sound.loop is False
    assert len(audio.active_sounds) == 1


def test_audio_manager_play_sound_supports_custom_volume_and_loop(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    sound = audio.play_sound(tmp_path / "loop.wav", volume=0.4, loop=True)

    assert sound.volume == 0.4
    assert sound.loop is True


def test_audio_manager_play_music_stores_current_music(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    music = audio.play_music(tmp_path / "music.wav")

    assert audio.current_music is music
    assert music.play_count == 1
    assert music.loop is True
    assert music.volume == 0.7


def test_audio_manager_play_music_stops_previous_music(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    old_music = audio.play_music(tmp_path / "old_music.wav")
    new_music = audio.play_music(tmp_path / "new_music.wav")

    assert old_music.stop_count == 1
    assert audio.current_music is new_music


def test_audio_manager_stop_music_clears_current_music(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    music = audio.play_music(tmp_path / "music.wav")
    audio.stop_music()

    assert music.stop_count == 1
    assert audio.current_music is None


def test_audio_manager_stop_all_sounds(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    sound_1 = audio.play_sound(tmp_path / "sound_1.wav")
    sound_2 = audio.play_sound(tmp_path / "sound_2.wav")

    audio.stop_all_sounds()

    assert sound_1.stop_count == 1
    assert sound_2.stop_count == 1
    assert audio.active_sounds == []


def test_audio_manager_raises_clear_error_when_audio_cannot_load(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    with pytest.raises(AudioLoadError):
        audio.play_sound(tmp_path / "missing.wav")


def test_audio_manager_clamps_volume(tmp_path: Path):
    loader = FakeSoundLoader()
    audio = AudioManager(sound_loader=loader)

    sound = audio.play_sound(tmp_path / "click.wav", volume=5.0)

    assert sound.volume == 1.0

    sound = audio.play_sound(tmp_path / "quiet.wav", volume=-2.0)

    assert sound.volume == 0.0



def test_audio_manager_tracks_sound_count_and_stop_sound(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    sound = audio.play_sound(
        tmp_path / "click.wav"
    )

    assert audio.sound_count == 1
    assert audio.stop_sound(sound) is True
    assert sound.stop_count == 1
    assert audio.sound_count == 0
    assert audio.stop_sound(sound) is False


def test_audio_manager_cleans_finished_sounds(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    first = audio.play_sound(
        tmp_path / "first.wav"
    )
    audio.play_sound(
        tmp_path / "second.wav"
    )

    first.stop()

    assert audio.cleanup_sounds() == 1
    assert audio.sound_count == 1


def test_audio_manager_music_pause_resume_state(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    music = audio.play_music(
        tmp_path / "music.wav"
    )

    assert audio.has_music
    assert not audio.music_paused

    assert audio.pause_music() is True
    assert audio.music_paused
    assert music.stop_count == 1
    assert audio.pause_music() is False

    assert audio.resume_music() is True
    assert not audio.music_paused
    assert music.play_count == 2
    assert audio.resume_music() is False


def test_audio_manager_stop_music_reports_result(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    assert audio.stop_music() is False

    audio.play_music(
        tmp_path / "music.wav"
    )

    assert audio.stop_music() is True
    assert not audio.has_music
    assert not audio.music_paused


def test_audio_manager_stop_all_sounds_reports_count(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    audio.play_sound(
        tmp_path / "one.wav"
    )
    audio.play_sound(
        tmp_path / "two.wav"
    )

    assert audio.stop_all_sounds() == 2
    assert audio.sound_count == 0


def test_audio_manager_volume_setters_are_chainable(
    tmp_path: Path,
):
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    music = audio.play_music(
        tmp_path / "music.wav"
    )

    assert audio.set_sound_volume(0.25) is audio
    assert audio.sound_volume == 0.25

    assert audio.set_music_volume(0.4) is audio
    assert audio.music_volume == 0.4
    assert music.volume == 0.4


def test_audio_manager_rejects_empty_audio_path():
    loader = FakeSoundLoader()
    audio = AudioManager(
        sound_loader=loader
    )

    with pytest.raises(
        AudioLoadError,
        match="must not be empty",
    ):
        audio.play_sound("   ")


def test_audio_manager_rejects_invalid_loader():
    audio = AudioManager(
        sound_loader=object()
    )

    with pytest.raises(
        Exception,
        match="load",
    ):
        audio.play_sound(
            "sound.wav"
        )
