"""Google AdMob Android provider for GameViz HyperKit.

The module is imported safely on desktop. Android-specific classes are
resolved lazily only when the bridge is initialized on an Android build.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from . import (
    AdConfig,
    AdResult,
    AdStatus,
    AdType,
)
from .android import (
    AndroidAdBridge,
    AndroidAdBuildRequirements,
    AndroidAdProvider,
)


ADMOB_SDK_DEPENDENCY = (
    "com.google.android.gms:"
    "play-services-ads:25.5.0"
)

ADMOB_APPLICATION_ID_META_DATA = (
    "com.google.android.gms.ads."
    "APPLICATION_ID"
)

ADMOB_SAMPLE_APP_ID = (
    "ca-app-pub-3940256099942544"
    "~3347511713"
)

ADMOB_TEST_BANNER_ID = (
    "ca-app-pub-3940256099942544"
    "/6300978111"
)

ADMOB_TEST_INTERSTITIAL_ID = (
    "ca-app-pub-3940256099942544"
    "/1033173712"
)

ADMOB_TEST_REWARDED_ID = (
    "ca-app-pub-3940256099942544"
    "/5224354917"
)

ADMOB_TEST_PLACEMENTS = {
    "banner": ADMOB_TEST_BANNER_ID,
    "interstitial": (
        ADMOB_TEST_INTERSTITIAL_ID
    ),
    "rewarded": ADMOB_TEST_REWARDED_ID,
    "game_over": (
        ADMOB_TEST_INTERSTITIAL_ID
    ),
    "revive": ADMOB_TEST_REWARDED_ID,
    "double_coins": (
        ADMOB_TEST_REWARDED_ID
    ),
}


def create_admob_config(
    *,
    app_id: str = ADMOB_SAMPLE_APP_ID,
    test_mode: bool = True,
    placements: dict[
        str,
        str,
    ] | None = None,
) -> AdConfig:
    """Create an AdMob-ready provider-neutral AdConfig."""

    resolved = (
        dict(ADMOB_TEST_PLACEMENTS)
        if test_mode
        else {}
    )

    if placements:
        resolved.update(
            placements
        )

    return AdConfig(
        enabled=True,
        test_mode=bool(test_mode),
        placements=resolved,
        provider_options={
            "app_id": str(app_id),
            "provider": "admob",
        },
    )


class AdMobAndroidBridge(
    AndroidAdBridge
):
    """Runtime bridge backed by Google Mobile Ads on Android."""

    bridge_name = "admob"

    def __init__(
        self,
        *,
        app_id: str = (
            ADMOB_SAMPLE_APP_ID
        ),
        java_class: str = (
            "org.gameviz.hyperkit.ads."
            "HyperKitAdMob"
        ),
        clock_interval: float = 0.1,
    ) -> None:
        self.app_id = str(
            app_id
        ).strip()

        if not self.app_id:
            raise ValueError(
                "AdMob app_id cannot be empty."
            )

        self.java_class = (
            java_class
        )

        self.clock_interval = float(
            clock_interval
        )

        if self.clock_interval <= 0:
            raise ValueError(
                "clock_interval must be "
                "greater than zero."
            )

        self.initialized = False
        self._helper = None
        self._activity = None

    @property
    def build_requirements(
        self,
    ) -> AndroidAdBuildRequirements:
        return AndroidAdBuildRequirements(
            permissions=(
                "INTERNET",
                "ACCESS_NETWORK_STATE",
            ),
            python_requirements=(
                "pyjnius",
            ),
            gradle_dependencies=(
                ADMOB_SDK_DEPENDENCY,
            ),
            meta_data={
                ADMOB_APPLICATION_ID_META_DATA: (
                    self.app_id
                ),
            },
            java_source_dirs=(
                "android_src",
            ),
            enable_androidx=True,
        )

    def _load_android_runtime(
        self,
    ) -> None:
        if (
            self._helper is not None
            and self._activity is not None
        ):
            return

        try:
            from jnius import autoclass
        except Exception as exc:
            raise RuntimeError(
                "AdMob Android runtime requires "
                "PyJNIus inside an Android build."
            ) from exc

        try:
            activity_class = autoclass(
                "org.kivy.android."
                "PythonActivity"
            )

            helper = autoclass(
                self.java_class
            )

        except Exception as exc:
            raise RuntimeError(
                "AdMob Android bridge classes "
                "are not available. Configure "
                "the Android project before "
                "building the APK."
            ) from exc

        self._activity = (
            activity_class.mActivity
        )

        self._helper = helper

    def initialize(
        self,
        config: AdConfig,
    ) -> AdResult:
        if not config.enabled:
            return AdResult(
                success=True,
                status=AdStatus.UNAVAILABLE,
                message="AdMob is disabled.",
            )

        try:
            self._load_android_runtime()

            self._helper.initialize(
                self._activity
            )

        except Exception as exc:
            self.initialized = False

            return AdResult(
                success=False,
                status=AdStatus.FAILED,
                message=str(exc),
            )

        self.initialized = True

        return AdResult(
            success=True,
            status=AdStatus.READY,
            message=(
                "AdMob Android bridge "
                "initialized."
            ),
        )

    def is_available(
        self,
        ad_type: AdType,
        placement_id: str | None,
    ) -> bool:
        return (
            self.initialized
            and bool(
                placement_id
            )
        )

    def _failed(
        self,
        ad_type: AdType,
        placement_id: str | None,
        message: str,
    ) -> AdResult:
        return AdResult(
            success=False,
            status=AdStatus.FAILED,
            ad_type=ad_type,
            placement=placement_id,
            message=message,
        )

    def show_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        if not self.is_available(
            AdType.BANNER,
            placement_id,
        ):
            return self._failed(
                AdType.BANNER,
                placement_id,
                "AdMob banner placement "
                "is unavailable.",
            )

        try:
            accepted = bool(
                self._helper.showBanner(
                    self._activity,
                    placement_id,
                )
            )

        except Exception as exc:
            return self._failed(
                AdType.BANNER,
                placement_id,
                str(exc),
            )

        return AdResult(
            success=accepted,
            status=(
                AdStatus.SHOWING
                if accepted
                else AdStatus.FAILED
            ),
            ad_type=AdType.BANNER,
            placement=placement_id,
        )

    def hide_banner(
        self,
        placement_id: str | None,
    ) -> AdResult:
        if not self.initialized:
            return self._failed(
                AdType.BANNER,
                placement_id,
                "AdMob is not initialized.",
            )

        try:
            self._helper.hideBanner(
                self._activity
            )

        except Exception as exc:
            return self._failed(
                AdType.BANNER,
                placement_id,
                str(exc),
            )

        return AdResult(
            success=True,
            status=AdStatus.COMPLETED,
            ad_type=AdType.BANNER,
            placement=placement_id,
        )

    def show_interstitial(
        self,
        placement_id: str | None,
    ) -> AdResult:
        if not self.is_available(
            AdType.INTERSTITIAL,
            placement_id,
        ):
            return self._failed(
                AdType.INTERSTITIAL,
                placement_id,
                "AdMob interstitial "
                "placement is unavailable.",
            )

        try:
            accepted = bool(
                self._helper.showInterstitial(
                    self._activity,
                    placement_id,
                )
            )

        except Exception as exc:
            return self._failed(
                AdType.INTERSTITIAL,
                placement_id,
                str(exc),
            )

        return AdResult(
            success=accepted,
            status=(
                AdStatus.SHOWING
                if accepted
                else AdStatus.FAILED
            ),
            ad_type=AdType.INTERSTITIAL,
            placement=placement_id,
        )

    def show_rewarded(
        self,
        placement_id: str | None,
        *,
        on_reward: (
            Callable[[], None]
            | None
        ) = None,
    ) -> AdResult:
        if not self.is_available(
            AdType.REWARDED,
            placement_id,
        ):
            return self._failed(
                AdType.REWARDED,
                placement_id,
                "AdMob rewarded placement "
                "is unavailable.",
            )

        try:
            self._helper.resetRewardState()

            accepted = bool(
                self._helper.showRewarded(
                    self._activity,
                    placement_id,
                )
            )

        except Exception as exc:
            return self._failed(
                AdType.REWARDED,
                placement_id,
                str(exc),
            )

        if (
            accepted
            and on_reward is not None
        ):
            self._schedule_reward_poll(
                on_reward
            )

        return AdResult(
            success=accepted,
            status=(
                AdStatus.SHOWING
                if accepted
                else AdStatus.FAILED
            ),
            ad_type=AdType.REWARDED,
            placement=placement_id,
            reward_granted=False,
        )

    def _schedule_reward_poll(
        self,
        on_reward: Callable[
            [],
            None,
        ],
    ) -> None:
        try:
            from kivy.clock import Clock
        except Exception:
            return

        called = {
            "rewarded": False,
        }

        def poll_reward(
            _dt,
        ):
            try:
                if bool(
                    self._helper
                    .consumeRewardEarned()
                ):
                    if not called[
                        "rewarded"
                    ]:
                        called[
                            "rewarded"
                        ] = True
                        on_reward()

                closed = bool(
                    self._helper
                    .consumeRewardedClosed()
                )

            except Exception:
                return False

            if closed:
                return False

            return True

        Clock.schedule_interval(
            poll_reward,
            self.clock_interval,
        )


class AdMobAndroidProvider(
    AndroidAdProvider
):
    """Convenience AndroidAdProvider configured for Google AdMob."""

    provider_name = "admob"

    def __init__(
        self,
        *,
        app_id: str = (
            ADMOB_SAMPLE_APP_ID
        ),
        test_mode: bool = True,
        placements: dict[
            str,
            str,
        ] | None = None,
        require_mapped_placements: bool = True,
    ) -> None:
        config = create_admob_config(
            app_id=app_id,
            test_mode=test_mode,
            placements=placements,
        )

        super().__init__(
            AdMobAndroidBridge(
                app_id=app_id
            ),
            config,
            require_mapped_placements=(
                require_mapped_placements
            ),
        )


def _merge_csv_setting(
    text: str,
    key: str,
    values: tuple[
        str,
        ...,
    ],
) -> str:
    if not values:
        return text

    lines = text.splitlines()
    prefix = f"{key} ="

    for index, line in enumerate(
        lines
    ):
        if line.strip().startswith(
            prefix
        ):
            existing = [
                item.strip()
                for item in (
                    line.split(
                        "=",
                        1,
                    )[1]
                    .split(",")
                )
                if item.strip()
            ]

            merged = list(
                existing
            )

            for value in values:
                if value not in merged:
                    merged.append(
                        value
                    )

            lines[index] = (
                f"{key} = "
                + ",".join(
                    merged
                )
            )

            return "\n".join(
                lines
            ) + "\n"

    buildozer_index = next(
        (
            index
            for index, line
            in enumerate(lines)
            if line.strip()
            == "[buildozer]"
        ),
        len(lines),
    )

    lines.insert(
        buildozer_index,
        (
            f"{key} = "
            + ",".join(values)
        ),
    )

    return "\n".join(
        lines
    ) + "\n"


def _upsert_scalar_setting(
    text: str,
    key: str,
    value: str,
) -> str:
    lines = text.splitlines()
    prefix = f"{key} ="

    for index, line in enumerate(
        lines
    ):
        if line.strip().startswith(
            prefix
        ):
            lines[index] = (
                f"{key} = {value}"
            )

            return "\n".join(
                lines
            ) + "\n"

    buildozer_index = next(
        (
            index
            for index, line
            in enumerate(lines)
            if line.strip()
            == "[buildozer]"
        ),
        len(lines),
    )

    lines.insert(
        buildozer_index,
        f"{key} = {value}",
    )

    return "\n".join(
        lines
    ) + "\n"


ADMOB_JAVA_SOURCE = r"""package org.gameviz.hyperkit.ads;

