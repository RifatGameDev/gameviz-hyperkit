"""Reusable object pooling helpers for HyperKit games."""

from __future__ import annotations

from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class ObjectPoolError(Exception):
    """Base error for object-pool operations."""


class ObjectPool(
    Generic[T]
):
    """Small reusable object pool for enemies, projectiles, and effects."""

    def __init__(
        self,
        factory: Callable[[], T],
        *,
        initial_size: int = 0,
        max_size: int | None = None,
        on_acquire: Callable[[T], None] | None = None,
        on_release: Callable[[T], None] | None = None,
    ) -> None:
        if not callable(
            factory
        ):
            raise ObjectPoolError(
                "factory must be callable."
            )

        initial_size = int(
            initial_size
        )

        if initial_size < 0:
            raise ObjectPoolError(
                "initial_size cannot be negative."
            )

        if max_size is not None:
            max_size = int(
                max_size
            )

            if max_size <= 0:
                raise ObjectPoolError(
                    "max_size must be greater than zero."
                )

            if initial_size > max_size:
                raise ObjectPoolError(
                    "initial_size cannot exceed max_size."
                )

        self.factory = factory
        self.max_size = max_size
        self.on_acquire = on_acquire
        self.on_release = on_release
        self._available: list[T] = []
        self._active: list[T] = []

        for _ in range(
            initial_size
        ):
            self._available.append(
                self._create()
            )

    @property
    def active_count(
        self,
    ) -> int:
        return len(
            self._active
        )

    @property
    def available_count(
        self,
    ) -> int:
        return len(
            self._available
        )

    @property
    def total_count(
        self,
    ) -> int:
        return (
            self.active_count
            + self.available_count
        )

    @property
    def active_items(
        self,
    ) -> tuple[T, ...]:
        return tuple(
            self._active
        )

    def _create(
        self,
    ) -> T:
        return self.factory()

    def acquire(
        self,
    ) -> T:
        if self._available:
            item = self._available.pop()
        else:
            if (
                self.max_size is not None
                and self.total_count
                >= self.max_size
            ):
                raise ObjectPoolError(
                    "Object pool has reached max_size."
                )

            item = self._create()

        self._active.append(
            item
        )

        if self.on_acquire is not None:
            self.on_acquire(
                item
            )

        return item

    def release(
        self,
        item: T,
    ) -> bool:
        index = next(
            (
                index
                for index, active
                in enumerate(
                    self._active
                )
                if active is item
            ),
            None,
        )

        if index is None:
            return False

        released = self._active.pop(
            index
        )

        if self.on_release is not None:
            self.on_release(
                released
            )

        self._available.append(
            released
        )

        return True

    def release_all(
        self,
    ) -> int:
        items = list(
            self._active
        )

        for item in items:
            self.release(
                item
            )

        return len(
            items
        )

    def clear(
        self,
    ) -> int:
        count = self.total_count
        self._active.clear()
        self._available.clear()
        return count
