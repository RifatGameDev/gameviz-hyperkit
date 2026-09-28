"""Firebase Analytics Android provider for GameViz HyperKit.

The provider is desktop-safe: Android classes are resolved lazily at
runtime. HyperKit configures Firebase programmatically through
FirebaseOptions, so the Buildozer integration does not depend on the
Google Services Gradle plugin.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape

from . import (
    AnalyticsEvent,
    AnalyticsProvider,
    AnalyticsResult,
)
from .android import (
    AndroidAnalyticsBridge,
    AndroidAnalyticsBuildRequirements,
    AndroidAnalyticsProvider,
)


FIREBASE_ANALYTICS_DEPENDENCY = (
    "com.google.firebase:"
    "firebase-analytics:23.2.0"
)


@dataclass(frozen=True)
class FirebaseAnalyticsConfig:
    """Firebase Android application settings required by the bridge."""

    application_id: str
    api_key: str
    project_id: str

    def __post_init__(
        self,
    ) -> None:
        for field_name in (
            "application_id",
            "api_key",
            "project_id",
        ):
            value = str(
                getattr(
                    self,
                    field_name,
                )
            ).strip()

            if not value:
                raise ValueError(
                    f"{field_name} cannot be empty."
                )

            object.__setattr__(
                self,
                field_name,
                value,
            )


def _json_safe_value(
    value: Any,
) -> Any:
    if value is None:
        return None

    if isinstance(
        value,
        (
            bool,
            int,
            float,
            str,
        ),
    ):
        return value

    return str(
        value
    )


def _serialize_event_properties(
    properties,
) -> str:
    payload = {
        str(key): _json_safe_value(
            value
        )
        for key, value
        in properties.items()
    }

    return json.dumps(
        payload,
        separators=(
            ",",
            ":",
        ),
        sort_keys=True,
    )


def load_firebase_analytics_config(
    path: str | Path,
    *,
    package_name: str | None = None,
) -> FirebaseAnalyticsConfig:
    """Load Firebase Android settings from google-services.json."""

    config_path = Path(
        path
    ).expanduser().resolve()

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Firebase config file not found: {config_path}"
        )

    try:
        data = json.loads(
            config_path.read_text(
                encoding="utf-8",
            )
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            "Invalid google-services.json."
        ) from exc

    project_info = data.get(
        "project_info",
        {},
    )

    project_id = str(
        project_info.get(
            "project_id",
            "",
        )
    ).strip()

    clients = data.get(
        "client",
        [],
    )

    if not isinstance(
        clients,
        list,
    ) or not clients:
        raise ValueError(
            "google-services.json does not "
            "contain any Android clients."
        )

    selected = None

    if package_name is not None:
        expected = str(
            package_name
        ).strip()

        for client in clients:
            actual = str(
                client.get(
                    "client_info",
                    {},
                )
                .get(
                    "android_client_info",
                    {},
                )
                .get(
                    "package_name",
                    "",
                )
            ).strip()

            if actual == expected:
                selected = client
                break

        if selected is None:
            raise ValueError(
                "google-services.json does not "
                f"contain package '{expected}'."
            )

    elif len(
        clients
    ) == 1:
        selected = clients[0]

    else:
        raise ValueError(
            "google-services.json contains "
            "multiple clients. Pass package_name."
        )

    client_info = selected.get(
        "client_info",
        {},
    )

    application_id = str(
        client_info.get(
            "mobilesdk_app_id",
            "",
        )
    ).strip()

    api_keys = selected.get(
        "api_key",
        [],
    )

    api_key = ""

    if (
        isinstance(
            api_keys,
            list,
        )
        and api_keys
    ):
        api_key = str(
            api_keys[0].get(
                "current_key",
                "",
            )
        ).strip()

    return FirebaseAnalyticsConfig(
        application_id=(
            application_id
        ),
        api_key=api_key,
        project_id=project_id,
    )


class FirebaseAnalyticsAndroidBridge(
    AndroidAnalyticsBridge
):
    """Runtime bridge backed by Firebase Analytics on Android."""

    bridge_name = "firebase-analytics"

    def __init__(
        self,
        config: FirebaseAnalyticsConfig,
        *,
        java_class: str = (
            "org.gameviz.hyperkit.analytics."
            "HyperKitFirebaseAnalytics"
        ),
    ) -> None:
        if not isinstance(
            config,
            FirebaseAnalyticsConfig,
        ):
            raise TypeError(
                "config must be a "
                "FirebaseAnalyticsConfig instance."
            )

        self.config = config
        self.java_class = java_class
        self.initialized = False
        self._helper = None
        self._activity = None

    @property
    def build_requirements(
        self,
    ) -> AndroidAnalyticsBuildRequirements:
        return AndroidAnalyticsBuildRequirements(
            permissions=(
                "INTERNET",
                "ACCESS_NETWORK_STATE",
            ),
            python_requirements=(
                "pyjnius",
            ),
            gradle_dependencies=(
                FIREBASE_ANALYTICS_DEPENDENCY,
            ),
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
                "Firebase Analytics Android "
                "runtime requires PyJNIus "
                "inside an Android build."
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
                "Firebase Analytics Android "
                "bridge classes are not "
                "available. Configure the "
                "Android project before "
                "building the APK."
            ) from exc

        self._activity = (
            activity_class.mActivity
        )

        self._helper = helper

    def initialize(
        self,
    ) -> AnalyticsResult:
        try:
            self._load_android_runtime()

            initialized = bool(
                self._helper.initialize(
                    self._activity,
                    self.config.application_id,
                    self.config.api_key,
                    self.config.project_id,
                )
            )

        except Exception as exc:
            self.initialized = False

            return AnalyticsResult(
                success=False,
                message=str(
                    exc
                ),
            )

        self.initialized = initialized

        return AnalyticsResult(
            success=initialized,
            message=(
                "Firebase Analytics Android "
                "bridge initialized."
                if initialized
                else (
                    "Firebase Analytics Android "
                    "bridge failed to initialize."
                )
            ),
        )

    def track_event(
        self,
        event: AnalyticsEvent,
    ) -> AnalyticsResult:
        if not self.initialized:
            return AnalyticsResult(
                success=False,
                message=(
                    "Firebase Analytics is "
                    "not initialized."
                ),
            )

        try:
            accepted = bool(
                self._helper.logEvent(
                    self._activity,
                    event.name,
                    _serialize_event_properties(
                        event.properties
                    ),
                )
            )

        except Exception as exc:
            return AnalyticsResult(
                success=False,
                message=str(
                    exc
                ),
            )

        return AnalyticsResult(
            success=accepted,
            message=(
                ""
                if accepted
                else (
                    "Firebase Analytics "
                    "rejected the event."
                )
            ),
        )

    def flush(
        self,
    ) -> AnalyticsResult:
        # Firebase Analytics sends events asynchronously and does not expose
        # an application flush API. Treat flush as a successful no-op.
        return AnalyticsResult(
            success=(
                self.initialized
            ),
            message=(
                ""
                if self.initialized
                else (
                    "Firebase Analytics is "
                    "not initialized."
                )
            ),
        )


class FirebaseAnalyticsAndroidProvider(
    AndroidAnalyticsProvider
):
    """Convenience provider configured for Firebase Analytics."""

    provider_name = "firebase-analytics"

    @classmethod
    def from_google_services_json(
        cls,
        path: str | Path,
        *,
        package_name: str | None = None,
    ) -> "FirebaseAnalyticsAndroidProvider":
        config = load_firebase_analytics_config(
            path,
            package_name=package_name,
        )

        return cls(
            application_id=(
                config.application_id
            ),
            api_key=config.api_key,
            project_id=config.project_id,
        )

    def __init__(
        self,
        *,
        application_id: str,
        api_key: str,
        project_id: str,
    ) -> None:
        config = FirebaseAnalyticsConfig(
            application_id=(
                application_id
            ),
            api_key=api_key,
            project_id=project_id,
        )

        super().__init__(
            FirebaseAnalyticsAndroidBridge(
                config
            )
        )

        self.config = config


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


FIREBASE_ANALYTICS_JAVA_SOURCE = r"""package org.gameviz.hyperkit.analytics;

