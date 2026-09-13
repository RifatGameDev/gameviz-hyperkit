from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from difflib import get_close_matches
from importlib import resources
from importlib.metadata import (
    PackageNotFoundError,
    version,
)
from pathlib import Path

from .android import (
    DEFAULT_ANDROID_API,
    DEFAULT_ANDROID_ARCHS,
    DEFAULT_ANDROID_MIN_API,
    DEFAULT_ANDROID_PERMISSIONS,
    DEFAULT_APP_VERSION,
    DEFAULT_PACKAGE_DOMAIN,
    SUPPORTED_ORIENTATIONS,
    create_buildozer_spec,
    detect_android_build_environment,
    format_android_readiness_report,
    generate_android_readiness_report,
)

from .audit import (
    format_pre_release_audit_report,
    generate_pre_release_audit_report,
)

from .generated_project_validation import (
    format_generated_project_validation_report,
    generate_generated_project_validation_report,
)

from .health import (
    format_health_report,
    generate_health_report,
)

from .release import (
    format_release_report,
    generate_release_report,
)

from .release_evidence import (
    format_release_evidence_report,
    generate_release_evidence_report,
)

from .template_validation import (
    format_template_validation_report,
    generate_template_validation_report,
)

try:
    import tomllib

except ModuleNotFoundError:
    import tomli as tomllib


TEMPLATES = {
    "tap-counter": {
        "folder": "tap_counter",
        "description": (
            "Simple tap/click game. Good for "
            "tap-to-score, tap-to-move, and "
            "beginner prototypes."
        ),
    },

    "flappy-mini": {
        "folder": "flappy_mini",
        "description": (
            "Small flappy-style prototype "
            "with tap-to-jump style gameplay."
        ),
    },

    "swipe-runner": {
        "folder": "swipe_runner",
        "description": (
            "3-lane swipe runner prototype "
            "with obstacles, score, and game over."
        ),
    },

    "puzzle-game": {
        "folder": "puzzle_game",
        "description": (
            "3x3 color matching puzzle prototype "
            "with score, target color, and restart."
        ),
    },

    "quiz-game": {
        "folder": "quiz_game",
        "description": (
            "Educational quiz prototype with "
            "questions, answer buttons, score, "
            "and result screen."
        ),
    },

    "simple-physics": {
        "folder": "simple_physics",
        "description": (
            "Physics prototype with gravity, "
            "bounce, coin collection, score, "
            "and restart."
        ),
    },
}


def get_hyperkit_version() -> str:
    try:
        return version(
            "gameviz-hyperkit"
        )

    except PackageNotFoundError:
        return "0.0.0-dev"


def normalize_template_name(
    template: str,
) -> str:
    return (
        template
        .strip()
        .lower()
        .replace(
            "_",
            "-",
        )
    )


def available_template_names(
) -> list[str]:
    return list(
        TEMPLATES.keys()
    )


def format_available_templates(
) -> str:
    return ", ".join(
        available_template_names()
    )


def suggest_template_name(
    template: str,
) -> str | None:
    template_key = (
        normalize_template_name(
            template
        )
    )

    matches = get_close_matches(
        template_key,
        available_template_names(),
        n=1,
        cutoff=0.55,
    )

    if matches:
        return matches[0]

    return None


def validate_template_name(
    template: str,
) -> str:
    if (
        not template
        or not template.strip()
    ):
        raise ValueError(
            "Template name is required. "
            "Run 'hyperkit list-templates' "
            "to see available templates."
        )

    template_key = (
        normalize_template_name(
            template
        )
    )

    if template_key not in TEMPLATES:
        available = (
            format_available_templates()
        )

        suggestion = (
            suggest_template_name(
                template
            )
        )

        message = (
            f"Unknown template '{template}'. "
            f"Available templates: {available}. "
            "Run 'hyperkit list-templates' "
            "to see details."
        )

        if suggestion:
            message += (
                f" Did you mean "
                f"'{suggestion}'?"
            )

        raise ValueError(
            message
        )

    return template_key


def get_template_folder(
    template: str,
) -> str:
    template_key = (
        validate_template_name(
            template
        )
    )

    return TEMPLATES[
        template_key
    ]["folder"]


