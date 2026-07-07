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

    def play(self):
        self.play_count += 1

    def stop(self):
        self.stop_count += 1


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
