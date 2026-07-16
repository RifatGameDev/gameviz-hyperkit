import re
import tomllib
from pathlib import Path


ROOT = Path(".")
PYPROJECT = ROOT / "pyproject.toml"


def load_pyproject():
    assert PYPROJECT.exists(), "pyproject.toml is missing"

    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)


def test_release_readiness_doc_exists():
    path = Path("docs/RELEASE_READINESS_CHECKLIST.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Release Readiness Checklist" in content
    assert "python -m build" in content
    assert "twine check dist/*" in content
    assert "gameviz-hyperkit" in content
    assert "hyperkit" in content
    assert "TestPyPI" in content


def test_pyproject_has_project_metadata():
    data = load_pyproject()

    assert "project" in data, "pyproject.toml must include [project] metadata"

    project = data["project"]

    assert project.get("name") == "gameviz-hyperkit"
    assert project.get("version")
    assert project.get("description")
    assert project.get("readme")
    assert project.get("requires-python")
    assert project.get("authors")


def test_pyproject_version_looks_valid():
    project = load_pyproject()["project"]
    version = project["version"]

    assert re.match(r"^\d+\.\d+\.\d+", version), (
        "Package version should look like 0.1.0"
    )


def test_pyproject_readme_file_exists():
    project = load_pyproject()["project"]
    readme = project.get("readme", "README.md")

    if isinstance(readme, dict):
        readme_path = readme.get("file", "README.md")
    else:
        readme_path = readme

    assert Path(readme_path).exists(), f"README file is missing: {readme_path}"


def test_package_import_folder_exists():
    package_path = Path("src/hyperkit")

    assert package_path.exists()
    assert (package_path / "__init__.py").exists()


def test_cli_entry_point_exists():
    project = load_pyproject()["project"]

    scripts = project.get("scripts", {})

    assert "hyperkit" in scripts
    assert scripts["hyperkit"] == "hyperkit.cli:main"


def test_required_documentation_files_exist():
    required_files = [
        "README.md",
        "docs/TEMPLATES.md",
        "docs/TEMPLATE_HELPERS.md",
        "docs/TEMPLATE_QUALITY_CHECKLIST.md",
        "docs/RELEASE_READINESS_CHECKLIST.md",
    ]

    for filename in required_files:
        assert Path(filename).exists(), f"Missing documentation file: {filename}"


def test_main_readme_mentions_package_identity():
    content = Path("README.md").read_text(encoding="utf-8").lower()

    assert "hyperkit" in content
    assert "gameviz" in content or "gameviz-hyperkit" in content


def test_main_readme_links_release_checklist():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "Release Readiness Checklist" in content
    assert "docs/RELEASE_READINESS_CHECKLIST.md" in content
