from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from difflib import get_close_matches
from importlib import resources
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .android import create_buildozer_spec

from .health import format_health_report, generate_health_report
from .release import format_release_report, generate_release_report
from .audit import format_pre_release_audit_report, generate_pre_release_audit_report

from .template_validation import (
    format_template_validation_report,
    generate_template_validation_report,
)

from .generated_project_validation import (
    format_generated_project_validation_report,
    generate_generated_project_validation_report,
)

from .release_evidence import (
    format_release_evidence_report,
    generate_release_evidence_report,
)

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 fallback
    tomllib = None


TEMPLATES = {
    "tap-counter": {
        "folder": "tap_counter",
        "description": "Simple tap/click game. Good for tap-to-score, tap-to-move, and beginner prototypes.",
    },
    "flappy-mini": {
        "folder": "flappy_mini",
        "description": "Small flappy-style prototype with tap-to-jump style gameplay.",
    },
    "swipe-runner": {
        "folder": "swipe_runner",
        "description": "3-lane swipe runner prototype with obstacles, score, and game over.",
    },
    "puzzle-game": {
        "folder": "puzzle_game",
        "description": "3x3 color matching puzzle prototype with score, target color, and restart.",
    },
    "quiz-game": {
        "folder": "quiz_game",
        "description": "Educational quiz prototype with questions, answer buttons, score, and result screen.",
    },
    "simple-physics": {
        "folder": "simple_physics",
        "description": "Physics prototype with gravity, bounce, coin collection, score, and restart.",
    },
}


def get_hyperkit_version() -> str:
    try:
        return version("gameviz-hyperkit")
    except PackageNotFoundError:
        return "0.0.0-dev"


def normalize_template_name(template: str) -> str:
    return template.strip().lower().replace("_", "-")


def available_template_names() -> list[str]:
    return list(TEMPLATES.keys())


def format_available_templates() -> str:
    return ", ".join(available_template_names())


def suggest_template_name(template: str) -> str | None:
    template_key = normalize_template_name(template)

    matches = get_close_matches(
        template_key,
        available_template_names(),
        n=1,
        cutoff=0.55,
    )

    if matches:
        return matches[0]

    return None


def validate_template_name(template: str) -> str:
    template_key = normalize_template_name(template)

    if template_key not in TEMPLATES:
        available = ", ".join(available_template_names())
        raise ValueError(
            f"Unknown template '{template}'. Available templates: {available}")

    return template_key


def validate_template_name(template: str) -> str:
    if not template or not template.strip():
        raise ValueError(
            "Template name is required. "
            "Run 'hyperkit list-templates' to see available templates."
        )

    template_key = normalize_template_name(template)

    if template_key not in TEMPLATES:
        available = format_available_templates()
        suggestion = suggest_template_name(template)

        message = (
            f"Unknown template '{template}'. "
            f"Available templates: {available}. "
            "Run 'hyperkit list-templates' to see details."
        )

        if suggestion:
            message += f" Did you mean '{suggestion}'?"

        raise ValueError(message)

    return template_key


def get_template_folder(template: str) -> str:
    template_key = validate_template_name(template)
    return TEMPLATES[template_key]["folder"]


def copy_template(template: str, destination: Path) -> None:
    template_key = validate_template_name(template)

    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(
            f"Destination '{destination}' already exists and is not empty.")

    destination.mkdir(parents=True, exist_ok=True)

    template_folder = TEMPLATES[template_key]["folder"]
    package_files = resources.files("hyperkit") / "templates" / template_folder

    if not package_files.is_dir():
        raise FileNotFoundError(f"Template folder missing: {template_folder}")

    for item in package_files.iterdir():
        target = destination / item.name

        if item.is_dir():
            shutil.copytree(str(item), target, dirs_exist_ok=True)
        else:
            target.write_bytes(item.read_bytes())


def write_project_metadata(project_path: Path, project_name: str, template: str) -> Path:
    template_key = validate_template_name(template)
    template_folder = get_template_folder(template_key)

    metadata_path = project_path / "hyperkit.toml"
    metadata = f'''[project]
name = "{project_name}"
template = "{template_key}"
template_folder = "{template_folder}"
created_by = "gameviz-hyperkit"
hyperkit_version = "{get_hyperkit_version()}"

[run]
main = "main.py"

[assets]
root = "assets"
images = "assets/images"
audio = "assets/audio"
fonts = "assets/fonts"
data = "assets/data"
'''

    metadata_path.write_text(metadata, encoding="utf-8")
    return metadata_path


