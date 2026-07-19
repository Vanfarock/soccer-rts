# Real-Time Tactical Soccer (RTS)

### Game Design Document — v0.1

**Engine:** Python + Pygame
**Camera:** Top-down tactical (live tactics-board view)
**MVP Scope (current):** Phase 0 manual-control sandbox — focus, move, pass/toss, receive. Full vision (commands, autonomous agents, opponent) is layered on per §6.

---

## 1. Elevator Pitch

You are not a player. You are not even a coach in the Football Manager sense, clicking through menus between matches. You are the **live tactical brain** of a football team, issuing intent in real time while eleven autonomous agents interpret your will through the lens of their own skill, awareness, and understanding of the system you've taught them.

Think **StarCraft's decision-density**, applied to **Guardiola's positional football**, rendered as a **minimalist tactics board that plays itself**.

---

## 2. Expanded Core Vision

Your original pillars are strong and I've kept them intact. Here's where I'd push further:

### 2.1 Space as currency, made visible

If space is the core resource, the game should **render it**, not just simulate it. This is the single biggest opportunity of the top-down tactical camera: you can show a **heatmap/voronoi overlay** of controlled space in real time — the way broadcast analysis shows "pitch control" models. This turns an abstract tactical idea into something the player _sees and reacts to viscerally_, the same way a StarCraft player reads a minimap.

**Suggestion:** Make "space control" a toggleable overlay (like a minimap layer), not mandatory clutter. Early game: player learns by eye. Later: player learns to read the overlay like an X-ray.

### 2.2 Commands as a language, not a menu

Your Strategic → Tactical → Operational hierarchy is good. I'd suggest formalizing it as a **grammar**:

`[SCOPE] + [VERB] + [MODIFIER]`

- **Scope:** Whole team / a line (defense, midfield, attack) / a flank (left, right) / an individual (via click-select)
- **Verb:** Press, Hold, Overload, Stretch, Compact, Recycle, Switch, Isolate, Pin, Overlap
- **Modifier:** Intensity (low/med/high), Target zone (half-space, channel, box), Trigger condition (on turnover, on backpass, on wide entry)

This keeps the command surface small (a handful of verbs) but combinatorially deep — same design philosophy as StarCraft's small unit roster with huge strategic depth.

### 2.3 The "Philosophy Programming" layer is your unique hook

The "if left-back overlaps → winger tucks in, striker attacks near post" system is the most novel part of your pitch — it's essentially **visual scripting for football patterns**. This deserves to be a first-class feature, not a late addition, because it's what turns "commanding" into "coaching a system," and it's what produces the emergent "I never told him to make that run" moments you want.

**Suggestion for MVP-later:** a simple trigger→response rule editor (if X happens, teammates in role Y do Z), starting with 3-5 hardcoded patterns before you build a UI for custom ones.

### 2.4 Attention economy needs a hard currency

Right now "limited commands" is a good instinct but vague. Suggest an explicit resource:

- **Focus Points (FP):** regenerate over time (e.g., 1 per 3 seconds). Each command costs FP based on scope/complexity (a single-player instruction = 1 FP, a team-wide restructure = 3-4 FP).
- This makes the tactical rhythm legible: you _feel_ when you're "banking" attention for a big moment (like mana in a MOBA) vs. spamming small adjustments.

### 2.5 Information warfare — start simple

Full fog-of-war/vision-cones for 22 players is a lot of simulation complexity for a fun-project MVP. Suggest deferring this to post-MVP, but keep the _hook_ for later: a simple "awareness" stat per player that affects reaction _delay_ (not full information hiding) gets you 80% of the emotional effect for 20% of the cost.

---

## 3. Command Hierarchy (Refined)

| Level           | Frequency                  | Examples                                                      | FP Cost                     |
| --------------- | -------------------------- | ------------------------------------------------------------- | --------------------------- |
| **Strategic**   | Pre-match / rare mid-match | Formation, mentality, defensive line height, pressing trigger | High (locks in for a while) |
| **Tactical**    | Every 10-30s               | Attack left, build centrally, trigger press, switch play      | Medium                      |
| **Operational** | Every few seconds          | Overlap, cut inside, pin CB, drop between CBs                 | Low                         |
| **Individual**  | Click-select a player      | Direct one-off instruction to a single agent                  | Low, but limited uses/match |

---

## 4. The Football Agent (Design Level)

