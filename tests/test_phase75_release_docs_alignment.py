from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


PYPROJECT = Path("pyproject.toml")
RELEASE_CHECKLIST = Path(
    "docs/RELEASE_READINESS_CHECKLIST.md"
)
RELEASE_BUILD_DOC = Path(
    "docs/RELEASE_BUILD_AUTOMATION.md"
)


def test_package_description_matches_complete_game_scope():
    with PYPROJECT.open("rb") as file:
        project = tomllib.load(file)["project"]

    description = project["description"]

    assert "complete small 2D" in description
    assert "prototypes" not in description.lower()


def test_release_checklist_has_no_machine_specific_workspace():
    content = RELEASE_CHECKLIST.read_text(
        encoding="utf-8"
    )

    assert "D:\\AI\\HyperKit" not in content
    assert "<workspace-outside-the-repository>" in content


def test_release_docs_allow_real_pypi_after_release_gates():
    checklist = RELEASE_CHECKLIST.read_text(
        encoding="utf-8"
    )
    build_doc = RELEASE_BUILD_DOC.read_text(
        encoding="utf-8"
    )

    stale = (
        "Do not publish to real PyPI "
        "until the package is more stable."
    )

    assert stale not in checklist
    assert stale not in build_doc
    assert "real PyPI" in checklist
    assert "real PyPI" in build_doc


def test_release_docs_require_clean_install_validation():
    checklist = RELEASE_CHECKLIST.read_text(
        encoding="utf-8"
    )
    build_doc = RELEASE_BUILD_DOC.read_text(
        encoding="utf-8"
    )

    assert "clean-install verification" in checklist
    assert "clean-install verification" in build_doc
