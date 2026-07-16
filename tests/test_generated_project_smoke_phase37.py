import ast
import os
from pathlib import Path

from hyperkit.cli import create_project


SMOKE_TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def generate_project(tmp_path: Path, template_name: str) -> Path:
    project_name = f"smoke_{template_name}"
    project_path = tmp_path / project_name

    current_dir = Path.cwd()

    try:
        os.chdir(tmp_path)
        create_project(project_name, template_name, project_path)
    finally:
        os.chdir(current_dir)

    assert project_path.exists(
    ), f"Generated project folder was not created: {project_path}"
    return project_path


def test_generated_projects_have_required_files(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)

        assert (project_path / "main.py").exists()
        assert (project_path / "README.md").exists()
        assert (project_path / "hyperkit.toml").exists()


def test_generated_projects_have_asset_folders(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)

        assert (project_path / "assets").exists()
        assert (project_path / "assets" / "images").exists()
        assert (project_path / "assets" / "audio").exists()
        assert (project_path / "assets" / "fonts").exists()
        assert (project_path / "assets" / "data").exists()


def test_generated_project_main_files_have_valid_python_syntax(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)
        main_file = project_path / "main.py"

        content = main_file.read_text(encoding="utf-8")
        ast.parse(content, filename=str(main_file))


def test_generated_project_main_files_import_hyperkit(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)
        content = (project_path / "main.py").read_text(encoding="utf-8")

        assert "from hyperkit import" in content
        assert "Game(" in content
        assert ".set_scene(" in content
        assert ".run()" in content


def test_generated_project_metadata_mentions_template(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)
        metadata = (project_path / "hyperkit.toml").read_text(encoding="utf-8")

        assert template_name in metadata


def test_generated_project_readmes_are_not_empty(tmp_path):
    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)
        readme = (project_path / "README.md").read_text(encoding="utf-8")

        assert len(readme.strip()) > 20
        assert "Template" in readme or "template" in readme


def test_generated_projects_do_not_contain_local_repo_paths(tmp_path):
    forbidden_terms = [
        "D:\\AI\\HyperKit\\gameviz-hyperkit",
        "/mnt/data",
        "gameviz-hyperkit\\src",
    ]

    for template_name in SMOKE_TEMPLATES:
        project_path = generate_project(tmp_path, template_name)

        for file_path in project_path.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in {".py", ".md", ".toml", ".txt", ".json"}:
                continue

            content = file_path.read_text(encoding="utf-8", errors="ignore")

            for forbidden in forbidden_terms:
                assert forbidden not in content
