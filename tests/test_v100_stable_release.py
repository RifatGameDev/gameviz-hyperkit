import json
from pathlib import Path

import hyperkit

from hyperkit.api_contract import (
    FROZEN_API_EXPORT_COUNT,
    FROZEN_API_FINGERPRINT,
)
from hyperkit.stable_release import (
    STABLE_PACKAGE_VERSION,
    generate_stable_release_report,
    write_stable_release_certificate,
)


def test_v100_stable_package_identity_and_api_contract():
    assert STABLE_PACKAGE_VERSION == "1.0.1"
    assert hyperkit.__version__ == "1.0.1"
    assert hyperkit.API_VERSION == "1.0"


def test_v100_frozen_api_is_unchanged_from_beta():
    assert FROZEN_API_EXPORT_COUNT == 256
    assert (
        FROZEN_API_FINGERPRINT
        == (
            "80bdc58a8590797b01faa0305ec3aac2"
            "2ed81ea17fc98b8d9a02ec211fa70d75"
        )
    )

    hyperkit.validate_frozen_public_api()


def test_v100_stable_release_report_passes():
    report = generate_stable_release_report(
        "."
    )

    assert report.passed
    assert report.package_version == "1.0.1"
    assert report.failed_count == 0


def test_v100_stable_release_report_contains_core_gates():
    report = generate_stable_release_report(
        "."
    )

    names = {
        check.name
        for check in report.checks
    }

    expected = {
        "Stable package version",
        "Package/module version synchronization",
        "Stable package classifier",
        "Frozen compatibility contract",
        "Frozen API exact match",
        "Frozen API export count",
        "Frozen API fingerprint",
        "Release readiness report",
        "Pre-release audit",
        "Stable PyPI target eligibility",
        "Stable README status",
        "Stable roadmap state",
        "Stable changelog entry",
        "Stable version history",
        "Stable release documentation",
        "Stable release workflow",
    }

    assert expected == names


def test_v100_stable_release_certificate(
    tmp_path: Path,
):
    report = generate_stable_release_report(
        "."
    )
    output = (
        tmp_path
        / "stable-release-certificate.json"
    )

    result = write_stable_release_certificate(
        report,
        output,
        source_commit="abc123",
    )

    assert result == output.resolve()

    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert data[
        "package"
    ] == "gameviz-hyperkit"
    assert data[
        "version"
    ] == "1.0.1"
    assert data[
        "api_version"
    ] == "1.0"
    assert data[
        "frozen_api_export_count"
    ] == 256
    assert data[
        "frozen_api_fingerprint"
    ] == FROZEN_API_FINGERPRINT
    assert data[
        "source_commit"
    ] == "abc123"
    assert data[
        "status"
    ] == "pass"
    assert all(
        data[
            "checks"
        ].values()
    )