Each player is an autonomous agent with:

**Attributes (drive decision-making, not just stats):**

- `Vision` — how much of the pitch state they factor into decisions
- `Decision Speed` — reaction delay before acting on new information
- `Technical Skill` — success probability of the chosen action (pass accuracy, first touch, etc.)
- `Positional IQ` — how well they interpret an abstract command into correct positioning
- `Stamina` — affects speed/decision quality over time
- `Discipline` — how strictly they follow the current philosophy vs. improvising

**Decision loop (conceptually), each tick:**

1. Perceive local game state (ball, teammates, opponents, current commands active)
2. Check active philosophy triggers (did a teammate just do X?)
3. Check active command from player (highest-priority override)
4. Evaluate options via a **utility function** (see technical section)
5. Act (move, pass, dribble, tackle, shoot)

---

## 5. Decisions (Confirmed)

1. **Match length:** 10 minutes real-time by default, exposed as a config value (`MATCH_DURATION_SECONDS`) so it's trivial to shorten further for rapid testing or lengthen later.
2. **Ball physics:** simple 2D kinematic model — position + velocity + friction, no physics engine. Confirmed, see §7.
3. **MVP sequencing:** the _very first_ playable milestone is **agents that move and act autonomously on their own** — no opponent, no score, no goals yet. The fun to validate first is "does watching my own team's autonomous behavior feel alive?" Everything else (opponent AI, goals/scoring, commands) is layered on only once that's proven fun. This reorders the roadmap below — see Phase 1.

---

## 6. Minimal Roadmap — Core Loop First

Confirmed priority: prove autonomous agent behavior is fun _by itself_ before adding an opponent, before adding goals/scoring, before adding the command layer. Here's the reordered roadmap — each phase a playable milestone, not a checklist.

### Phase 0 — Technical Bootstrap: Manual Control Sandbox

This phase is pure engineering scaffolding, not a "fun test" — Phase 1 is where the real design question gets answered. The goal here is to build and feel the core verbs (move, kick, pass, receive) yourself before an AI has to decide when to use them, so any bugs are obviously physics bugs, not decision bugs.

**Key architecture decision:** separate _actions_ from _input source_, so this code is not throwaway. Implemented as layered packages (see §7.1):

```python
# domain/player — identity, pose, facing (no ball rules)
class Player(GameObject): ...

# domain/ball — velocity, carrier ref (GameObject), physics component
class Ball(GameObject): ...

# application/possession — sole place that knows both Player and Ball
class PossessionService:
    @staticmethod
    def try_receive(player, ball): ...
    @staticmethod
    def kick(player, ball, power): ...

class KeyboardControllerComponent:
    def update(self, ctx):
        PossessionService.try_receive(player, ball)
        # WASD handled by PlayerMovementComponent; Space/RMB -> PossessionService.kick

class AIController:  # Phase 1 drop-in
    def update(self, ctx):
        # same PossessionService / movement hooks, different decision source
        ...
```

In Phase 1, `KeyboardControllerComponent` is swapped for an AI controller — domain entities and `PossessionService` stay unchanged.

**Build list:**

1. Window + fixed-timestep game loop
2. Pitch rendering (rectangle, lines, goal areas — unused for now)
3. `Ball` class: position, velocity, friction, boundary bounce _(touchlines use bounce as a Phase 0 placeholder; throw-ins replace left/right `EdgeResponse.BOUNCE` later — see `domain/ball/boundary.py`)_
4. `Player` class: position, velocity, acceleration/max-speed, facing direction, collision radius
5. `KeyboardControllerComponent`: WASD → movement; Space/click → `PossessionService.kick()` when in possession
6. **Focus control:** Tab focuses ball carrier; number keys select a home player; only the focused player accepts input
7. Basic kick physics: kick sets ball velocity from power + facing direction; charged pass (RMB hold) shows aim overlay
8. _(Optional, cheap, worth it)_ a second manually-controlled player on arrow keys, so you can test **passing** between two human-controlled dots before any AI exists — this validates the pass mechanic's feel independently of decision-making.

**Goal:** the foundation renders, moving/kicking/passing feels physically right, and the action layer is ready for an AI brain to plug into.

### Phase 1 — Autonomous Agents, No Opponent, No Score ⭐ (your real MVP)

