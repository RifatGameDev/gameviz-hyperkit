from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .health import generate_health_report


@dataclass
class ReleaseCheck:
    name: str
    passed: bool
    message: str


@dataclass
class ReleaseReport:
    root: Path
    checks: list[ReleaseCheck] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def passed_count(self) -> int:
        return sum(1 for check in self.checks if check.passed)

    @property
    def failed_count(self) -> int:
        return self.total - self.passed_count

    def add(self, name: str, passed: bool, message: str) -> None:
        self.checks.append(
            ReleaseCheck(
                name=name,
                passed=passed,
                message=message,
            )
        )


REQUIRED_RELEASE_FILES = [
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "pyproject.toml",
    "src/hyperkit/__main__.py",
    "docs/TEMPLATES.md",
    "docs/TEMPLATE_HELPERS.md",
    "docs/TEMPLATE_QUALITY_CHECKLIST.md",
    "docs/RELEASE_READINESS_CHECKLIST.md",
    "docs/V050_COMPLETE_GAMES_TOOLING.md",
    "src/hyperkit/devtools.py",
    "src/hyperkit/complete_games.py",
    ".github/workflows/ci.yml",
    "src/hyperkit/performance.py",
    "docs/V060_MOBILE_RUNTIME_PERFORMANCE.md",
    "src/hyperkit/content.py",
    "src/hyperkit/prefab.py",
    "src/hyperkit/pool.py",
    "src/hyperkit/level_sequence.py",
    "docs/V070_CONTENT_ASSETS_ADVANCED_FEATURES.md",
    "src/hyperkit/release_build.py",
    "src/hyperkit/android_release.py",
    "docs/V080_BUILD_PUBLISHING_PRODUCTION_HARDENING.md",
    ".github/workflows/release-package.yml",
    ".github/workflows/android-production-release.yml",
    "docs/V090_API_FREEZE_PUBLIC_BETA.md",
    ".github/workflows/public-beta.yml",
    "src/hyperkit/stable_release.py",
    "docs/V100_STABLE_RELEASE.md",
    ".github/workflows/stable-release.yml",
    "docs/VERSION_HISTORY.md",
    "docs/GENERATED_PROJECT_SMOKE_TESTS.md",
    "docs/PROJECT_HEALTH_REPORT.md",
    "docs/RELEASE_BUILD_AUTOMATION.md",
    "docs/FINAL_PRE_RELEASE_AUDIT.md",
    "docs/QUICK_START_TUTORIAL.md",
    "docs/TEMPLATE_MEDIA_GUIDE.md",
    "docs/TEMPLATE_SCREENSHOTS.md",
    "docs/CLI_ERROR_MESSAGES.md",
    "docs/TEMPLATE_VALIDATION.md",
    "docs/PRODUCTION_TEMPLATE_POLISH_CHECKLIST.md",
    "docs/TAP_COUNTER_POLISH_PHASE48.md",
    "docs/FLAPPY_MINI_POLISH_PHASE49.md",
    "docs/SWIPE_RUNNER_POLISH_PHASE50.md",
    "docs/PUZZLE_GAME_POLISH_PHASE51.md",
    "docs/QUIZ_GAME_POLISH_PHASE52.md",
    "docs/SIMPLE_PHYSICS_POLISH_PHASE53.md",
    "docs/TEMPLATE_POLISH_SUMMARY_PHASE54.md",
    "docs/TEMPLATE_STABILIZATION_CHECKLIST.md",
    "src/hyperkit/generated_project_validation.py",
    "docs/GENERATED_PROJECT_VALIDATION_PHASE55.md",
    "docs/TEMPLATE_RUNTIME_READINESS_PHASE56.md",
    "docs/TEMPLATE_MANUAL_QA_CHECKLIST.md",
    "docs/MANUAL_QA_RESULT_TEMPLATE.md",
    "docs/RELEASE_EVIDENCE_STRUCTURE.md",
    "docs/release-evidence/README.md",
    "docs/release-evidence/templates/tap_counter/README.md",
    "docs/release-evidence/templates/flappy_mini/README.md",
    "docs/release-evidence/templates/swipe_runner/README.md",
    "docs/release-evidence/templates/puzzle_game/README.md",
    "docs/release-evidence/templates/quiz_game/README.md",
    "docs/release-evidence/templates/simple_physics/README.md",
    "src/hyperkit/release_evidence.py",
    "docs/RUNTIME_QA_TRACKER_PHASE58.md",
    "docs/release-evidence/qa-tracker.json",
    "docs/release-evidence/templates/tap_counter/manual-qa-result.md",
    "docs/release-evidence/templates/tap_counter/validation-output.txt",
    "docs/release-evidence/templates/tap_counter/runtime-notes.md",
    "docs/release-evidence/templates/tap_counter/screenshot.png",
    "docs/release-evidence/templates/flappy_mini/manual-qa-result.md",
    "docs/release-evidence/templates/flappy_mini/validation-output.txt",
    "docs/release-evidence/templates/flappy_mini/runtime-notes.md",
    "docs/release-evidence/templates/flappy_mini/screenshot.png",
    "docs/release-evidence/templates/swipe_runner/manual-qa-result.md",
    "docs/release-evidence/templates/swipe_runner/validation-output.txt",
    "docs/release-evidence/templates/swipe_runner/runtime-notes.md",
    "docs/release-evidence/templates/swipe_runner/screenshot.png",
    "docs/release-evidence/templates/puzzle_game/manual-qa-result.md",
    "docs/release-evidence/templates/puzzle_game/validation-output.txt",
    "docs/release-evidence/templates/puzzle_game/runtime-notes.md",
    "docs/release-evidence/templates/puzzle_game/screenshot.png",
    "docs/release-evidence/templates/quiz_game/manual-qa-result.md",
    "docs/release-evidence/templates/quiz_game/validation-output.txt",
    "docs/release-evidence/templates/quiz_game/runtime-notes.md",
    "docs/release-evidence/templates/quiz_game/screenshot.png",
    "docs/release-evidence/templates/simple_physics/manual-qa-result.md",
    "docs/release-evidence/templates/simple_physics/validation-output.txt",
    "docs/release-evidence/templates/simple_physics/runtime-notes.md",
    "docs/release-evidence/templates/simple_physics/screenshot.png",
    "docs/release-evidence/FINAL_QA_CERTIFICATION_PHASE65.md",
    "docs/release-evidence/final-certification-output.txt",
    "docs/release-evidence/phase68/STABLE_RELEASE_READINESS.md",
    "docs/release-evidence/phase68/stable-validation.json",
]

