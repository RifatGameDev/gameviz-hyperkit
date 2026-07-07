from __future__ import annotations

from pathlib import Path
from typing import Any


class AudioError(Exception):
    """Base error for HyperKit audio."""


class AudioLoadError(AudioError):
    """Raised when an audio file cannot be loaded."""


class AudioManager:
    """Simple audio helper for HyperKit games.

    Uses Kivy SoundLoader internally when running a game.
    """

    def __init__(
        self,
        sound_volume: float = 1.0,
        music_volume: float = 0.7,
        sound_loader: Any | None = None,
    ) -> None:
        self.sound_volume = self._clamp_volume(sound_volume)
        self.music_volume = self._clamp_volume(music_volume)
        self.current_music = None
        self.active_sounds: list[Any] = []
        self._sound_loader = sound_loader

    def _clamp_volume(self, volume: float) -> float:
        return max(0.0, min(1.0, float(volume)))

    def _get_sound_loader(self):
        if self._sound_loader is not None:
            return self._sound_loader

        try:
            from kivy.core.audio import SoundLoader
        except ImportError as exc:  # pragma: no cover
            raise AudioError(
                "Kivy is required for audio playback. Install with: pip install kivy"
            ) from exc

        return SoundLoader

    def _load_audio(self, audio_path: str | Path):
        path = str(audio_path)
        loader = self._get_sound_loader()
        sound = loader.load(path)

        if sound is None:
            raise AudioLoadError(f"Could not load audio file: {path}")

        return sound

    def play_sound(
        self,
        audio_path: str | Path,
        volume: float | None = None,
        loop: bool = False,
    ):
        """Play a short sound effect."""
        sound = self._load_audio(audio_path)
        sound.volume = self.sound_volume if volume is None else self._clamp_volume(
            volume)
        sound.loop = loop
        sound.play()

        self.active_sounds.append(sound)
        return sound

    def play_music(
        self,
        audio_path: str | Path,
        volume: float | None = None,
        loop: bool = True,
    ):
        """Play background music. Stops old music before playing new music."""
        self.stop_music()

        music = self._load_audio(audio_path)
        music.volume = self.music_volume if volume is None else self._clamp_volume(
            volume)
        music.loop = loop
        music.play()

        self.current_music = music
        return music

    def stop_music(self) -> None:
        """Stop current background music."""
        if self.current_music is not None:
            self.current_music.stop()
            self.current_music = None

    def pause_music(self) -> None:
        """Pause current background music if supported."""
        if self.current_music is not None and hasattr(self.current_music, "stop"):
            self.current_music.stop()

    def resume_music(self) -> None:
        """Resume current background music if available."""
        if self.current_music is not None:
            self.current_music.play()

    def stop_all_sounds(self) -> None:
        """Stop all active sound effects."""
        for sound in self.active_sounds:
            if hasattr(sound, "stop"):
                sound.stop()

        self.active_sounds.clear()

    def set_sound_volume(self, volume: float) -> None:
        self.sound_volume = self._clamp_volume(volume)

    def set_music_volume(self, volume: float) -> None:
        self.music_volume = self._clamp_volume(volume)

        if self.current_music is not None:
            self.current_music.volume = self.music_volume


_default_audio_manager = AudioManager()


def play_sound(audio_path: str | Path, volume: float | None = None, loop: bool = False):
    return _default_audio_manager.play_sound(audio_path, volume=volume, loop=loop)


def play_music(audio_path: str | Path, volume: float | None = None, loop: bool = True):
    return _default_audio_manager.play_music(audio_path, volume=volume, loop=loop)


def stop_music() -> None:
    _default_audio_manager.stop_music()