- One full team (11 agents) on an otherwise empty pitch, no goals, no opposition
- Each agent uses steering behaviors (§7.2) + utility-based decision-making (§7.3) to: move to receive, pass to a teammate, dribble, position via role-based anchors (§7.4)
- No player input at all yet — you are purely an observer
- **Goal:** answer the real design question first — _does watching this team pass, move, and hold shape on its own feel alive and fun to watch?_ If yes, everything else is worth building. If no, this is the cheapest possible point to find that out and iterate on the agent AI itself.

### Phase 2 — Basic Commands (still no opponent)

- Introduce a small set of Operational/Tactical commands (e.g., attack left, hold shape, press) and the Focus Points system (§2.4, §7.5)
- Still no opponent — you're learning whether _influencing_ the autonomous team is satisfying before adding the complexity of a second brain
- **Goal:** commands visibly and satisfyingly change team behavior.

### Phase 3 — Scripted Opponent AI (reacts to you)

- Mirror-team opponent with a simple rule-based brain: reacts to your pressing intensity, mirrors/counters your shape, makes its own basic decisions
- Same agent AI as your team, just running its own (simpler) command logic instead of taking player input
- **Goal:** first real "vs" experience — two systems competing for space.

### Phase 4 — Goals & Scoring

- Add goal areas, scoring, win/loss state, and the `MATCH_DURATION_SECONDS` countdown (default 10 min, configurable)
- Replace touchline boundary bounce with **throw-ins** (and goal-line restarts: goal kicks, corners) — wired via `EdgeResponse.OUT_OF_PLAY` in `domain/ball/boundary.py`
- **Goal:** the loop now has stakes — commands and positioning finally matter toward an outcome.

### Phase 5 — Philosophy/Pattern System (stretch, post-MVP)

- Hardcode 3-5 "if X then Y" team patterns (e.g., fullback overlaps → winger tucks in)
- Toggle them on/off, observe emergent play

**Everything else (progression, space-control overlay, fog of war, multiplayer, full pattern editor, art polish) comes after Phase 4 is fun.** Phase 1 is your cheapest and most important checkpoint — it's pure agent-AI quality with zero other systems to hide behind, so treat it as the real "is the core idea fun" test.

---

## 7. Technical Starter Guide (Pygame)

### 7.1 Project structure (implemented)

Code lives under `src/` with explicit layers. **`AGENTS.md`** is the source of truth for import rules; this section summarizes layout for design context.

```
src/
├── main.py
├── shared/                  # colors, entity sizes (no src deps)
├── infra/engine/            # GameObject, Component, window, render, collision
├── domain/
│   ├── player/              # Player entity
│   ├── ball/                # Ball + BallPhysicsComponent
│   ├── pitch/               # Pitch markings, DRAG constant
│   └── team/                # Team enum
└── application/
    ├── game.py              # composition root, spawn, outer loop
    ├── possession.py        # kick / receive / attach (knows Player + Ball)
    └── components/          # keyboard, movement, focus, ball_receiver
```

**Layer dependency:** `shared ← infra ← domain ← application ← main`. Domain siblings (`player`, `ball`, …) do not import each other; cross-entity flows (possession) live in `application/possession.py`.

Planned additions (not yet present): `ai/` (decision, behaviors), `tactics/` (philosophy), HUD overlay — see roadmap §6.

### 7.2 Movement — Steering Behaviors

Don't hand-code pathing per situation. Use classic **steering behaviors** (Craig Reynolds' model — the same foundation used in most sports/crowd sims):

- `seek(target)` — move toward a point
- `arrive(target)` — seek but decelerate on approach (for receiving a pass)
- `intercept(moving_target)` — predict ball trajectory and move to meet it
- `separate(nearby_agents)` — avoid teammate collisions
- `pursue` / `evade` — for marking and dribbling past defenders

Each agent picks ONE dominant steering behavior per tick, chosen by the decision layer below. This is lightweight and fast — perfectly fine in Python/Pygame for 22 agents.

### 7.3 Decision-Making — Utility AI (recommended over Finite State Machines)

A pure FSM (Idle → Chasing → Passing → etc.) gets brittle fast with 11 interacting agents and layered commands. Instead, use **Utility AI**: each tick, score every possible action, take the highest score.

```python
def evaluate_actions(agent, world_state):
    actions = {
        "pass_to_teammate": score_pass(agent, world_state),
        "dribble_forward": score_dribble(agent, world_state),
        "shoot": score_shot(agent, world_state),
        "hold_position": score_hold(agent, world_state),
        "press_opponent": score_press(agent, world_state),
    }
    return max(actions, key=actions.get)
```