import android.app.Activity;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.FrameLayout;

import com.google.android.gms.ads.AdError;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdSize;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.FullScreenContentCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.interstitial.InterstitialAd;
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.rewarded.RewardedAd;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;

public final class HyperKitAdMob {
    private static AdView bannerView = null;
    private static volatile boolean rewardEarned = false;
    private static volatile boolean rewardedClosed = false;

    private HyperKitAdMob() {}

    public static void initialize(final Activity activity) {
        activity.runOnUiThread(() ->
            MobileAds.initialize(activity)
        );
    }

    public static boolean showBanner(
        final Activity activity,
        final String adUnitId
    ) {
        if (adUnitId == null || adUnitId.trim().isEmpty()) {
            return false;
        }

        activity.runOnUiThread(() -> {
            hideBannerInternal();

            bannerView = new AdView(activity);
            bannerView.setAdSize(AdSize.BANNER);
            bannerView.setAdUnitId(adUnitId);

            FrameLayout.LayoutParams params =
                new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                );

            params.gravity =
                Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;

            activity.addContentView(
                bannerView,
                params
            );

            bannerView.loadAd(
                new AdRequest.Builder().build()
            );
        });

        return true;
    }

    public static void hideBanner(
        final Activity activity
    ) {
        activity.runOnUiThread(
            HyperKitAdMob::hideBannerInternal
        );
    }

    private static void hideBannerInternal() {
        if (bannerView == null) {
            return;
        }

        if (bannerView.getParent() instanceof ViewGroup) {
            ((ViewGroup) bannerView.getParent())
                .removeView(bannerView);
        }

        bannerView.destroy();
        bannerView = null;
    }

    public static boolean showInterstitial(
        final Activity activity,
        final String adUnitId
    ) {
        if (adUnitId == null || adUnitId.trim().isEmpty()) {
            return false;
        }

        activity.runOnUiThread(() -> {
            AdRequest request =
                new AdRequest.Builder().build();

            InterstitialAd.load(
                activity,
                adUnitId,
                request,
                new InterstitialAdLoadCallback() {
                    @Override
                    public void onAdLoaded(
                        InterstitialAd ad
                    ) {
                        ad.setFullScreenContentCallback(
                            new FullScreenContentCallback() {
                                @Override
                                public void onAdDismissedFullScreenContent() {
                                }

                                @Override
                                public void onAdFailedToShowFullScreenContent(
                                    AdError adError
                                ) {
                                }
                            }
                        );

                        ad.show(activity);
                    }

                    @Override
                    public void onAdFailedToLoad(
                        LoadAdError error
                    ) {
                    }
                }
            );
        });

        return true;
    }

    public static void resetRewardState() {
        rewardEarned = false;
        rewardedClosed = false;
    }

    public static boolean showRewarded(
        final Activity activity,
        final String adUnitId
    ) {
        if (adUnitId == null || adUnitId.trim().isEmpty()) {
            return false;
        }

        resetRewardState();

        activity.runOnUiThread(() -> {
            AdRequest request =
                new AdRequest.Builder().build();

            RewardedAd.load(
                activity,
                adUnitId,
                request,
                new RewardedAdLoadCallback() {
                    @Override
                    public void onAdLoaded(
                        RewardedAd ad
                    ) {
                        ad.setFullScreenContentCallback(
                            new FullScreenContentCallback() {
                                @Override
                                public void onAdDismissedFullScreenContent() {
                                    rewardedClosed = true;
                                }

                                @Override
                                public void onAdFailedToShowFullScreenContent(
                                    AdError adError
                                ) {
                                    rewardedClosed = true;
                                }
                            }
                        );

                        ad.show(
                            activity,
                            rewardItem -> {
                                rewardEarned = true;
                            }
                        );
                    }

                    @Override
                    public void onAdFailedToLoad(
                        LoadAdError error
                    ) {
                        rewardedClosed = true;
                    }
                }
            );
        });

        return true;
    }

    public static boolean consumeRewardEarned() {
        boolean value = rewardEarned;
        rewardEarned = false;
        return value;
    }

    public static boolean consumeRewardedClosed() {
        boolean value = rewardedClosed;
        rewardedClosed = false;
        return value;
    }
}
"""


def configure_admob_android_project(
    path: str | Path = ".",
    *,
    app_id: str = ADMOB_SAMPLE_APP_ID,
) -> tuple[
    Path,
    Path,
]:
    """Add AdMob native build settings to an existing Android project."""

    root = Path(
        path
    ).resolve()

    spec_path = (
        root
        / "buildozer.spec"
    )

    if not spec_path.is_file():
        raise FileNotFoundError(
            "buildozer.spec was not found. "
            "Run 'hyperkit init-android' first."
        )

    bridge = AdMobAndroidBridge(
        app_id=app_id
    )

    requirements = (
        bridge.build_requirements
    )

    text = spec_path.read_text(
        encoding="utf-8",
    )

    text = _merge_csv_setting(
        text,
        "requirements",
        requirements.python_requirements,
    )

    text = _merge_csv_setting(
        text,
        "android.permissions",
        requirements.permissions,
    )

    text = _merge_csv_setting(
        text,
        "android.gradle_dependencies",
        requirements.gradle_dependencies,
    )

    meta_data = tuple(
        f"{key}={value}"
        for key, value
        in requirements.meta_data.items()
    )

    text = _merge_csv_setting(
        text,
        "android.meta_data",
        meta_data,
    )

    text = _merge_csv_setting(
        text,
        "android.add_src",
        requirements.java_source_dirs,
    )

    if requirements.enable_androidx:
        text = _upsert_scalar_setting(
            text,
            "android.enable_androidx",
            "True",
        )

    spec_path.write_text(
        text,
        encoding="utf-8",
    )

    java_path = (
        root
        / "android_src"
        / "org"
        / "gameviz"
        / "hyperkit"
        / "ads"
        / "HyperKitAdMob.java"
    )

    java_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    java_path.write_text(
        ADMOB_JAVA_SOURCE,
        encoding="utf-8",
    )

    return (
        spec_path,
        java_path,
    )


__all__ = [
    "ADMOB_APPLICATION_ID_META_DATA",
    "ADMOB_JAVA_SOURCE",
    "ADMOB_SAMPLE_APP_ID",
    "ADMOB_SDK_DEPENDENCY",
    "ADMOB_TEST_BANNER_ID",
    "ADMOB_TEST_INTERSTITIAL_ID",
    "ADMOB_TEST_PLACEMENTS",
    "ADMOB_TEST_REWARDED_ID",
    "AdMobAndroidBridge",
    "AdMobAndroidProvider",
    "configure_admob_android_project",
    "create_admob_config",
]
