from pathlib import Path

docs_dir = Path("docs")
docs_dir.mkdir(exist_ok=True)

quality_doc = """# Template Quality Checklist

This checklist is used to keep HyperKit templates clean, beginner-friendly, and reliable.

---

## Required Files

Each template should include:

- `main.py`
- `README.md`

---

## Required Template Code Standards

Each template `main.py` should:

- be valid Python syntax
- import from `hyperkit`
- define at least one `Scene` class
- include a `start()` method
- call `self.start_game()`
- include a runnable entry point
- create a `Game(...)`
- call `.set_scene(...)`
- call `.run()`

---

## Required README Sections

Each template README should include:

- template title
- `## Features`
- `## Run`
- `## Gameplay`
- `## Helper Systems Used`

---

## Helper-Based Template Expectations

The upgraded templates should demonstrate the following helper systems where useful:

| Template | Expected Helpers |
|---|---|
| `tap_counter` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `flappy_mini` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `swipe_runner` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `InputActionMap`, `ScoreManager` |
| `puzzle_game` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `ScoreManager` |
| `quiz_game` | `ProgressBar`, `ParticleEmitter`, `CameraShake`, `InputActionMap`, `ScoreManager` |
| `simple_physics` | `AssetManager`, `ProgressBar`, `ParticleEmitter`, `CameraShake`, `BoundsManager`, `InputActionMap`, `Cooldown` |

---

## Template Goals

A good HyperKit template should be:

- easy to run
- easy to understand
- mobile-friendly
- small enough for beginners
- useful as a starting point for real game prototypes
- visually clear
- structured around reusable HyperKit helpers
"""

quality_test = '''import ast
from pathlib import Path


UPGRADED_TEMPLATES = {
    "tap_counter": [
        "AssetManager",
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "BoundsManager",
        "InputActionMap",
        "ScoreManager",
    ],
    "flappy_mini": [
        "AssetManager",
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "BoundsManager",
        "InputActionMap",
        "ScoreManager",
    ],
    "swipe_runner": [
        "AssetManager",
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "InputActionMap",
        "ScoreManager",
    ],
    "puzzle_game": [
        "AssetManager",
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "BoundsManager",
        "InputActionMap",
        "ScoreManager",
    ],
    "quiz_game": [
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "InputActionMap",
        "ScoreManager",
    ],
    "simple_physics": [
        "AssetManager",
        "ProgressBar",
        "ParticleEmitter",
        "CameraShake",
        "BoundsManager",
        "InputActionMap",
        "Cooldown",
    ],
}


def template_main_path(template_name: str) -> Path:
    return Path("src/hyperkit/templates") / template_name / "main.py"


def template_readme_path(template_name: str) -> Path:
    return Path("src/hyperkit/templates") / template_name / "README.md"


def read_main(template_name: str) -> str:
    return template_main_path(template_name).read_text(encoding="utf-8")


def read_readme(template_name: str) -> str:
    return template_readme_path(template_name).read_text(encoding="utf-8")


def test_all_upgraded_templates_have_required_files():
    for template_name in UPGRADED_TEMPLATES:
        assert template_main_path(template_name).exists(), f"{template_name} missing main.py"
        assert template_readme_path(template_name).exists(), f"{template_name} missing README.md"


def test_all_upgraded_templates_have_valid_python_syntax():
    for template_name in UPGRADED_TEMPLATES:
        content = read_main(template_name)
        ast.parse(content, filename=str(template_main_path(template_name)))


def test_all_upgraded_templates_are_runnable_apps():
    for template_name in UPGRADED_TEMPLATES:
        content = read_main(template_name)

        assert "from hyperkit import" in content
        assert "Scene" in content
        assert "def start(self)" in content
        assert "self.start_game()" in content
        assert 'if __name__ == "__main__"' in content
        assert "Game(" in content
        assert ".set_scene(" in content
        assert ".run()" in content


def test_all_upgraded_templates_include_expected_helpers_in_code():
    for template_name, helpers in UPGRADED_TEMPLATES.items():
        content = read_main(template_name)

        for helper in helpers:
            assert helper in content, f"{template_name} missing {helper} in main.py"


def test_all_upgraded_template_readmes_have_required_sections():
    required_sections = [
        "## Features",
        "## Run",
        "## Gameplay",
        "## Helper Systems Used",
    ]

    for template_name in UPGRADED_TEMPLATES:
        content = read_readme(template_name)

        for section in required_sections:
            assert section in content, f"{template_name} README missing {section}"


def test_all_upgraded_template_readmes_mention_expected_helpers():
    for template_name, helpers in UPGRADED_TEMPLATES.items():
        content = read_readme(template_name)

        for helper in helpers:
            assert helper in content, f"{template_name} README missing {helper}"


def test_template_quality_checklist_doc_exists():
    path = Path("docs/TEMPLATE_QUALITY_CHECKLIST.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "Template Quality Checklist" in content
    assert "Required Files" in content
    assert "Required Template Code Standards" in content
    assert "Required README Sections" in content
    assert "Helper-Based Template Expectations" in content
    assert "tap_counter" in content
    assert "simple_physics" in content
'''

Path("docs/TEMPLATE_QUALITY_CHECKLIST.md").write_text(
    quality_doc,
    encoding="utf-8",
)

Path("tests/test_template_quality_phase34.py").write_text(
    quality_test,
    encoding="utf-8",
)

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

link_line = "- [Template Quality Checklist](docs/TEMPLATE_QUALITY_CHECKLIST.md)"

if link_line not in readme:
    marker = "## Documentation"

    if marker in readme:
        readme = readme.replace(marker, marker + "\\n\\n" + link_line)
    else:
        readme += "\\n\\n## Documentation\\n\\n" + link_line + "\\n"

readme_path.write_text(readme, encoding="utf-8")

print("Phase 34 template quality docs and tests created successfully.")
