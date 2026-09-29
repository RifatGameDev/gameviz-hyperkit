from pathlib import Path

from hyperkit.cli import main


def create_content_project(
    root: Path,
    *,
    missing: bool = False,
) -> None:
    (
        root
        / "assets"
        / "images"
    ).mkdir(
        parents=True
    )
    (
        root
        / "assets"
        / "data"
    ).mkdir()

    if not missing:
        (
            root
            / "assets"
            / "images"
            / "hero.png"
        ).write_bytes(
            b"fake"
        )

    (
        root
        / "assets"
        / "data"
        / "content.json"
    ).write_text(
        """
{
  "name": "CLI Content",
  "items": [
    {
      "id": "hero",
      "kind": "image",
      "asset": "hero.png"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )


def test_validate_content_cli_passes(
    tmp_path: Path,
    capsys,
):
    create_content_project(
        tmp_path
    )

    result = main(
        [
            "validate-content",
            "--path",
            str(
                tmp_path
            ),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 0
    assert "Items: 1" in output
    assert (
        "Content validation status: PASS"
        in output
    )


def test_validate_content_cli_fails_for_missing_asset(
    tmp_path: Path,
    capsys,
):
    create_content_project(
        tmp_path,
        missing=True,
    )

    result = main(
        [
            "validate-content",
            "--path",
            str(
                tmp_path
            ),
        ]
    )

    output = (
        capsys.readouterr()
        .out
    )

    assert result == 1
    assert "Failed assets: 1" in output
    assert (
        "Content validation status: FAIL"
        in output
    )
