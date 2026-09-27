from __future__ import annotations

from pathlib import Path

from hyperkit import (
    AnalyticsService,
    FirebaseAnalyticsAndroidProvider,
    Game,
    GameObject,
    Scene,
    TextLabel,
)


PACKAGE_NAME = (
    "org.gameviz.phase74analyticssmoke"
)


class FirebaseAnalyticsSmokeScene(
    Scene
):
    def start(
        self,
    ):
        self.tap_count = 0

        self.background = self.add(
            GameObject(
                x=0,
                y=0,
                width=720,
                height=1280,
                color=(0.06, 0.08, 0.12, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1160,
                text=(
                    "HyperKit Firebase "
                    "Analytics"
                ),
                font_size=38,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1050,
                text=(
                    "Left: custom event\n"
                    "Right: level complete\n"
                    "Check Firebase DebugView"
                ),
                font_size=24,
                color=(0.82, 0.88, 1, 1),
            )
        )

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=820,
                text=(
                    "Initializing Firebase "
                    "Analytics..."
                ),
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self.left_zone = self.add(
            GameObject(
                x=40,
                y=360,
                width=300,
                height=260,
                color=(0.18, 0.42, 0.76, 1),
                shape="rect",
            )
        )

        self.left_label = self.add(
            TextLabel(
                x=88,
                y=470,
                text="CUSTOM EVENT",
                font_size=24,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.right_zone = self.add(
            GameObject(
                x=380,
                y=360,
                width=300,
                height=260,
                color=(0.65, 0.38, 0.18, 1),
                shape="rect",
            )
        )

        self.right_label = self.add(
            TextLabel(
                x=422,
                y=470,
                text="LEVEL COMPLETE",
                font_size=22,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        config_path = (
            Path(__file__).resolve().parent
            / "google-services.json"
        )

        try:
            provider = (
                FirebaseAnalyticsAndroidProvider
                .from_google_services_json(
                    config_path,
                    package_name=PACKAGE_NAME,
                )
            )

            self.analytics = (
                AnalyticsService(
                    provider
                )
            )

            result = (
                self.analytics
                .initialize()
            )

        except Exception as exc:
            self.analytics = None
            self.status_label.set_text(
                "Firebase setup failed: "
                + str(exc)
            )

            self.start_game()
            return

        if result.success:
            startup_result = (
                self.analytics
                .game_start(
                    mode="firebase_smoke",
                    phase=74,
                )
            )

            if startup_result.success:
                self.status_label.set_text(
                    "Firebase initialized. "
                    "game_start sent."
                )

            else:
                self.status_label.set_text(
                    "Firebase initialized, "
                    "but event failed: "
                    + startup_result.message
                )

        else:
            self.status_label.set_text(
                "Firebase init failed: "
                + result.message
            )

        self.start_game()

    def on_tap(
        self,
        x,
        y,
    ):
        if self.analytics is None:
            self.status_label.set_text(
                "Analytics is unavailable."
            )
            return

        self.tap_count += 1

        if x < 360:
            result = (
                self.analytics
                .track(
                    "hyperkit_smoke_tap",
                    side="left",
                    tap_count=(
                        self.tap_count
                    ),
                )
            )

            self.status_label.set_text(
                (
                    "Custom event sent. "
                    f"Tap #{self.tap_count}"
                )
                if result.success
                else (
                    "Custom event failed: "
                    + result.message
                )
            )

            return

        result = (
            self.analytics
            .level_complete(
                1,
                score=100,
                duration=12.5,
                source="firebase_smoke",
            )
        )

        self.status_label.set_text(
            "level_complete sent."
            if result.success
            else (
                "Level event failed: "
                + result.message
            )
        )


if __name__ == "__main__":
    Game(
        title=(
            "HyperKit Phase 74 "
            "Firebase Analytics"
        ),
        width=720,
        height=1280,
    ).set_scene(
        FirebaseAnalyticsSmokeScene()
    ).run()