import android.app.Activity;
import android.os.Bundle;

import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.analytics.FirebaseAnalytics;

import org.json.JSONObject;

import java.util.Iterator;

public final class HyperKitFirebaseAnalytics {
    private static FirebaseAnalytics analytics = null;

    private HyperKitFirebaseAnalytics() {}

    public static boolean initialize(
        final Activity activity,
        final String applicationId,
        final String apiKey,
        final String projectId
    ) {
        if (
            applicationId == null ||
            applicationId.trim().isEmpty() ||
            apiKey == null ||
            apiKey.trim().isEmpty() ||
            projectId == null ||
            projectId.trim().isEmpty()
        ) {
            return false;
        }

        try {
            FirebaseApp app;

            try {
                app = FirebaseApp.getInstance();
            } catch (IllegalStateException error) {
                FirebaseOptions options =
                    new FirebaseOptions.Builder()
                        .setApplicationId(applicationId)
                        .setApiKey(apiKey)
                        .setProjectId(projectId)
                        .build();

                app = FirebaseApp.initializeApp(
                    activity,
                    options
                );
            }

            if (app == null) {
                return false;
            }

            analytics = FirebaseAnalytics.getInstance(
                activity
            );

            return analytics != null;

        } catch (Exception error) {
            analytics = null;
            return false;
        }
    }

