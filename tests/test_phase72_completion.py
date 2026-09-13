import pytest

import hyperkit
from hyperkit import (
    HyperKitCompatibilityError,
    HyperKitRuntimeError,
    PlatformKind,
    REQUIRED_PUBLIC_API,
    RuntimeEnvironment,
    SDKContext,
    get_missing_public_api,
    run_game,
    start_runtime,
    stop_runtime,
    validate_public_api,
)


class DummyGame:
    def __init__(self):
        self.ran = False

    def run(self):
        self.ran = True
        return "finished"


class FailingGame:
    def run(self):
        raise RuntimeError(
            "game failed"
        )


def test_start_runtime_initializes_context():
    context = SDKContext()

    result = start_runtime(context)

    assert result is context
    assert context.is_running is True

    environment = context.get_metadata(
        "environment"
    )

    assert isinstance(
        environment,
        dict,
    )

    assert "platform" in environment
    assert "python_version" in environment


def test_stop_runtime_stops_context():
    context = SDKContext()

    start_runtime(context)
    result = stop_runtime(context)

    assert result is context
    assert context.is_stopped is True


def test_run_game_manages_runtime_lifecycle():
    game = DummyGame()
    context = SDKContext()

    result = run_game(
        game,
        context=context,
    )

    assert result == "finished"
    assert game.ran is True
    assert context.is_stopped is True


def test_run_game_stops_runtime_on_failure():
    context = SDKContext()

    with pytest.raises(
        RuntimeError
    ):
        run_game(
            FailingGame(),
            context=context,
        )

    assert context.is_stopped is True


def test_run_game_rejects_invalid_game():
    with pytest.raises(
        HyperKitRuntimeError
    ):
        run_game(object())


def test_environment_types_are_public():
    assert PlatformKind.WINDOWS.value == "windows"

    environment = RuntimeEnvironment(
        platform=PlatformKind.WINDOWS,
        python_version="3.11",
        python_implementation="CPython",
        executable="python",
    )

    assert environment.is_desktop is True


def test_required_public_api_is_not_empty():
    assert REQUIRED_PUBLIC_API

    assert "SDKContext" in REQUIRED_PUBLIC_API
    assert "run_game" in REQUIRED_PUBLIC_API
    assert "load_project_config" in REQUIRED_PUBLIC_API


def test_current_hyperkit_public_api_contract_passes():
    validate_public_api()


def test_public_api_contract_detects_missing_names():
    missing = get_missing_public_api(
        {}
    )

    assert "SDKContext" in missing
    assert "run_game" in missing


def test_public_api_validation_rejects_incomplete_namespace():
    with pytest.raises(
        HyperKitCompatibilityError
    ):
        validate_public_api(
            {
                "Game": object(),
            }
        )


def test_required_api_names_are_exported():
    exported = set(
        hyperkit.__all__
    )

    assert REQUIRED_PUBLIC_API <= exported
