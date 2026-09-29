from hyperkit import generate_release_report


def _checks():
    report = generate_release_report(".")
    return {
        check.name: check
        for check in report.checks
    }


def test_release_report_verifies_version_synchronization():
    checks = _checks()

    assert (
        checks[
            "Package version synchronized"
        ].passed
    )


def test_release_report_verifies_readme_development_version():
    checks = _checks()

    assert (
        checks[
            "README active development version"
        ].passed
    )


def test_release_report_verifies_changelog_development_version():
    checks = _checks()

    assert (
        checks[
            "CHANGELOG active development version"
        ].passed
    )


def test_release_report_verifies_python_module_entry():
    checks = _checks()

    assert (
        checks[
            "Python module CLI entry point"
        ].passed
    )


def test_release_report_verifies_current_roadmap_state():
    checks = _checks()

    assert (
        checks[
            "Roadmap completion state"
        ].passed
    )
