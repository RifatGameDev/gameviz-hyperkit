from pathlib import Path


READINESS = Path(
    "docs/release-evidence/TESTPYPI_RC_READINESS_PHASE66.md"
)
INSTALL_RESULT = Path(
    "docs/release-evidence/TESTPYPI_INSTALL_RESULT_PHASE66.md"
)
ARTIFACT_OUTPUT = Path(
    "docs/release-evidence/phase66-artifact-validation.txt"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase66_evidence_files_exist():
    for path in [
        READINESS,
        INSTALL_RESULT,
        ARTIFACT_OUTPUT,
    ]:
        assert path.exists(), f"Missing Phase 66 evidence: {path}"


def test_rc_readiness_document_is_completed():
    content = read(READINESS)

    assert "gameviz-hyperkit" in content
    assert "0.1.1rc1" in content
    assert "Current status: TESTPYPI RC VALIDATED" in content
    assert "Approved for TestPyPI upload: Yes" in content
    assert "Approved for real PyPI publication: No" in content
    assert "- [ ]" not in content


def test_testpypi_install_result_passed():
    content = read(INSTALL_RESULT)

    assert "Package installed from TestPyPI: PASS" in content
    assert (
        "Installed version confirmed as 0.1.1rc1: PASS"
        in content
    )
    assert "HyperKit import: PASS" in content
    assert "All generated main.py files compiled: PASS" in content
    assert "Phase 66 result: PASS" in content


def test_artifact_validation_passed():
    content = read(ARTIFACT_OUTPUT)

    assert "0.1.1rc1" in content
    assert "PASSED" in content
    assert (
        "gameviz_hyperkit-0.1.1rc1-py3-none-any.whl"
        in content
    )
    assert "gameviz_hyperkit-0.1.1rc1.tar.gz" in content


def test_phase66_evidence_has_no_local_paths():
    files = [
        READINESS,
        INSTALL_RESULT,
        ARTIFACT_OUTPUT,
    ]

    forbidden = [
        "D:" + "\\AI\\HyperKit\\gameviz-hyperkit",
        "gameviz-hyperkit" + "\\src",
        "/" + "mnt/data",
        "pypi-" + "AgEI",
    ]

    for path in files:
        content = read(path)

        for term in forbidden:
            assert term not in content