def write_file_if_missing(path: Path, content: str = "") -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def create_project_asset_structure(project_path: Path) -> None:
    assets_root = project_path / "assets"

    asset_folders = [
        assets_root,
        assets_root / "images",
        assets_root / "audio",
        assets_root / "fonts",
        assets_root / "data",
    ]

    for folder in asset_folders:
        folder.mkdir(parents=True, exist_ok=True)

    write_file_if_missing(
        assets_root / "README.md",
        """# Assets Folder

This folder contains game assets for your HyperKit project.

## Folders

- `images/` — sprites, icons, backgrounds, UI images
- `audio/` — sound effects and music
- `fonts/` — custom font files
- `data/` — JSON, CSV, level data, quiz data, and other game data

## Supported Types

- Images: `.png`, `.jpg`, `.jpeg`, `.webp`
- Audio: `.wav`, `.mp3`, `.ogg`
- Fonts: `.ttf`, `.otf`
- Data: `.json`, `.csv`, `.txt`

## FBX Note

FBX is not directly supported in HyperKit v0.2.

FBX is mainly a 3D source asset format. For 2D HyperKit games, export your FBX model as:

- PNG image
- PNG animation frames
- Sprite sheet

Then place the exported files inside `assets/images/`.

Keep your game assets organized so your project stays clean.
""",
    )

    for folder in asset_folders[1:]:
        write_file_if_missing(folder / ".gitkeep", "")


def create_project(project_name: str, template: str, destination: Path) -> Path:
    template_key = validate_template_name(template)
    copy_template(template_key, destination)
    write_project_metadata(
        destination, project_name=project_name, template=template_key)
    create_project_asset_structure(destination)
    return destination


def _read_toml_fallback(path: Path) -> dict[str, dict[str, str]]:
    data: dict[str, dict[str, str]] = {}
    current_section: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            data[current_section] = {}
            continue

        if "=" in line and current_section:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"')
            data[current_section][key] = value

    return data


def read_project_metadata(project_path: Path) -> dict:
    metadata_path = project_path / "hyperkit.toml"

    if not metadata_path.exists():
        raise FileNotFoundError(f"Project metadata not found: {metadata_path}")

    if tomllib is not None:
        return tomllib.loads(metadata_path.read_text(encoding="utf-8"))

    return _read_toml_fallback(metadata_path)


