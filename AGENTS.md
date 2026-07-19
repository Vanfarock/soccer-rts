# soccer-rts — agent guide

**One-liner:** Top-down tactical soccer RTS — Python + Pygame, manual-control sandbox (Phase 0).

**Entrypoint:** `uv run python src/main.py` (`src/` is on `PYTHONPATH` via the script location).

## Source tree

```
src/
  main.py                 # entry only
  shared/                 # foundation (colors, sizes — no src deps)
  infra/
    engine/               # window, clock, scene graph, collision, render
  domain/
    player/               # Player entity + entity-local render
    ball/                 # Ball + BallPhysicsComponent
    pitch/                # dimensions, markings, scene root, DRAG
    team/                 # Team enum + jersey colors
  application/
    game.py               # composition root + outer loop
    possession.py         # kick / receive / attach orchestration
    components/           # focus, keyboard, movement, ball_receiver
```

## Layer rules

| Folder | Owns | May import | Must not |
|---|---|---|---|
| `shared/` | Colors, sizes, pure constants | stdlib only | Anything else under `src/` |
| `infra/` | Window, clock, scene graph, collision, render, frame plumbing | `shared` | `domain`, `application` |
| `domain/` | Entity state + entity-local behavior | `infra`, `shared` | `application`; **sibling domain packages** (`player` ↛ `ball`) |
| `application/` | Match wiring, focus, input→actions, possession flows, aim overlays | `domain`, `infra`, `shared` | Be imported by `domain` or `infra` |

Dependency direction:

```
shared ← infra ← domain ← application ← main
```

## Hard rules

- **No circular imports** between layers or domain siblings.
- **No `TYPE_CHECKING` or local imports** to hide coupling — fix the layer instead.
- **No sideways `domain.*` imports** (e.g. `domain.player` must not import `domain.ball`).
- **Put new code in the matching folder** — don't add flat packages under `src/`.
- **Canonical engine types:** import `GameObject`, `Component`, `GameObjectType` from `infra.engine.entity`.
- **Possession logic lives only in `application/possession.py`** — domain entities never call each other's kick/receive rules.

## When adding X → folder Y

| You're adding… | Put it in… |
|---|---|
| A color, radius, tunable constant | `shared/` |
| Window, render primitive, collision, clock | `infra/engine/` |
| Player pose, ball velocity, pitch markings | `domain/<entity>/` |
| Keyboard handling, focus switching, kick/receive flow | `application/` or `application/components/` |
| Spawning entities, wiring the match loop | `application/game.py` |

## Doc roles

- **`docs/GDD.md`** — game design: mechanics, roadmap, vision, tunables.
- **`AGENTS.md`** (this file) — code structure, layering, import rules.

### GDD sync rule

When a design or architecture change affects systems or entities, **update `docs/GDD.md` in the same change set**. Before treating a feature as done, confront the implementation against the GDD — if they disagree, resolve explicitly (prefer GDD for product intent; prefer code when GDD is stale for the implemented MVP).

## Import style

```python
from infra.engine.entity import GameObject, Component
from domain.player.player import Player
from domain.ball.ball import Ball
from application.possession import PossessionService
from shared.entity_sizes import PLAYER_RADIUS
```

## Current MVP (Phase 0 sandbox)

Implemented and playable:

- Pitch rendering with drag-based ball deceleration
- **Focus control:** Tab snaps focus to ball carrier; number keys (1–9, 0) select home roster
- **Movement:** WASD on focused home player; slower when carrying
- **Possession:** proximity receive; post-kick pickup block until ball clears pickup radius
- **Kick/toss:** Space = quick toss; RMB hold/release = charged pass with aim overlay
- Away players auto-receive via `BallReceiverComponent`

Not yet implemented (see GDD roadmap): FP system, commands, autonomous AI, scoring.
