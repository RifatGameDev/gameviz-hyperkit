from pathlib import Path

from hyperkit.ads.admob import (
    ADMOB_SAMPLE_APP_ID,
    ADMOB_SDK_DEPENDENCY,
)
from hyperkit.android import (
    create_buildozer_spec,
)
from hyperkit.cli import (
    build_parser,
    main,
)


def test_cli_parser_supports_init_admob():
    parser = build_parser()

    args = parser.parse_args(
        [
            "init-admob",
            "--path",
            ".",
        ]
    )

    assert args.command == "init-admob"
    assert args.app_id == ADMOB_SAMPLE_APP_ID


def test_cli_init_admob_configures_android_project(
    tmp_path: Path,
    capsys,
):
    create_buildozer_spec(
        tmp_path,
        title="AdMob CLI Smoke",
    )

    result = main(
        [
            "init-admob",
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
        "HyperKit AdMob Configuration"
        in output
    )
    assert (
        "Google demo/test"
        in output
    )

    spec = (
        tmp_path
        / "buildozer.spec"
    ).read_text(
        encoding="utf-8",
    )

    assert (
        ADMOB_SDK_DEPENDENCY
        in spec
    )

    assert (
        tmp_path
        / "android_src"
        / "org"
        / "gameviz"
        / "hyperkit"
        / "ads"
        / "HyperKitAdMob.java"
    ).is_file()