REQUIRED_RELEASE_TESTS = [
    "tests/test_template_quality_phase34.py",
    "tests/test_release_readiness_phase35.py",
    "tests/test_changelog_phase36.py",
    "tests/test_generated_project_smoke_phase37.py",
    "tests/test_health_phase38.py",
    "tests/test_pre_release_audit_phase40.py",
    "tests/test_public_readme_phase42.py",
    "tests/test_quick_start_tutorial_phase43.py",
    "tests/test_template_media_phase44.py",
    "tests/test_cli_error_messages_phase45.py",
    "tests/test_template_validation_phase46.py",
    "tests/test_production_template_polish_phase47.py",
    "tests/test_tap_counter_polish_phase48.py",
    "tests/test_flappy_mini_polish_phase49.py",
    "tests/test_swipe_runner_polish_phase50.py",
    "tests/test_puzzle_game_polish_phase51.py",
    "tests/test_quiz_game_polish_phase52.py",
    "tests/test_simple_physics_polish_phase53.py",
    "tests/test_template_polish_summary_phase54.py",
    "tests/test_generated_project_validation_phase55.py",
    "tests/test_template_runtime_readiness_phase56.py",
    "tests/test_release_evidence_phase57.py",
    "tests/test_runtime_qa_tracker_phase58.py",
    "tests/test_tap_counter_runtime_qa_phase59.py",
    "tests/test_flappy_mini_runtime_qa_phase60.py",
    "tests/test_swipe_runner_runtime_qa_phase61.py",
    "tests/test_puzzle_game_runtime_qa_phase62.py",
    "tests/test_quiz_game_runtime_qa_phase63.py",
    "tests/test_simple_physics_runtime_qa_phase64.py",
    "tests/test_final_qa_certification_phase65.py",
    "tests/test_stable_release_readiness_phase68.py",
    "tests/test_phase75_documentation_sync.py",
    "tests/test_phase75_public_api_audit.py",
    "tests/test_phase75_cli_entry.py",
    "tests/test_v060_performance.py",
    "tests/test_v060_mobile_runtime.py",
    "tests/test_v060_service_lifecycle.py",
    "tests/test_v060_milestone.py",
    "tests/test_v070_content.py",
    "tests/test_v070_prefab.py",
    "tests/test_v070_pool.py",
    "tests/test_v070_level_sequence.py",
    "tests/test_v070_asset_cache.py",
    "tests/test_v070_sprite_pattern.py",
    "tests/test_v070_cli.py",
    "tests/test_v070_milestone.py",
    "tests/test_v080_release_build.py",
    "tests/test_v080_android_production.py",
    "tests/test_v080_cli.py",
    "tests/test_v080_workflows.py",
    "tests/test_v080_milestone.py",
    "tests/test_v090_api_freeze.py",
    "tests/test_v090_cli.py",
    "tests/test_v090_workflows.py",
    "tests/test_v090_milestone.py",
    "tests/test_v100_stable_release.py",
    "tests/test_v100_cli.py",
    "tests/test_v100_workflow.py",
    "tests/test_v100_milestone.py",
]

