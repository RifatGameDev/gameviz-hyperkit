import pytest

from hyperkit import (
    GameObject,
    ObjectPool,
    ObjectPoolError,
)


def test_object_pool_preallocates_and_reuses_items():
    created = []

    def factory():
        obj = GameObject()
        created.append(
            obj
        )
        return obj

    pool = ObjectPool(
        factory,
        initial_size=2,
    )

    assert pool.available_count == 2
    assert pool.total_count == 2

    first = pool.acquire()
    second = pool.acquire()

    assert pool.active_count == 2
    assert len(
        created
    ) == 2

    assert pool.release(
        first
    )

    again = pool.acquire()

    assert again is first
    assert second in pool.active_items


def test_object_pool_calls_lifecycle_callbacks():
    events = []

    pool = ObjectPool(
        GameObject,
        on_acquire=lambda obj: (
            events.append(
                "acquire"
            )
        ),
        on_release=lambda obj: (
            events.append(
                "release"
            )
        ),
    )

    obj = pool.acquire()
    assert pool.release(
        obj
    )

    assert events == [
        "acquire",
        "release",
    ]


def test_object_pool_enforces_max_size():
    pool = ObjectPool(
        GameObject,
        max_size=1,
    )

    pool.acquire()

    with pytest.raises(
        ObjectPoolError,
        match="max_size",
    ):
        pool.acquire()


def test_object_pool_release_all_and_clear():
    pool = ObjectPool(
        GameObject,
        initial_size=1,
    )

    pool.acquire()
    pool.acquire()

    assert pool.release_all() == 2
    assert pool.active_count == 0
    assert pool.available_count == 2
    assert pool.clear() == 2
    assert pool.total_count == 0


def test_object_pool_rejects_invalid_sizes():
    with pytest.raises(
        ObjectPoolError
    ):
        ObjectPool(
            GameObject,
            initial_size=-1,
        )

    with pytest.raises(
        ObjectPoolError
    ):
        ObjectPool(
            GameObject,
            initial_size=2,
            max_size=1,
        )



def test_object_pool_release_uses_identity_for_equal_objects():
    first = GameObject()
    second = GameObject()
    items = [
        first,
        second,
    ]

    pool = ObjectPool(
        lambda: items.pop(0),
    )

    acquired_first = pool.acquire()
    acquired_second = pool.acquire()

    assert (
        acquired_first
        == acquired_second
    )
    assert (
        acquired_first
        is not acquired_second
    )

    assert pool.release(
        acquired_second
    )

    assert (
        pool.active_items
        == (acquired_first,)
    )
