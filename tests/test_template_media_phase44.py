from pathlib import Path


MEDIA_GUIDE = Path("docs/TEMPLATE_MEDIA_GUIDE.md")
SCREENSHOTS_DOC = Path("docs/TEMPLATE_SCREENSHOTS.md")
README_PATH = Path("README.md")

TEMPLATES = [
    "tap_counter",
    "flappy_mini",
    "swipe_runner",
    "puzzle_game",
    "quiz_game",
    "simple_physics",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_template_media_docs_exist():
    assert MEDIA_GUIDE.exists()
    assert SCREENSHOTS_DOC.exists()


def test_template_media_folders_exist():
    for template in TEMPLATES:
        folder = Path("docs/media/templates") / template

        assert folder.exists()
        assert (folder / "README.md").exists()


def test_template_media_guide_mentions_all_templates():
    content = read(MEDIA_GUIDE)

    for template in TEMPLATES:
        assert f"docs/media/templates/{template}/" in content


def test_template_screenshots_doc_mentions_expected_media_files():
    content = read(SCREENSHOTS_DOC)

    for template in TEMPLATES:
        assert f"docs/media/templates/{template}/screenshot.png" in content
        assert f"docs/media/templates/{template}/demo.gif" in content
        assert f"docs/media/templates/{template}/thumbnail.png" in content


def test_template_media_folder_readmes_are_not_empty():
    for template in TEMPLATES:
        readme = Path("docs/media/templates") / template / "README.md"
        content = read(readme)

        assert len(content.strip()) > 20
        assert "screenshot.png" in content
        assert "demo.gif" in content
        assert "thumbnail.png" in content


def test_main_readme_links_template_media_docs():
    content = read(README_PATH)

    assert "Template Media Guide" in content
    assert "docs/TEMPLATE_MEDIA_GUIDE.md" in content
    assert "Template Screenshots and Demo Media" in content
    assert "docs/TEMPLATE_SCREENSHOTS.md" in content


def test_health_checks_include_template_media_docs():
    from hyperkit import generate_health_report

    report = generate_health_report(".")
    paths = {check.path for check in report.checks}

    assert "docs/TEMPLATE_MEDIA_GUIDE.md" in paths
    assert "docs/TEMPLATE_SCREENSHOTS.md" in paths
    assert "tests/test_template_media_phase44.py" in paths


def test_release_checks_include_template_media_docs():
    from hyperkit import generate_release_report

    report = generate_release_report(".")
    check_names = {check.name for check in report.checks}

    assert "Required release file: docs/TEMPLATE_MEDIA_GUIDE.md" in check_names
    assert "Required release file: docs/TEMPLATE_SCREENSHOTS.md" in check_names
    assert "Required release test: tests/test_template_media_phase44.py" in check_names


def test_template_media_markdown_fences_are_balanced():
    assert read(MEDIA_GUIDE).count("```") % 2 == 0
    assert read(SCREENSHOTS_DOC).count("```") % 2 == 0