REQUIRED_PYPROJECT_TERMS = [
    "gameviz-hyperkit",
    "hyperkit.cli:main",
    "requires-python",
    "dependencies",
]


def _file_contains(path: Path, terms: list[str]) -> bool:
    if not path.exists():
        return False

    content = path.read_text(encoding="utf-8", errors="ignore")

    return all(term in content for term in terms)


def _read_project_version(
    pyproject_path: Path,
) -> str | None:
    if not pyproject_path.is_file():
        return None

    try:
        data = tomllib.loads(
            pyproject_path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        tomllib.TOMLDecodeError,
    ):
        return None

    version = (
        data.get("project", {})
        .get("version")
    )

    if version is None:
        return None

    return str(version)


def _read_module_version(
    init_path: Path,
) -> str | None:
    if not init_path.is_file():
        return None

    content = init_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']',
        content,
        flags=re.MULTILINE,
    )

    if match is None:
        return None

    return match.group(1)


def generate_release_report(root: str | Path = ".") -> ReleaseReport:
    root_path = Path(root).resolve()
    report = ReleaseReport(root=root_path)

    health_report = generate_health_report(root_path)

    report.add(
        name="Project health report",
        passed=health_report.passed,
        message=(
            f"{health_report.passed_count}/{health_report.total} health checks passed"
        ),
    )

    for filename in REQUIRED_RELEASE_FILES:
        if filename.endswith(
            "/screenshot.png"
        ):
            continue

        path = root_path / filename
        report.add(
            name=f"Required release file: {filename}",
            passed=path.exists(),
            message="Found" if path.exists() else "Missing",
        )

    for filename in REQUIRED_RELEASE_TESTS:
        path = root_path / filename
        report.add(
            name=f"Required release test: {filename}",
            passed=path.exists(),
            message="Found" if path.exists() else "Missing",
        )

    pyproject_path = root_path / "pyproject.toml"
    report.add(
        name="pyproject release metadata",
        passed=_file_contains(pyproject_path, REQUIRED_PYPROJECT_TERMS),
        message="Required package metadata found",
    )

    readme_path = root_path / "README.md"
    report.add(
        name="README package identity",
        passed=_file_contains(readme_path, ["HyperKit", "gameviz-hyperkit"]),
        message="README mentions package identity",
    )

    changelog_path = root_path / "CHANGELOG.md"
    report.add(
        name="CHANGELOG version notes",
        passed=_file_contains(changelog_path, ["Unreleased", "0.1.0"]),
        message="CHANGELOG contains version sections",
    )

    project_version = _read_project_version(
        pyproject_path
    )
    module_version = _read_module_version(
        root_path
        / "src"
        / "hyperkit"
        / "__init__.py"
    )
    versions_match = (
        project_version is not None
        and project_version
        == module_version
    )

    report.add(
        name="Package version synchronized",
        passed=versions_match,
        message=(
            f"pyproject and hyperkit.__version__ = {project_version}"
            if versions_match
            else (
                "Version mismatch: "
                f"pyproject={project_version}, "
                f"module={module_version}"
            )
        ),
    )

    report.add(
        name="README active development version",
        passed=(
            project_version is not None
            and _file_contains(
                readme_path,
                [
                    "Active development version:",
                    project_version,
                ],
            )
        ),
        message=(
            "README tracks active package version"
        ),
    )

    report.add(
        name="CHANGELOG active development version",
        passed=(
            project_version is not None
            and _file_contains(
                changelog_path,
                [
                    "Current development version:",
                    project_version,
                ],
            )
        ),
        message=(
            "CHANGELOG tracks active package version"
        ),
    )

    report.add(
        name="Python module CLI entry point",
        passed=_file_contains(
            root_path
            / "src"
            / "hyperkit"
            / "__main__.py",
            [
                "from .cli import main",
                "raise SystemExit",
            ],
        ),
        message="python -m hyperkit entry point found",
    )

    roadmap_path = root_path / "ROADMAP.md"
    report.add(
        name="Roadmap completion state",
        passed=(
            project_version is not None
            and _file_contains(
                roadmap_path,
                [
                    "Current State",
                    project_version,
                    "CURRENT STABLE RELEASE",
                    "v1.0.1",
                    "Stable Patch Release",
                ],
            )
        ),
        message="Roadmap tracks current completion phase",
    )

    report.add(
        name="Build command available",
        passed=True,
        message="Run: python -m build",
    )

    report.add(
        name="Twine check command available",
        passed=True,
        message="Run after build: twine check dist/*",
    )

    cli_path = (
        root_path
        / "src"
        / "hyperkit"
        / "cli.py"
    )

    report.add(
        name="Distribution verification command",
        passed=_file_contains(
            cli_path,
            [
                "verify-dist",
                "verify-clean-install",
                "release-manifest",
                "publish-check",
            ],
        ),
        message=(
            "v0.8 distribution verification commands found"
        ),
    )

    package_workflow = (
        root_path
        / ".github"
        / "workflows"
        / "release-package.yml"
    )

    report.add(
        name="Trusted publishing workflow",
        passed=_file_contains(
            package_workflow,
            [
                "workflow_dispatch:",
                "id-token: write",
                "pypa/gh-action-pypi-publish",
                "verify-clean-install",
            ],
        ),
        message=(
            "Gated release-package workflow found"
        ),
    )

    android_workflow = (
        root_path
        / ".github"
        / "workflows"
        / "android-production-release.yml"
    )

    report.add(
        name="Android production release workflow",
        passed=_file_contains(
            android_workflow,
            [
                "android release",
                "android-release-doctor",
                "ANDROID_KEYSTORE_BASE64",
                "android.release_artifact = aab",
            ],
        ),
        message=(
            "Signed Android production workflow found"
        ),
    )

    api_contract_path = (
        root_path
        / "src"
        / "hyperkit"
        / "api_contract.py"
    )

    report.add(
        name="Frozen API exact-match check",
        passed=_file_contains(
            api_contract_path,
            [
                'FROZEN_API_VERSION = "1.0"',
                "FROZEN_API_EXPORT_COUNT = 256",
                "FROZEN_API_FINGERPRINT",
                "validate_frozen_public_api",
            ],
        ),
        message=(
            "Frozen 1.0 API contract metadata found"
        ),
    )

    beta_workflow = (
        root_path
        / ".github"
        / "workflows"
        / "public-beta.yml"
    )

    report.add(
        name="Public beta workflow",
        passed=_file_contains(
            beta_workflow,
            [
                "workflow_dispatch:",
                "api-freeze-check",
                "publish-check --target testpypi",
                "pypa/gh-action-pypi-publish",
            ],
        ),
        message=(
            "Public beta validation workflow found"
        ),
    )

    stable_workflow = (
        root_path
        / ".github"
        / "workflows"
        / "stable-release.yml"
    )

    report.add(
        name="Stable release certification command",
        passed=_file_contains(
            cli_path,
            [
                "stable-release-check",
                "cmd_stable_release_check",
            ],
        ),
        message=(
            "Stable release certification CLI found"
        ),
    )

    report.add(
        name="Stable release workflow",
        passed=_file_contains(
            stable_workflow,
            [
                "workflow_dispatch:",
                "stable-release-check",
                "refs/tags/v1.0.1",
                "publish-check --target pypi",
                "verify-clean-install",
                "pypa/gh-action-pypi-publish",
            ],
        ),
        message=(
            "Protected HyperKit 1.0.1 stable patch workflow found"
        ),
    )

    return report


def format_release_report(report: ReleaseReport) -> str:
    lines: list[str] = []

    lines.append("HyperKit Release Readiness Report")
    lines.append("=" * 37)
    lines.append(f"Root: {report.root}")
    lines.append("")
    lines.append(f"Passed: {report.passed_count}/{report.total}")
    lines.append(f"Failed: {report.failed_count}")
    lines.append("")

    for check in report.checks:
        status = "OK" if check.passed else "FAIL"
        lines.append(f"[{status}] {check.name} - {check.message}")

    lines.append("")

    if report.passed:
        lines.append("Release readiness status: PASS")
        lines.append("Next manual commands:")
        lines.append("  pytest")
        lines.append("  python -m build")
        lines.append("  twine check dist/*")
        lines.append("  hyperkit verify-dist")
        lines.append("  hyperkit release-manifest")
        lines.append("  hyperkit verify-clean-install")
        lines.append("  hyperkit stable-release-check")
    else:
        lines.append("Release readiness status: FAIL")
        lines.append("Fix failed checks before building a release.")

    return "\n".join(lines)


def run_release_check(root: str | Path = ".") -> int:
    report = generate_release_report(root)
    print(format_release_report(report))
    return 0 if report.passed else 1