def copy_template(
    template: str,
    destination: Path,
) -> None:
    template_key = (
        validate_template_name(
            template
        )
    )

    if (
        destination.exists()
        and any(
            destination.iterdir()
        )
    ):
        raise FileExistsError(
            f"Destination "
            f"'{destination}' "
            f"already exists and "
            f"is not empty."
        )

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    template_folder = (
        TEMPLATES[
            template_key
        ]["folder"]
    )

    package_files = (
        resources.files(
            "hyperkit"
        )
        / "templates"
        / template_folder
    )

    if not package_files.is_dir():
        raise FileNotFoundError(
            "Template folder missing: "
            f"{template_folder}"
        )

    for item in (
        package_files.iterdir()
    ):
        target = (
            destination
            / item.name
        )

        if item.is_dir():
            shutil.copytree(
                str(item),
                target,
                dirs_exist_ok=True,
            )

        else:
            target.write_bytes(
                item.read_bytes()
            )


def write_project_metadata(
    project_path: Path,
    project_name: str,
    template: str,
) -> Path:
    template_key = (
        validate_template_name(
            template
        )
    )

    template_folder = (
        get_template_folder(
            template_key
        )
    )

    metadata_path = (
        project_path
        / "hyperkit.toml"
    )

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

    metadata_path.write_text(
        metadata,
        encoding="utf-8",
    )

    return metadata_path


def write_file_if_missing(
    path: Path,
    content: str = "",
) -> None:
    if not path.exists():
        path.write_text(
            content,
            encoding="utf-8",
        )


