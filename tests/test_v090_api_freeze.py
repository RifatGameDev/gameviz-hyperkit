import pytest

import hyperkit
from hyperkit import (
    HyperKitCompatibilityError,
)
from hyperkit.api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
    FROZEN_API_VERSION,
    FROZEN_PUBLIC_API,
    get_api_fingerprint,
    validate_frozen_public_api,
)


def test_v090_frozen_api_version_is_10():
    assert FROZEN_API_VERSION == "1.0"
    assert hyperkit.API_VERSION == "1.0"
    assert hyperkit.get_api_version() == "1.0"


def test_v090_frozen_export_set_matches_public_all_exactly():
    assert len(
        hyperkit.__all__
    ) == len(
        set(
            hyperkit.__all__
        )
    )

    assert set(
        hyperkit.__all__
    ) == set(
        FROZEN_PUBLIC_API
    )


def test_v090_frozen_api_export_count_is_pinned():
    assert (
        len(
            FROZEN_PUBLIC_API
        )
        == FROZEN_API_EXPORT_COUNT
        == 256
    )


def test_v090_frozen_api_fingerprint_is_pinned():
    assert (
        get_api_fingerprint()
        == FROZEN_API_FINGERPRINT
        == (
            "80bdc58a8590797b01faa0305ec3aac2"
            "2ed81ea17fc98b8d9a02ec211fa70d75"
        )
    )


def test_v090_exact_freeze_validation_passes():
    validate_frozen_public_api()


def test_v090_freeze_rejects_missing_export():
    exports = list(
        hyperkit.__all__
    )
    exports.remove(
        "Game"
    )

    with pytest.raises(
        HyperKitCompatibilityError,
        match="missing=Game",
    ):
        validate_frozen_public_api(
            exports
        )


def test_v090_freeze_rejects_unexpected_export():
    exports = list(
        hyperkit.__all__
    )
    exports.append(
        "FutureUnreviewedAPI"
    )

    with pytest.raises(
        HyperKitCompatibilityError,
        match="unexpected=FutureUnreviewedAPI",
    ):
        validate_frozen_public_api(
            exports
        )


def test_v090_freeze_rejects_duplicate_export():
    exports = list(
        hyperkit.__all__
    )
    exports.append(
        "Game"
    )

    with pytest.raises(
        HyperKitCompatibilityError,
        match="duplicates=Game",
    ):
        validate_frozen_public_api(
            exports
        )


def test_v090_api_compatibility_rules():
    assert hyperkit.is_api_compatible(
        "1.0"
    )
    assert not hyperkit.is_api_compatible(
        "1.1"
    )
    assert not hyperkit.is_api_compatible(
        "0.9"
    )
    assert not hyperkit.is_api_compatible(
        "2.0"
    )

    hyperkit.require_api_version(
        "1.0"
    )

    with pytest.raises(
        HyperKitCompatibilityError
    ):
        hyperkit.require_api_version(
            "0.9"
        )
