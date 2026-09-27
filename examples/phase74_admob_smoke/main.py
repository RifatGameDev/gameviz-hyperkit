from __future__ import annotations

from kivy.clock import Clock

from hyperkit import (
    AdMobAndroidProvider,
    Game,
    GameObject,
    Scene,
    TextLabel,
)


class AdMobSmokeScene(Scene):
    def start(self):
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
                text="HyperKit AdMob Smoke",
                font_size=38,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1060,
                text=(
                    "Left side: Interstitial\n"
                    "Right side: Rewarded\n"
                    "Banner loads at the bottom"
                ),
                font_size=24,
                color=(0.82, 0.88, 1, 1),
            )
        )

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=820,
                text="Initializing AdMob...",
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
                x=90,
                y=470,
                text="INTERSTITIAL",
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
                color=(0.20, 0.65, 0.42, 1),
                shape="rect",
            )
        )

        self.right_label = self.add(
            TextLabel(
                x=450,
                y=470,
                text="REWARDED",
                font_size=24,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.ads = AdMobAndroidProvider()

        result = self.ads.initialize()

        if result.success:
            self.status_label.set_text(
                "AdMob initialized with Google test ads."
            )

            Clock.schedule_once(
                self._show_banner,
                1.0,
            )

        else:
            self.status_label.set_text(
                "AdMob init failed: "
                + result.message
            )

        self.start_game()

    def _show_banner(self, _dt):
        result = self.ads.show_banner(
            "banner"
        )

        if not result.success:
            self.status_label.set_text(
                "Banner request failed: "
                + result.message
            )

    def _reward_player(self):
        self.status_label.set_text(
            "Reward earned successfully!"
        )

    def on_tap(self, x, y):
        if x < 360:
            result = (
                self.ads
                .show_interstitial(
                    "game_over"
                )
            )

            self.status_label.set_text(
                "Interstitial requested."
                if result.success
                else (
                    "Interstitial failed: "
                    + result.message
                )
            )

            return

        result = self.ads.show_rewarded(
            "revive",
            on_reward=(
                self._reward_player
            ),
        )

        self.status_label.set_text(
            "Rewarded ad requested."
            if result.success
            else (
                "Rewarded ad failed: "
                + result.message
            )
        )


if __name__ == "__main__":
    Game(
        title="HyperKit AdMob Smoke",
        width=720,
        height=1280,
    ).set_scene(
        AdMobSmokeScene()
    ).run()