def validate_project(project_path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []

    if not project_path.exists():
        issues.append(f"Project path does not exist: {project_path}")
        return False, issues

    main_file = project_path / "main.py"
    metadata_file = project_path / "hyperkit.toml"

    if not main_file.exists():
        issues.append("Missing main.py")

    if not metadata_file.exists():
        issues.append("Missing hyperkit.toml project metadata")
    else:
        try:
            metadata = read_project_metadata(project_path)
            template = metadata.get("project", {}).get("template")

            if template:
                validate_template_name(template)
            else:
                issues.append("hyperkit.toml is missing project.template")
        except Exception as exc:
            issues.append(f"Invalid hyperkit.toml: {exc}")

    required_folders = [
        "assets",
        "assets/images",
        "assets/audio",
        "assets/fonts",
        "assets/data",
    ]

    for folder in required_folders:
        if not (project_path / folder).exists():
            issues.append(f"Missing folder: {folder}")

    return len(issues) == 0, issues


def cmd_new(args: argparse.Namespace) -> int:
    destination = Path(args.name).resolve()
    create_project(project_name=destination.name,
                   template=args.template, destination=destination)

    print(f"Created HyperKit project: {destination}")
    print(f"Template: {validate_template_name(args.template)}")
    print("")
    print("Next steps:")
    print(f"  cd {destination.name}")
    print("  python main.py")
    return 0


def cmd_list_templates(args: argparse.Namespace) -> int:
    print("Available HyperKit templates")
    print("----------------------------")

    for name, info in TEMPLATES.items():
        print(f"- {name}")
        print(f"  {info['description']}")

    return 0


def cmd_info(args: argparse.Namespace) -> int:
    project_path = Path(args.path).resolve()

    try:
        metadata = read_project_metadata(project_path)
    except FileNotFoundError:
        print("No hyperkit.toml found in this project.", file=sys.stderr)
        print(
            "This may be an older project or a manually created project.", file=sys.stderr)
        return 1

    project = metadata.get("project", {})
    run = metadata.get("run", {})

    print("HyperKit Project Info")
    print("---------------------")
    print(f"Name: {project.get('name', 'unknown')}")
    print(f"Template: {project.get('template', 'unknown')}")
    print(f"Template Folder: {project.get('template_folder', 'unknown')}")
    print(f"Created By: {project.get('created_by', 'unknown')}")
    print(f"HyperKit Version: {project.get('hyperkit_version', 'unknown')}")
    print(f"Main File: {run.get('main', 'main.py')}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    project_path = Path(args.path).resolve()
    is_valid, issues = validate_project(project_path)

    print("HyperKit Project Validation")
    print("---------------------------")
    print(f"Path: {project_path}")

    if is_valid:
        print("Status: valid")
        return 0

    print("Status: invalid")
    for issue in issues:
        print(f"- {issue}")

    return 1


def cmd_validate_templates(args: argparse.Namespace) -> int:
    root = getattr(args, "path", ".")
    report = generate_template_validation_report(root)

    print(format_template_validation_report(report))

    return 0 if report.passed else 1


def cmd_validate_generated_projects(args: argparse.Namespace) -> int:
    work_root = getattr(args, "work_path", None)

    report = generate_generated_project_validation_report(
        work_root=work_root
    )

    print(format_generated_project_validation_report(report))

    return 0 if report.passed else 1


def cmd_validate_release_evidence(args: argparse.Namespace) -> int:
    root = getattr(args, "path", ".")
    require_complete = getattr(args, "require_complete", False)

    report = generate_release_evidence_report(root)

    print(format_release_evidence_report(report))

    if not report.passed:
        return 1

    if require_complete and not report.all_complete:
        print("")
        print(
            "Strict evidence validation failed: "
            "runtime QA evidence is not complete."
        )
        return 1

    return 0


def cmd_run(args: argparse.Namespace) -> int:
    project_path = Path(args.path).resolve()
    main_file = project_path / "main.py"

    if not project_path.exists():
        print(f"Project path does not exist: {project_path}", file=sys.stderr)
        print(
            "Tip: run this command inside a HyperKit project, "
            "or use 'hyperkit run --path path/to/project'.",
            file=sys.stderr,
        )
        return 1

    if not main_file.exists():
        print(f"Could not find main.py in: {project_path}", file=sys.stderr)
        print(
            "Tip: make sure this is a generated HyperKit project, "
            "or use 'hyperkit run --path path/to/project'.",
            file=sys.stderr,
        )
        return 1

    return subprocess.call([sys.executable, str(main_file)])


def cmd_init_android(args: argparse.Namespace) -> int:
    spec = create_buildozer_spec(
        path=args.path, title=args.title, overwrite=args.overwrite)
    print(f"Android config ready: {spec}")
    return 0


def cmd_build_android(args: argparse.Namespace) -> int:
    project_path = Path(args.path).resolve()
    spec_path = project_path / "buildozer.spec"

    if not spec_path.exists():
        create_buildozer_spec(path=project_path, title=args.title)
        print("Created buildozer.spec")

    buildozer = shutil.which("buildozer")

    if buildozer is None:
        print("Buildozer is not installed.", file=sys.stderr)
        print("Current Android build support is experimental.", file=sys.stderr)
        print("For now, use the desktop runner while we develop the full Android build system.", file=sys.stderr)
        return 1

    return subprocess.call([buildozer, "android", "debug"], cwd=project_path)


def cmd_doctor(args: argparse.Namespace) -> int:
    print("HyperKit Doctor")
    print("---------------")
    print(f"HyperKit: {get_hyperkit_version()}")
    print(f"Python: {sys.version.split()[0]}")

    try:
        import kivy  # type: ignore

        print(f"Kivy: {kivy.__version__}")
    except Exception:
        print("Kivy: not installed")

    buildozer = shutil.which("buildozer")
    print(f"Buildozer: {buildozer or 'not installed'}")

    if sys.platform.startswith("win"):
        print("Note: Android build support is experimental in v0.1.x.")

    return 0


def cmd_health(args):
    root = getattr(args, "path", ".")
    report = generate_health_report(root)

    print(format_health_report(report))

    return 0 if report.passed else 1


def cmd_release_check(args):
    root = getattr(args, "path", ".")
    report = generate_release_report(root)

    print(format_release_report(report))

    return 0 if report.passed else 1


def cmd_pre_release_audit(args):
    root = getattr(args, "path", ".")
    report = generate_pre_release_audit_report(root)

    print(format_pre_release_audit_report(report))

    return 0 if report.passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hyperkit",
        description="GameViz HyperKit CLI for creating 2D hypercasual game prototypes.",
    )

    sub = parser.add_subparsers(dest="command")

    p_new = sub.add_parser("new", help="Create a new HyperKit game project")
    p_new.add_argument("name", help="Project folder name")
    p_new.add_argument(
        "--template",
        default="tap-counter",
        help="Template name. Example: tap-counter, tap_counter, flappy-mini, flappy_mini",
    )
    p_new.set_defaults(func=cmd_new)

    p_list = sub.add_parser(
        "list-templates", help="Show available game templates")
    p_list.set_defaults(func=cmd_list_templates)

    p_info = sub.add_parser("info", help="Show HyperKit project metadata")
    p_info.add_argument("--path", default=".")
    p_info.set_defaults(func=cmd_info)

    p_validate = sub.add_parser("validate", help="Validate a HyperKit project")
    p_validate.add_argument("--path", default=".")
    p_validate.set_defaults(func=cmd_validate)

    p_run = sub.add_parser("run", help="Run a HyperKit game project")
    p_run.add_argument("--path", default=".")
    p_run.set_defaults(func=cmd_run)

    p_init_android = sub.add_parser(
        "init-android", help="Create Android build configuration")
    p_init_android.add_argument("--path", default=".")
    p_init_android.add_argument("--title", default="HyperKit Game")
    p_init_android.add_argument("--overwrite", action="store_true")
    p_init_android.set_defaults(func=cmd_init_android)

    p_build = sub.add_parser("build", help="Build project targets")
    p_build.add_argument("target", choices=["android"])
    p_build.add_argument("--path", default=".")
    p_build.add_argument("--title", default="HyperKit Game")
    p_build.set_defaults(func=lambda args: cmd_build_android(
        args) if args.target == "android" else 1)

    p_doctor = sub.add_parser(
        "doctor", help="Check local HyperKit environment")

    p_doctor.set_defaults(func=cmd_doctor)

    p_health = sub.add_parser(
        "health",
        help="Show HyperKit project health report",
    )
    p_health.add_argument(
        "--path",
        default=".",
        help="Project root path to check",
    )
    p_health.set_defaults(func=cmd_health)

    p_release_check = sub.add_parser(
        "release-check",
        help="Show HyperKit release readiness report",
    )
    p_release_check.add_argument(
        "--path",
        default=".",
        help="Project root path to check",
    )
    p_release_check.set_defaults(func=cmd_release_check)

    p_pre_release_audit = sub.add_parser(
        "pre-release-audit",
        help="Show HyperKit final pre-release audit report",
    )
    p_pre_release_audit.add_argument(
        "--path",
        default=".",
        help="Project root path to check",
    )
    p_pre_release_audit.set_defaults(func=cmd_pre_release_audit)

    p_validate_templates = sub.add_parser(
        "validate-templates",
        help="Validate built-in HyperKit templates",
    )
    p_validate_templates.add_argument(
        "--path",
        default=".",
        help="Repository root path to check",
    )
    p_validate_templates.set_defaults(func=cmd_validate_templates)

    p_validate_generated_projects = sub.add_parser(
        "validate-generated-projects",
        help="Generate and validate all polished HyperKit templates",
    )

    p_validate_generated_projects.add_argument(
        "--work-path",
        default=None,
        help=(
            "Optional directory for generated validation projects. "
            "A temporary directory is used by default."
        ),
    )

    p_validate_generated_projects.set_defaults(
        func=cmd_validate_generated_projects
    )

    p_validate_release_evidence = sub.add_parser(
        "validate-release-evidence",
        help="Validate runtime QA tracker and release evidence",
    )

    p_validate_release_evidence.add_argument(
        "--path",
        default=".",
        help="Repository root path to validate",
    )

    p_validate_release_evidence.add_argument(
        "--require-complete",
        action="store_true",
        help=(
            "Fail unless every polished template has completed "
            "passing runtime QA evidence"
        ),
    )

    p_validate_release_evidence.set_defaults(
        func=cmd_validate_release_evidence
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
