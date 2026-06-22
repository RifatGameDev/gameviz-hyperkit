from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from importlib import resources
from pathlib import Path

from .android import create_buildozer_spec

AVAILABLE_TEMPLATES = ["tap-counter", "flappy-mini"]
TEMPLATE_DIRS = {
    "tap-counter": "tap_counter",
    "flappy-mini": "flappy_mini",
}


def copy_template(template: str, destination: Path) -> None:
    if template not in TEMPLATE_DIRS:
        raise ValueError(f"Unknown template '{template}'. Available: {', '.join(AVAILABLE_TEMPLATES)}")

    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Destination '{destination}' already exists and is not empty.")

    destination.mkdir(parents=True, exist_ok=True)

    package_files = resources.files("hyperkit") / "templates" / TEMPLATE_DIRS[template]
    for item in package_files.iterdir():
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(str(item), target, dirs_exist_ok=True)
        else:
            target.write_bytes(item.read_bytes())


def cmd_new(args: argparse.Namespace) -> int:
    destination = Path(args.name).resolve()
    copy_template(args.template, destination)
    print(f"Created HyperKit project: {destination}")
    print("Next steps:")
    print(f"  cd {destination.name}")
    print("  python main.py")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    main_file = Path(args.path).resolve() / "main.py"
    if not main_file.exists():
        print(f"Could not find {main_file}", file=sys.stderr)
        return 1
    return subprocess.call([sys.executable, str(main_file)])


def cmd_init_android(args: argparse.Namespace) -> int:
    spec = create_buildozer_spec(path=args.path, title=args.title, overwrite=args.overwrite)
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
        print("Buildozer is not installed. Install it on Linux/macOS/WSL with:", file=sys.stderr)
        print("  pip install buildozer", file=sys.stderr)
        return 1

    return subprocess.call([buildozer, "android", "debug"], cwd=project_path)


def cmd_doctor(args: argparse.Namespace) -> int:
    print("HyperKit Doctor")
    print("---------------")
    print(f"Python: {sys.version.split()[0]}")

    try:
        import kivy  # type: ignore

        print(f"Kivy: {kivy.__version__}")
    except Exception:
        print("Kivy: not installed")

    buildozer = shutil.which("buildozer")
    print(f"Buildozer: {buildozer or 'not installed'}")

    if sys.platform.startswith("win"):
        print("Note: Android builds should be done inside WSL/Linux, not native Windows.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hyperkit", description="GameViz HyperKit CLI")
    sub = parser.add_subparsers(dest="command")

    p_new = sub.add_parser("new", help="Create a new HyperKit game project")
    p_new.add_argument("name", help="Project folder name")
    p_new.add_argument("--template", default="tap-counter", choices=AVAILABLE_TEMPLATES)
    p_new.set_defaults(func=cmd_new)

    p_run = sub.add_parser("run", help="Run a HyperKit game project")
    p_run.add_argument("--path", default=".")
    p_run.set_defaults(func=cmd_run)

    p_init_android = sub.add_parser("init-android", help="Create buildozer.spec for Android APK builds")
    p_init_android.add_argument("--path", default=".")
    p_init_android.add_argument("--title", default="HyperKit Game")
    p_init_android.add_argument("--overwrite", action="store_true")
    p_init_android.set_defaults(func=cmd_init_android)

    p_build = sub.add_parser("build", help="Build project targets")
    p_build.add_argument("target", choices=["android"])
    p_build.add_argument("--path", default=".")
    p_build.add_argument("--title", default="HyperKit Game")
    p_build.set_defaults(func=lambda args: cmd_build_android(args) if args.target == "android" else 1)

    p_doctor = sub.add_parser("doctor", help="Check local HyperKit environment")
    p_doctor.set_defaults(func=cmd_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
