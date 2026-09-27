import hyperkit


def test_phase74_service_public_api_exports():
    expected = {
        "AdsService",
        "AnalyticsService",
    }

    assert expected.issubset(
        set(hyperkit.__all__)
    )

    for name in expected:
        assert hasattr(
            hyperkit,
            name,
        )


def test_phase74_services_are_available_from_subpackages():
    from hyperkit.ads import AdsService
    from hyperkit.analytics import AnalyticsService

    assert AdsService is hyperkit.AdsService
    assert (
        AnalyticsService
        is hyperkit.AnalyticsService
    )
