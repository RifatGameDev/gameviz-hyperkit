from __future__ import annotations

from pathlib import Path
from typing import Any


class AudioError(Exception):
    """Base error for HyperKit audio."""


class AudioLoadError(AudioError):
    """Raised when an audio file cannot be loaded."""


class AudioManager:
    """Audio helper for HyperKit games.

    Uses Kivy SoundLoader internally when running a game while remaining
    testable with an injected loader.
    """

    def __init__(
        self,
        sound_volume: float = 1.0,
        music_volume: float = 0.7,
        sound_loader: Any | None = None,
    ) -> None:
        self.sound_volume = self._clamp_volume(
            sound_volume
        )
        self.music_volume = self._clamp_volume(
            music_volume
        )
        self.current_music = None
        self.active_sounds: list[Any] = []
        self.music_paused = False
        self._sound_loader = sound_loader

    @staticmethod
    def _clamp_volume(
        volume: float,
    ) -> float:
        return max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

    @property
    def sound_count(
        self,
    ) -> int:
        """Return the number of tracked sound effects."""

        return len(
            self.active_sounds
        )

    @property
    def has_music(
        self,
    ) -> bool:
        """Return whether background music is currently loaded."""

        return (
            self.current_music
            is not None
        )

    def _get_sound_loader(
        self,
    ):
        if self._sound_loader is not None:
            loader = self._sound_loader
        else:
            try:
                from kivy.core.audio import SoundLoader
            except ImportError as exc:  # pragma: no cover
                raise AudioError(
                    "Kivy is required for audio playback. "
                    "Install with: pip install kivy"
                ) from exc

            loader = SoundLoader

        if not hasattr(
            loader,
            "load",
        ):
            raise AudioError(
                "Audio loader must provide a load() method."
            )

        return loader

    def _load_audio(
        self,
        audio_path: str | Path,
    ):
        path = str(
            audio_path
        ).strip()

        if not path:
            raise AudioLoadError(
                "Audio path must not be empty."
            )

        loader = self._get_sound_loader()
        sound = loader.load(
            path
        )

        if sound is None:
            raise AudioLoadError(
                f"Could not load audio file: {path}"
            )

        return sound

    def play_sound(
        self,
        audio_path: str | Path,
        volume: float | None = None,
        loop: bool = False,
    ):
        """Play a short sound effect and track it."""

        self.cleanup_sounds()

        sound = self._load_audio(
            audio_path
        )
        sound.volume = (
            self.sound_volume
            if volume is None
            else self._clamp_volume(
                volume
            )
        )
        sound.loop = bool(
            loop
        )
        sound.play()

        self.active_sounds.append(
            sound
        )

        return sound

    def stop_sound(
        self,
        sound: Any,
    ) -> bool:
        """Stop one tracked sound effect."""

        if sound not in self.active_sounds:
            return False

        if hasattr(
            sound,
            "stop",
        ):
            sound.stop()

        self.active_sounds.remove(
            sound
        )

        return True

    def cleanup_sounds(
        self,
    ) -> int:
        """Forget sound effects that report a stopped state."""

        before = len(
            self.active_sounds
        )

        self.active_sounds = [
            sound
            for sound in self.active_sounds
            if getattr(
                sound,
                "state",
                None,
            ) != "stop"
        ]

        return (
            before
            - len(
                self.active_sounds
            )
        )

    def play_music(
        self,
        audio_path: str | Path,
        volume: float | None = None,
        loop: bool = True,
    ):
        """Play background music, replacing any previously loaded music."""

        self.stop_music()

        music = self._load_audio(
            audio_path
        )
        music.volume = (
            self.music_volume
            if volume is None
            else self._clamp_volume(
                volume
            )
        )
        music.loop = bool(
            loop
        )
        music.play()

        self.current_music = music
        self.music_paused = False

        return music

    def stop_music(
        self,
    ) -> bool:
        """Stop and clear current background music."""

        if self.current_music is None:
            self.music_paused = False
            return False

        if hasattr(
            self.current_music,
            "stop",
        ):
            self.current_music.stop()

        self.current_music = None
        self.music_paused = False

        return True

    def pause_music(
        self,
    ) -> bool:
        """Pause current music using the backend stop operation."""

        if self.current_music is None:
            return False

        if self.music_paused:
            return False

        if hasattr(
            self.current_music,
            "stop",
        ):
            self.current_music.stop()

        self.music_paused = True
        return True

    def resume_music(
        self,
    ) -> bool:
        """Resume previously paused background music."""

        if (
            self.current_music is None
            or not self.music_paused
        ):
            return False

        if hasattr(
            self.current_music,
            "play",
        ):
            self.current_music.play()

        self.music_paused = False
        return True

    def stop_all_sounds(
        self,
    ) -> int:
        """Stop all active sound effects and return the number stopped."""

        sounds = list(
            self.active_sounds
        )

        for sound in sounds:
            if hasattr(
                sound,
                "stop",
            ):
                sound.stop()

        self.active_sounds.clear()

        return len(
            sounds
        )

    def set_sound_volume(
        self,
        volume: float,
    ) -> "AudioManager":
        self.sound_volume = self._clamp_volume(
            volume
        )
        return self

    def set_music_volume(
        self,
        volume: float,
    ) -> "AudioManager":
        self.music_volume = self._clamp_volume(
            volume
        )

        if self.current_music is not None:
            self.current_music.volume = (
                self.music_volume
            )

        return self


_default_audio_manager = AudioManager()


def play_sound(
    audio_path: str | Path,
    volume: float | None = None,
    loop: bool = False,
):
    return _default_audio_manager.play_sound(
        audio_path,
        volume=volume,
        loop=loop,
    )


def play_music(
    audio_path: str | Path,
    volume: float | None = None,
    loop: bool = True,
):
    return _default_audio_manager.play_music(
        audio_path,
        volume=volume,
        loop=loop,
    )


def stop_music() -> None:
    _default_audio_manager.stop_music()
