from hyperkit import (
    AudioManager,
    create_context,
)
from hyperkit.lifecycle import (
    background_runtime,
    pause_runtime,
    resume_runtime,
    start_runtime,
    stop_runtime,
)


class LifecycleService:
    def __init__(self):
        self.events = []

    def on_runtime_start(self):
        self.events.append(
            "start"
        )

    def on_runtime_pause(self):
        self.events.append(
            "pause"
        )

    def on_runtime_background(self):
        self.events.append(
            "background"
        )

    def on_runtime_resume(self):
        self.events.append(
            "resume"
        )

    def on_runtime_stop(self):
        self.events.append(
            "stop"
        )


class DummySound:
    def __init__(self):
        self.state = "play"
        self.volume = 1.0
        self.loop = False
        self.play_calls = 0
        self.stop_calls = 0

    def play(self):
        self.state = "play"
        self.play_calls += 1

    def stop(self):
        self.state = "stop"
        self.stop_calls += 1


class DummyLoader:
    def __init__(self):
        self.created = []

    def load(self, path):
        sound = DummySound()
        self.created.append(
            sound
        )
        return sound


def test_runtime_lifecycle_notifies_all_registered_services():
    context = create_context()
    service = LifecycleService()

    context.register_service(
        "custom",
        service,
    )
    context.register_service(
        "same-custom",
        service,
    )

    start_runtime(
        context
    )
    pause_runtime(
        context
    )
    background_runtime(
        context
    )
    resume_runtime(
        context
    )
    stop_runtime(
        context
    )

    assert service.events == [
        "start",
        "pause",
        "background",
        "resume",
        "stop",
    ]


def test_audio_manager_follows_runtime_lifecycle():
    loader = DummyLoader()
    audio = AudioManager(
        sound_loader=loader
    )
    context = create_context()
    context.register_service(
        "audio",
        audio,
    )

    start_runtime(
        context
    )
    music = audio.play_music(
        "music.ogg"
    )
    effect = audio.play_sound(
        "tap.wav"
    )

    pause_runtime(
        context
    )

    assert audio.music_paused
    assert music.stop_calls == 1

    resume_runtime(
        context
    )

    assert not audio.music_paused
    assert music.play_calls == 2

    stop_runtime(
        context
    )

    assert audio.current_music is None
    assert audio.sound_count == 0
    assert effect.stop_calls == 1



class SelfRemovingService:
    def __init__(
        self,
        context,
        name,
    ):
        self.context = context
        self.name = name
        self.calls = 0

    def on_runtime_pause(
        self,
    ):
        self.calls += 1
        self.context.unregister_service(
            self.name
        )


def test_runtime_service_dispatch_allows_registry_mutation():
    context = create_context()
    removing = SelfRemovingService(
        context,
        "removing",
    )
    other = LifecycleService()

    context.register_service(
        "removing",
        removing,
    )
    context.register_service(
        "other",
        other,
    )

    start_runtime(
        context
    )
    pause_runtime(
        context
    )

    assert removing.calls == 1
    assert "pause" in other.events
    assert not context.has_service(
        "removing"
    )
