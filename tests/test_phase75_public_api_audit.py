import hyperkit


def test_public_all_has_no_duplicates():
    assert len(
        hyperkit.__all__
    ) == len(
        set(
            hyperkit.__all__
        )
    )


def test_every_public_export_exists():
    missing = [
        name
        for name in hyperkit.__all__
        if not hasattr(
            hyperkit,
            name,
        )
    ]

    assert missing == []


def test_compatibility_contract_is_subset_of_public_exports():
    assert hyperkit.REQUIRED_PUBLIC_API.issubset(
        set(
            hyperkit.__all__
        )
    )


def test_phase75_hardened_systems_are_public():
    expected = {
        "AnimationManager",
        "AssetManager",
        "AudioManager",
        "Bounds",
        "Button",
        "CameraFollow",
        "CanvasScaler",
        "CollisionManifold",
        "Cooldown",
        "GameObject",
        "GameSystems",
        "InputActionMap",
        "LevelManager",
        "ParticleEmitter",
        "PhysicsBody",
        "PhysicsMaterial",
        "PhysicsWorld",
        "ProgressBar",
        "SaveManager",
        "SceneTransition",
        "SpriteAnimator",
        "StateMachine",
        "TimerManager",
        "Vector2",
    }

    assert expected.issubset(
        set(
            hyperkit.__all__
        )
    )


def test_package_version_and_api_contract_remain_separate():
    assert (
        hyperkit.__version__
        == "1.0.1"
    )
    assert (
        hyperkit.API_VERSION
        == "1.0"
    )
