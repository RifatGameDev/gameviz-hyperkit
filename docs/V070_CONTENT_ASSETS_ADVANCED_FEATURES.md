# HyperKit v0.7 — Content, Assets + Advanced Game Features

HyperKit v0.7 expands the SDK's content-driven workflow and reusable gameplay systems.

## Scope

The v0.7 milestone focuses on:

- structured content manifests
- reusable data-driven prefabs
- cached data loading and preload helpers
- level sequencing
- reusable object pooling
- sprite frame-pattern generation
- keeping the complete-game and mobile runtime foundations stable

## Content Manifests

Use `ContentManifest`, `ContentItem`, and `ContentManager` to describe game content in JSON and query it by id, kind, or tag.

Example manifest:

```json
{
  "name": "Main Content",
  "version": "1",
  "items": [
    {
      "id": "hero",
      "kind": "image",
      "asset": "hero.png",
      "tags": ["player", "character"]
    },
    {
      "id": "quiz-data",
      "kind": "json",
      "asset": "quiz.json",
      "tags": ["quiz"]
    }
  ]
}
```

Example usage:

```python
from hyperkit import ContentManager

content = ContentManager()
content.load("content.json")

hero_path = content.resolve_asset("hero")
questions = content.load_item("quiz-data")
```

Supported loadable content kinds are:

- `image`
- `audio`
- `font`
- `json`
- `csv`
- `text`

Content entries without an asset can carry inline configuration in their `data` field.

## Prefabs

`PrefabLibrary` provides reusable JSON-driven `GameObject` definitions.

Example:

```json
{
  "prefabs": {
    "coin": {
      "object": {
        "name": "coin",
        "type": "collectible",
        "width": 48,
        "height": 48,
        "shape": "circle",
        "data": {
          "score": 10
        }
      }
    }
  }
}
```

Then:

```python
from hyperkit import PrefabLibrary

prefabs = PrefabLibrary()
prefabs.load("prefabs.json")

coin = prefabs.create(
    "coin",
    x=200,
    y=500,
)
```

Overrides may replace top-level object properties while nested `data` values are merged.

## Asset Data Cache

`AssetManager` now supports opt-in cached loading for JSON, CSV, and TXT data.

```python
from hyperkit import AssetManager

assets = AssetManager()

config = assets.load_json(
    "config.json",
    cached=True,
)

assets.preload_data(
    [
        "config.json",
        "items.csv",
        "dialogue.txt",
    ]
)
```

Cached mutable data is returned as a copy so callers cannot accidentally mutate the stored cache.

Use:

- `assets.cache_size`
- `assets.clear_cache()`
- `assets.preload_data(...)`

## Level Sequences

`LevelSequence` provides lightweight ordered level progression.

```python
from hyperkit import LevelManager, LevelSequence

levels = LevelSequence(
    [
        "level_1.json",
        "level_2.json",
        "level_3.json",
    ]
)

manager = LevelManager()
level = levels.load_current(manager)
```

It supports:

- next
- previous
- looping
- reset
- index selection
- current progress
- load-current and advance-and-load helpers

## Object Pooling

`ObjectPool` provides reusable allocation for common mobile-game objects such as:

- projectiles
- enemies
- coins
- obstacles
- temporary effects

Example:

```python
from hyperkit import GameObject, ObjectPool

pool = ObjectPool(
    GameObject,
    initial_size=10,
    max_size=30,
)

enemy = pool.acquire()

# Later
pool.release(enemy)
```

Optional acquire/release callbacks allow callers to reset active state, position, visual state, or gameplay data.

## Sprite Frame Patterns

`SpriteAnimation.from_pattern(...)` creates animation frame lists from a numbered naming convention.

```python
from hyperkit import SpriteAnimation

run = SpriteAnimation.from_pattern(
    name="run",
    pattern="run_{index:02d}.png",
    start=1,
    end=8,
    fps=12,
)
```

## v0.7 Completion Rule

The v0.7 milestone is complete when:

- content-manifest validation and lookup tests pass
- content asset loading tests pass
- prefab registration/loading/creation tests pass
- asset caching and preload tests pass
- level sequencing tests pass
- object-pool reuse and capacity tests pass
- sprite frame-pattern tests pass
- all v0.6 mobile runtime/performance regressions remain green
- all six complete games remain valid
- Python 3.9–3.12 CI remains green
- wheel/sdist build and `twine check` remain green

The public compatibility contract remains API `0.2`.
The public API freeze remains scheduled for v0.9.