def create_project_asset_structure(
    project_path: Path,
) -> None:
    assets_root = (
        project_path
        / "assets"
    )

    asset_folders = [
        assets_root,
        assets_root / "images",
        assets_root / "audio",
        assets_root / "fonts",
        assets_root / "data",
    ]

    for folder in asset_folders:
        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

    write_file_if_missing(
        assets_root
        / "README.md",
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

FBX is not directly supported in HyperKit's 2D runtime.

FBX is mainly a 3D source asset format. For 2D HyperKit games, export your FBX model as:

- PNG image
- PNG animation frames
- Sprite sheet

Then place the exported files inside `assets/images/`.

Keep your game assets organized so your project stays clean.
""",
    )

    for folder in (
        asset_folders[1:]
    ):
        write_file_if_missing(
            folder / ".gitkeep",
            "",
        )


def create_project(
    project_name: str,
    template: str,
    destination: Path | None = None,
) -> Path:
    template_key = (
        validate_template_name(
            template
        )
    )

    project_path = (
        destination
        or (
            Path.cwd()
            / project_name
        )
    )

    project_path = (
        Path(
            project_path
        ).resolve()
    )

    copy_template(
        template_key,
        project_path,
    )

    write_project_metadata(
        project_path,
        project_name=project_name,
        template=template_key,
    )

    create_project_asset_structure(
        project_path
    )

    return project_path


def read_project_metadata(
    project_path: Path,
) -> dict:
    metadata_path = (
        project_path
        / "hyperkit.toml"
    )

    if not metadata_path.exists():
        raise FileNotFoundError(
            "Project metadata "
            "not found: "
            f"{metadata_path}"
        )

    return tomllib.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )


def validate_project(
    project_path: Path,
) -> tuple[
    bool,
    list[str],
]:
    issues: list[str] = []

    if not project_path.exists():
        issues.append(
            "Project path "
            "does not exist: "
            f"{project_path}"
        )

        return (
            False,
            issues,
        )

    main_file = (
        project_path
        / "main.py"
    )

    metadata_file = (
        project_path
        / "hyperkit.toml"
    )

    if not main_file.exists():
        issues.append(
            "Missing main.py"
        )

    if not metadata_file.exists():
        issues.append(
            "Missing hyperkit.toml "
            "project metadata"
        )

    else:
        try:
            metadata = (
                read_project_metadata(
                    project_path
                )
            )

            template = (
                metadata
                .get(
                    "project",
                    {},
                )
                .get(
                    "template"
                )
            )

            if template:
                validate_template_name(
                    template
                )

            else:
                issues.append(
                    "hyperkit.toml "
                    "is missing "
                    "project.template"
                )

        except Exception as exc:
            issues.append(
                "Invalid hyperkit.toml: "
                f"{exc}"
            )

    required_folders = [
        "assets",
        "assets/images",
        "assets/audio",
        "assets/fonts",
        "assets/data",
    ]

    for folder in (
        required_folders
    ):
        if not (
            project_path
            / folder
        ).exists():
            issues.append(
                f"Missing folder: "
                f"{folder}"
            )

    return (
        len(issues) == 0,
        issues,
    )


def cmd_new(
    args: argparse.Namespace,
) -> int:
    destination = (
        Path(
            args.name
        ).resolve()
    )

    create_project(
        project_name=(
            destination.name
        ),
        template=args.template,
        destination=destination,
    )

    print(
        "Created HyperKit "
        f"project: {destination}"
    )

    print(
        "Template: "
        f"{validate_template_name(args.template)}"
    )

    print("")

    print(
        "Next steps:"
    )

    print(
        f"  cd "
        f"{destination.name}"
    )

    print(
        "  python main.py"
    )

    return 0


def cmd_list_templates(
    args: argparse.Namespace,
) -> int:
    print(
        "Available HyperKit "
        "templates"
    )

    print(
        "----------------------------"
    )

    for (
        name,
        info,
    ) in TEMPLATES.items():
        print(
            f"- {name}"
        )

        print(
            "  "
            f"{info['description']}"
        )

    return 0


def cmd_info(
    args: argparse.Namespace,
) -> int:
    project_path = (
        Path(
            args.path
        ).resolve()
    )

    try:
        metadata = (
            read_project_metadata(
                project_path
            )
        )

    except FileNotFoundError:
        print(
            "No hyperkit.toml "
            "found in this project.",
            file=sys.stderr,
        )

        print(
            "This may be an older "
            "project or a manually "
            "created project.",
            file=sys.stderr,
        )

        return 1

    project = metadata.get(
        "project",
        {},
    )

    run = metadata.get(
        "run",
        {},
    )

    print(
        "HyperKit Project Info"
    )

    print(
        "---------------------"
    )

    print(
        "Name: "
        f"{project.get('name', 'unknown')}"
    )

    print(
        "Template: "
        f"{project.get('template', 'unknown')}"
    )

    print(
        "Template Folder: "
        f"{project.get('template_folder', 'unknown')}"
    )

    print(
        "Created By: "
        f"{project.get('created_by', 'unknown')}"
    )

    print(
        "HyperKit Version: "
        f"{project.get('hyperkit_version', 'unknown')}"
    )

    print(
        "Main File: "
        f"{run.get('main', 'main.py')}"
    )

    return 0


def cmd_validate(
    args: argparse.Namespace,
) -> int:
    project_path = (
        Path(
            args.path
        ).resolve()
    )

    (
        is_valid,
        issues,
    ) = validate_project(
        project_path
    )

    print(
        "HyperKit Project Validation"
    )

    print(
        "---------------------------"
    )

    print(
        f"Path: {project_path}"
    )

    if is_valid:
        print(
            "Status: valid"
        )

        return 0

    print(
        "Status: invalid"
    )

    for issue in issues:
        print(
            f"- {issue}"
        )

    return 1


def cmd_validate_templates(
    args: argparse.Namespace,
) -> int:
    root = getattr(
        args,
        "path",
        ".",
    )

    report = (
        generate_template_validation_report(
            root
        )
    )

    print(
        format_template_validation_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def cmd_validate_generated_projects(
    args: argparse.Namespace,
) -> int:
    work_root = getattr(
        args,
        "work_path",
        None,
    )

    report = (
        generate_generated_project_validation_report(
            work_root=work_root
        )
    )

    print(
        format_generated_project_validation_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def cmd_validate_release_evidence(
    args: argparse.Namespace,
) -> int:
    root = getattr(
        args,
        "path",
        ".",
    )

    require_complete = getattr(
        args,
        "require_complete",
        False,
    )

    report = (
        generate_release_evidence_report(
            root
        )
    )

    print(
        format_release_evidence_report(
            report
        )
    )

    if not report.passed:
        return 1

    if (
        require_complete
        and not report.all_complete
    ):
        print("")

        print(
            "Strict evidence validation "
            "failed: runtime QA evidence "
            "is not complete."
        )

        return 1

    return 0


def cmd_run(
    args: argparse.Namespace,
) -> int:
    project_path = (
        Path(
            args.path
        ).resolve()
    )

    main_file = (
        project_path
        / "main.py"
    )

    if not project_path.exists():
        print(
            "Project path "
            "does not exist: "
            f"{project_path}",
            file=sys.stderr,
        )

        print(
            "Tip: run this command "
            "inside a HyperKit project, "
            "or use 'hyperkit run "
            "--path path/to/project'.",
            file=sys.stderr,
        )

        return 1

    if not main_file.exists():
        print(
            "Could not find main.py "
            f"in: {project_path}",
            file=sys.stderr,
        )

        print(
            "Tip: make sure this is "
            "a generated HyperKit project, "
            "or use 'hyperkit run "
            "--path path/to/project'.",
            file=sys.stderr,
        )

        return 1

    return subprocess.call(
        [
            sys.executable,
            str(main_file),
        ]
    )


def _android_permissions_from_args(
    args: argparse.Namespace,
) -> tuple[str, ...]:
    values = getattr(
        args,
        "permission",
        None,
    )

    if values is None:
        return (
            DEFAULT_ANDROID_PERMISSIONS
        )

    return tuple(
        values
    )


def _android_archs_from_args(
    args: argparse.Namespace,
) -> tuple[str, ...]:
    values = getattr(
        args,
        "arch",
        None,
    )

    if values is None:
        return (
            DEFAULT_ANDROID_ARCHS
        )

    return tuple(
        values
    )


def cmd_init_android(
    args: argparse.Namespace,
) -> int:
    spec = create_buildozer_spec(
        path=args.path,
        title=args.title,
        overwrite=args.overwrite,
        package_name=args.package_name,
        package_domain=args.package_domain,
        version=args.app_version,
        orientation=args.orientation,
        fullscreen=args.fullscreen,
        permissions=(
            _android_permissions_from_args(
                args
            )
        ),
        android_api=args.android_api,
        min_api=args.min_api,
        ndk=args.ndk,
        archs=(
            _android_archs_from_args(
                args
            )
        ),
    )

    print(
        "HyperKit Android Configuration"
    )

    print(
        "------------------------------"
    )

    print(
        f"Spec: {spec}"
    )

    print(
        f"Title: {args.title}"
    )

    print(
        "Package domain: "
        f"{args.package_domain}"
    )

    print(
        "Orientation: "
        f"{args.orientation}"
    )

    print(
        "Fullscreen: "
        f"{'yes' if args.fullscreen else 'no'}"
    )

    print(
        "Android API: "
        f"{args.android_api}"
    )

    print(
        "Minimum API: "
        f"{args.min_api}"
    )

    print("")

    print(
        "Next:"
    )

    print(
        "  hyperkit android-doctor"
    )

    print(
        "  hyperkit build android"
    )

    return 0


def cmd_android_doctor(
    args: argparse.Namespace,
) -> int:
    report = (
        generate_android_readiness_report(
            args.path,
            require_build_tools=args.strict,
        )
    )

    print(
        format_android_readiness_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def cmd_build_android(
    args: argparse.Namespace,
) -> int:
    project_path = (
        Path(
            args.path
        ).resolve()
    )

    spec_path = (
        project_path
        / "buildozer.spec"
    )

    if not project_path.exists():
        print(
            "Project path "
            "does not exist: "
            f"{project_path}",
            file=sys.stderr,
        )

        return 1

    if not spec_path.exists():
        create_buildozer_spec(
            path=project_path,
            title=args.title,
        )

        print(
            "Created Android "
            "configuration: "
            f"{spec_path}"
        )

    report = (
        generate_android_readiness_report(
            project_path,
            require_build_tools=True,
        )
    )

    if not report.passed:
        print(
            format_android_readiness_report(
                report
            ),
            file=sys.stderr,
        )

        print(
            "",
            file=sys.stderr,
        )

        print(
            "Android build cannot "
            "start until the required "
            "checks pass.",
            file=sys.stderr,
        )

        return 1

    environment = (
        report.environment
    )

    buildozer = (
        environment.buildozer_path
    )

    if buildozer is None:
        print(
            "Buildozer is not available.",
            file=sys.stderr,
        )

        return 1

    print(
        "Starting Android "
        f"{args.mode} build in: "
        f"{project_path}"
    )

    return subprocess.call(
        [
            buildozer,
            "android",
            args.mode,
        ],
        cwd=project_path,
    )


def cmd_doctor(
    args: argparse.Namespace,
) -> int:
    print(
        "HyperKit Doctor"
    )

    print(
        "---------------"
    )

    print(
        "HyperKit: "
        f"{get_hyperkit_version()}"
    )

    print(
        "Python: "
        f"{sys.version.split()[0]}"
    )

    try:
        import kivy  # type: ignore

        print(
            f"Kivy: {kivy.__version__}"
        )

    except Exception:
        print(
            "Kivy: not installed"
        )

    environment = (
        detect_android_build_environment()
    )

    print(
        "Host: "
        f"{environment.host_platform}"
    )

    print(
        "Buildozer: "
        f"{environment.buildozer_path or 'not installed'}"
    )

    print(
        "Java: "
        f"{environment.java_path or 'not found'}"
    )

    print(
        "ADB: "
        f"{environment.adb_path or 'not found'}"
    )

    if environment.wsl_path:
        print(
            "WSL: "
            f"{environment.wsl_path}"
        )

    print(
        "Android: "
        f"{environment.guidance}"
    )

    return 0


def cmd_health(
    args: argparse.Namespace,
) -> int:
    root = getattr(
        args,
        "path",
        ".",
    )

    report = (
        generate_health_report(
            root
        )
    )

    print(
        format_health_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def cmd_release_check(
    args: argparse.Namespace,
) -> int:
    root = getattr(
        args,
        "path",
        ".",
    )

    report = (
        generate_release_report(
            root
        )
    )

    print(
        format_release_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def cmd_pre_release_audit(
    args: argparse.Namespace,
) -> int:
    root = getattr(
        args,
        "path",
        ".",
    )

    report = (
        generate_pre_release_audit_report(
            root
        )
    )

    print(
        format_pre_release_audit_report(
            report
        )
    )

    return (
        0
        if report.passed
        else 1
    )


def _add_android_config_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    parser.add_argument(
        "--path",
        default=".",
    )

    parser.add_argument(
        "--title",
        default="HyperKit Game",
    )

    parser.add_argument(
        "--package-name",
        default=None,
    )

    parser.add_argument(
        "--package-domain",
        default=DEFAULT_PACKAGE_DOMAIN,
    )

    parser.add_argument(
        "--app-version",
        default=DEFAULT_APP_VERSION,
    )

    parser.add_argument(
        "--orientation",
        choices=SUPPORTED_ORIENTATIONS,
        default="portrait",
    )

    parser.add_argument(
        "--fullscreen",
        action="store_true",
        help=(
            "Use fullscreen mode "
            "on mobile"
        ),
    )

    parser.add_argument(
        "--permission",
        action="append",
        default=None,
        help=(
            "Android permission. "
            "Repeat for multiple "
            "permissions, for example "
            "--permission INTERNET "
            "--permission VIBRATE."
        ),
    )

    parser.add_argument(
        "--android-api",
        type=int,
        default=DEFAULT_ANDROID_API,
    )

    parser.add_argument(
        "--min-api",
        type=int,
        default=DEFAULT_ANDROID_MIN_API,
    )

    parser.add_argument(
        "--ndk",
        default=None,
        help=(
            "Optional explicit Android "
            "NDK version. Omit to let "
            "the toolchain choose."
        ),
    )

    parser.add_argument(
        "--arch",
        action="append",
        default=None,
        help=(
            "Android CPU architecture. "
            "Repeat for multiple "
            "architectures. Defaults to "
            "arm64-v8a and armeabi-v7a."
        ),
    )


def build_parser(
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hyperkit",
        description=(
            "GameViz HyperKit CLI for "
            "creating 2D hypercasual "
            "game prototypes."
        ),
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    p_new = sub.add_parser(
        "new",
        help=(
            "Create a new HyperKit "
            "game project"
        ),
    )

    p_new.add_argument(
        "name",
        help="Project folder name",
    )

    p_new.add_argument(
        "--template",
        default="tap-counter",
        help=(
            "Template name. Example: "
            "tap-counter, tap_counter, "
            "flappy-mini, flappy_mini"
        ),
    )

    p_new.set_defaults(
        func=cmd_new
    )

    p_list = sub.add_parser(
        "list-templates",
        help=(
            "Show available "
            "game templates"
        ),
    )

    p_list.set_defaults(
        func=cmd_list_templates
    )

    p_info = sub.add_parser(
        "info",
        help=(
            "Show HyperKit "
            "project metadata"
        ),
    )

    p_info.add_argument(
        "--path",
        default=".",
    )

    p_info.set_defaults(
        func=cmd_info
    )

    p_validate = sub.add_parser(
        "validate",
        help=(
            "Validate a "
            "HyperKit project"
        ),
    )

    p_validate.add_argument(
        "--path",
        default=".",
    )

    p_validate.set_defaults(
        func=cmd_validate
    )

    p_run = sub.add_parser(
        "run",
        help=(
            "Run a HyperKit "
            "game project"
        ),
    )

    p_run.add_argument(
        "--path",
        default=".",
    )

    p_run.set_defaults(
        func=cmd_run
    )

    p_init_android = (
        sub.add_parser(
            "init-android",
            help=(
                "Create Android "
                "build configuration"
            ),
        )
    )

    _add_android_config_arguments(
        p_init_android
    )

    p_init_android.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace an existing "
            "buildozer.spec"
        ),
    )

    p_init_android.set_defaults(
        func=cmd_init_android
    )

    p_android_doctor = (
        sub.add_parser(
            "android-doctor",
            help=(
                "Check Android/mobile "
                "build readiness"
            ),
        )
    )

    p_android_doctor.add_argument(
        "--path",
        default=".",
    )

    p_android_doctor.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Require a directly "
            "usable Android "
            "build toolchain"
        ),
    )

    p_android_doctor.set_defaults(
        func=cmd_android_doctor
    )

    p_build = sub.add_parser(
        "build",
        help=(
            "Build project targets"
        ),
    )

    p_build.add_argument(
        "target",
        choices=[
            "android",
        ],
    )

    p_build.add_argument(
        "--path",
        default=".",
    )

    p_build.add_argument(
        "--title",
        default="HyperKit Game",
    )

    p_build.add_argument(
        "--mode",
        choices=[
            "debug",
            "release",
        ],
        default="debug",
    )

    p_build.set_defaults(
        func=lambda args: (
            cmd_build_android(
                args
            )
            if (
                args.target
                == "android"
            )
            else 1
        )
    )

    p_doctor = sub.add_parser(
        "doctor",
        help=(
            "Check local "
            "HyperKit environment"
        ),
    )

    p_doctor.set_defaults(
        func=cmd_doctor
    )

    p_health = sub.add_parser(
        "health",
        help=(
            "Show HyperKit "
            "project health report"
        ),
    )

    p_health.add_argument(
        "--path",
        default=".",
        help=(
            "Project root "
            "path to check"
        ),
    )

    p_health.set_defaults(
        func=cmd_health
    )

    p_release_check = (
        sub.add_parser(
            "release-check",
            help=(
                "Show HyperKit "
                "release readiness "
                "report"
            ),
        )
    )

    p_release_check.add_argument(
        "--path",
        default=".",
        help=(
            "Project root "
            "path to check"
        ),
    )

    p_release_check.set_defaults(
        func=cmd_release_check
    )

    p_pre_release_audit = (
        sub.add_parser(
            "pre-release-audit",
            help=(
                "Show HyperKit final "
                "pre-release audit report"
            ),
        )
    )

    p_pre_release_audit.add_argument(
        "--path",
        default=".",
        help=(
            "Project root "
            "path to check"
        ),
    )

    p_pre_release_audit.set_defaults(
        func=cmd_pre_release_audit
    )

    p_validate_templates = (
        sub.add_parser(
            "validate-templates",
            help=(
                "Validate built-in "
                "HyperKit templates"
            ),
        )
    )

    p_validate_templates.add_argument(
        "--path",
        default=".",
        help=(
            "Repository root "
            "path to check"
        ),
    )

    p_validate_templates.set_defaults(
        func=cmd_validate_templates
    )

    p_validate_generated_projects = (
        sub.add_parser(
            "validate-generated-projects",
            help=(
                "Generate and validate "
                "all polished "
                "HyperKit templates"
            ),
        )
    )

    p_validate_generated_projects.add_argument(
        "--work-path",
        default=None,
        help=(
            "Optional directory for "
            "generated validation projects. "
            "A temporary directory is "
            "used by default."
        ),
    )

    p_validate_generated_projects.set_defaults(
        func=(
            cmd_validate_generated_projects
        )
    )

    p_validate_release_evidence = (
        sub.add_parser(
            "validate-release-evidence",
            help=(
                "Validate runtime QA "
                "tracker and release "
                "evidence"
            ),
        )
    )

    p_validate_release_evidence.add_argument(
        "--path",
        default=".",
        help=(
            "Repository root "
            "path to validate"
        ),
    )

    p_validate_release_evidence.add_argument(
        "--require-complete",
        action="store_true",
        help=(
            "Fail unless every polished "
            "template has completed "
            "passing runtime QA evidence"
        ),
    )

    p_validate_release_evidence.set_defaults(
        func=(
            cmd_validate_release_evidence
        )
    )

    return parser


def main(
    argv: list[str] | None = None,
) -> int:
    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    if not hasattr(
        args,
        "func",
    ):
        parser.print_help()

        return 0

    try:
        return args.func(
            args
        )

    except Exception as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
