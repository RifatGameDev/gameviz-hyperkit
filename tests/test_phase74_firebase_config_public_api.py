import hyperkit


def test_firebase_json_loader_is_public():
    assert hasattr(
        hyperkit,
        "load_firebase_analytics_config",
    )

    assert (
        "load_firebase_analytics_config"
        in hyperkit.__all__
    )
