from pathlib import Path

from hyperkit.analytics.firebase import (
    FIREBASE_ANALYTICS_DEPENDENCY,
)
from hyperkit.android import (
    create_buildozer_spec,
)
from hyperkit.cli import (
    build_parser,
    main,
)


def test_cli_parser_supports_init_firebase_analytics():
    parser = build_parser()

    args = parser.parse_args(
        [
            "init-firebase-analytics",
            "--path",
            ".",
        ]
    )

    assert (
        args.command
        == "init-firebase-analytics"
    )


def test_cli_init_firebase_analytics_configures_project(
    tmp_path: Path,
    capsys,
):
    create_buildozer_spec(
        tmp_path,
        title="Firebase CLI Smoke",
    )

    result = main(
        [
            "init-firebase-analytics",
            "--path",
            str(tmp_path),
        ]
    )

    output = (
        capsys
        .readouterr()
        .out
    )

    assert result == 0

    assert (
        "HyperKit Firebase Analytics Configuration"
        in output
    )

    spec = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8",
    )

    assert (
        FIREBASE_ANALYTICS_DEPENDENCY
        in spec
    )

    assert (
        tmp_path
        / "android_src"
        / "org"
        / "gameviz"
        / "hyperkit"
        / "analytics"
        / "HyperKitFirebaseAnalytics.java"
    ).is_file()


def test_cli_init_firebase_analytics_accepts_google_services(
    tmp_path: Path,
):
    create_buildozer_spec(
        tmp_path,
        title="Firebase CLI Resources",
    )

    config = (
        tmp_path
        / "google-services.json"
    )

    config.write_text(
        """{
  "project_info": {
    "project_id": "hyperkit-cli-project"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:456:android:def",
        "android_client_info": {
          "package_name": "org.gameviz.cli"
        }
      },
      "api_key": [
        {
          "current_key": "cli-api-key"
        }
      ]
    }
  ]
}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "init-firebase-analytics",
            "--path",
            str(tmp_path),
            "--google-services",
            str(config),
            "--package-name",
            "org.gameviz.cli",
        ]
    )

    assert result == 0

    spec = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8",
    )

    assert (
        "android.add_resources = android_resources"
        in spec
    )

    assert (
        tmp_path
        / "android_resources"
        / "values"
        / "firebase_analytics.xml"
    ).is_file()