    public static boolean logEvent(
        final Activity activity,
        final String name,
        final String jsonProperties
    ) {
        if (
            analytics == null ||
            name == null ||
            name.trim().isEmpty()
        ) {
            return false;
        }

        try {
            Bundle bundle = new Bundle();

            if (
                jsonProperties != null &&
                !jsonProperties.trim().isEmpty()
            ) {
                JSONObject object =
                    new JSONObject(
                        jsonProperties
                    );

                Iterator<String> keys =
                    object.keys();

                while (keys.hasNext()) {
                    String key = keys.next();

                    Object value =
                        object.opt(key);

                    if (
                        value == null ||
                        value == JSONObject.NULL
                    ) {
                        continue;
                    }

                    if (value instanceof Boolean) {
                        bundle.putLong(
                            key,
                            ((Boolean) value)
                                ? 1L
                                : 0L
                        );

                    } else if (
                        value instanceof Integer ||
                        value instanceof Long
                    ) {
                        bundle.putLong(
                            key,
                            ((Number) value)
                                .longValue()
                        );

                    } else if (
                        value instanceof Float ||
                        value instanceof Double
                    ) {
                        bundle.putDouble(
                            key,
                            ((Number) value)
                                .doubleValue()
                        );

                    } else {
                        bundle.putString(
                            key,
                            String.valueOf(
                                value
                            )
                        );
                    }
                }
            }

            analytics.logEvent(
                name,
                bundle
            );

            return true;

        } catch (Exception error) {
            return false;
        }
    }
}
"""


def _write_firebase_analytics_android_resources(
    root: Path,
    config: FirebaseAnalyticsConfig,
) -> Path:
    """Write Android string resources required by Firebase Analytics."""

    values_dir = (
        root
        / "android_resources"
        / "values"
    )

    values_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    resource_path = (
        values_dir
        / "firebase_analytics.xml"
    )

    content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        "    <string name=\"google_app_id\" translatable=\"false\">"
        + xml_escape(
            config.application_id
        )
        + "</string>\n"
        "    <string name=\"google_api_key\" translatable=\"false\">"
        + xml_escape(
            config.api_key
        )
        + "</string>\n"
        "    <string name=\"project_id\" translatable=\"false\">"
        + xml_escape(
            config.project_id
        )
        + "</string>\n"
        "</resources>\n"
    )

    resource_path.write_text(
        content,
        encoding="utf-8",
    )

    return resource_path


def configure_firebase_analytics_android_project(
    path: str | Path = ".",
    *,
    google_services_path: str | Path | None = None,
    package_name: str | None = None,
) -> tuple[
    Path,
    Path,
]:
    """Add Firebase Analytics native build settings to an Android project."""

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

    requirements = (
        FirebaseAnalyticsAndroidBridge(
            FirebaseAnalyticsConfig(
                application_id="1:0:android:hyperkit",
                api_key="hyperkit-build-config",
                project_id="hyperkit-build-config",
            )
        )
        .build_requirements
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

    text = _merge_csv_setting(
        text,
        "android.add_src",
        requirements.java_source_dirs,
    )

    if google_services_path is not None:
        config = load_firebase_analytics_config(
            google_services_path,
            package_name=package_name,
        )

        _write_firebase_analytics_android_resources(
            root,
            config,
        )

        text = _merge_csv_setting(
            text,
            "android.add_resources",
            (
                "android_resources",
            ),
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
        / "analytics"
        / "HyperKitFirebaseAnalytics.java"
    )

    java_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    java_path.write_text(
        FIREBASE_ANALYTICS_JAVA_SOURCE,
        encoding="utf-8",
    )

    return (
        spec_path,
        java_path,
    )


__all__ = [
    "FIREBASE_ANALYTICS_DEPENDENCY",
    "FIREBASE_ANALYTICS_JAVA_SOURCE",
    "FirebaseAnalyticsAndroidBridge",
    "FirebaseAnalyticsAndroidProvider",
    "FirebaseAnalyticsConfig",
    "configure_firebase_analytics_android_project",
    "load_firebase_analytics_config",
]