Each `score_*` function returns 0.0–1.0 based on factors like: distance to goal, passing lane openness, teammate positioning IQ, current active command bias, and philosophy triggers. **Active commands simply add weight** to relevant actions — e.g., "Attack the left" adds +0.3 utility to any action that moves the ball leftward/forward for left-side players. This is clean because commands never _force_ an action, they _bias_ the existing decision system — which is exactly the "intelligent interpretation" you described in your pitch.

### 7.4 Positioning without commands — Role-based anchor points

Give each player a **dynamic anchor point** relative to ball position and team shape (a formation "skeleton" that shifts as the ball moves — this is how real tactical boards work). Example: a fullback's anchor = `base_position + (ball_position - pitch_center) * role_elasticity`. Agents `arrive()` toward their anchor when not actively involved in the play. This alone produces surprisingly convincing "shape" without any AI complexity.

### 7.5 Suggested tunable parameters (config.py)

```python
PLAYER_ATTRS = {
    "max_speed": 4.0,          # px/tick or m/s scaled
    "acceleration": 0.3,
    "vision_radius": 250,       # px, how far they perceive
    "decision_delay": 0.15,     # seconds, reaction time
    "pass_accuracy": 0.85,      # 0-1 chance modifier
    "positional_iq": 0.7,       # 0-1, how well they read commands
    "stamina_drain_rate": 0.002,
}

FP_SYSTEM = {
    "regen_per_second": 0.33,
    "cost_individual_command": 1,
    "cost_operational_command": 2,
    "cost_tactical_command": 3,
    "cost_strategic_command": 5,
}

MATCH_SETTINGS = {
    "MATCH_DURATION_SECONDS": 600,   # 10 minutes, tweak freely for testing
}
```

### 7.6 Visual style — minimalist tactics board

Given your top-down tactical choice, lean into flat, high-contrast, broadcast-analysis aesthetics rather than trying to render realistic players:

- Solid-color circles/chevrons for players (team color + role letter or number)
- A thin directional indicator (facing/momentum arrow) on each player
- Ball as a small white/yellow dot with a motion trail
- Pitch: flat green or dark tactical-board style (navy/charcoal background with white lines — closer to a coach's whiteboard than a real pitch)
- Command feedback: a brief animated pulse/ring on the players affected when you issue a command, so the "intent" is visually legible even without deep observation

This keeps the art budget near zero while making the _information_ the visual star — which fits the "tactical brain" fantasy far better than trying to fake realistic 3D players.

### 7.7 Performance note

22 agents × utility scoring × steering, all in pure Python at 30-60fps, is very feasible in Pygame as long as you avoid recomputing expensive things (like full line-of-sight checks) every single tick for every agent. A simple optimization: stagger full "deep" decision evaluation across agents (e.g., 3-4 agents re-evaluate deeply per frame, others coast on their last decision) — cheap and invisible to the player, and mirrors how real players don't reconsider everything every instant either.

---

## 8. Summary

| Pillar          | Your Original Idea       | Refinement                                                                                                                                                                     |
| --------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Core resource   | Space                    | Make it visible via an optional overlay                                                                                                                                        |
| Command system  | 3-tier hierarchy         | Formalize as a small grammar (scope+verb+modifier)                                                                                                                             |
| Attention limit | Vague "limited commands" | Explicit Focus Points resource                                                                                                                                                 |
| Emergent play   | Philosophy patterns      | Trigger→response rules, hardcoded first, editable later                                                                                                                        |
| Fog of war      | Full vision simulation   | Defer; use reaction-delay-by-awareness as a cheap proxy first                                                                                                                  |
| MVP             | Unclear                  | **Phase 1 — autonomous agents alone, no opponent, no score — is the real first checkpoint.** Opponent (Phase 3) and goals/scoring (Phase 4) are deliberately layered on after. |
| Match length    | Unclear                  | 10 minutes real-time by default, configurable via `MATCH_DURATION_SECONDS`                                                                                                     |

The strongest thing about this concept is that it's genuinely underexplored — no major game treats football as _pure positional-space warfare_ the way you're describing. The risk is scope: this document intentionally strips things down so Phase 4 is reachable in weeks, not months, while preserving every hook that makes the full vision special for later.
