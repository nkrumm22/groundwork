# Groundwork

A 12-week fitness app for a sedentary start: bodyweight strength, a
walk-to-run progression, weight tracking, and daily basics. Three sessions a
week. No equipment, no gym.

Everything is vanilla HTML/CSS/JS in one file — no build step, no npm, no
dependencies. Open `index.html` and read it top to bottom; it's organised in
numbered sections.

---

## Run it

```
python server.py
```

Then open the printed address. It prints two:

- `http://localhost:4100` — on this PC
- `http://192.168.x.x:4100` — on your phone, same Wi-Fi

Stop it with Ctrl+C.

---

## Get it onto your phone

**It's live here:**

### https://nkrumm22.github.io/groundwork/

Open that on your phone and install it:

- **iPhone** — Safari → Share → *Add to Home Screen*
- **Android** — Chrome → ⋮ → *Install app*

You get an icon, a fullscreen app with no browser bars, and full offline
support. Your PC does not need to be on.

`server.py` is still useful for developing — edits show up instantly without
pushing.

### Publishing a change

```
git add -A
git commit -m "what changed"
git push
```

GitHub rebuilds in under a minute. The phone picks it up next time you open the
app (`sw.js` serves the page network-first, so you get the new version as soon
as you have a connection, and the cached one when you don't).

---

## Your data

Everything lives in your phone's `localStorage` — nothing is uploaded anywhere,
and there is no account. Two consequences:

- **The phone copy and the PC copy are separate.** They don't sync.
- **Clearing browser data erases your history.** Use *Plan → Export backup*
  every so often; *Import* restores it.

---

## Food

The **Food** tab tracks four things by tapping — vegetables, protein, water,
home-cooked meals — plus a neutral count of meals out. Tap the nth pip to set
that value; tap the filled pip you're on to take one back. Targets are editable
at the bottom of the tab.

**There is deliberately no calorie counting, no daily budget, and no score for
the day.** Habit tracking is what people actually sustain, and the request here
was to eat better rather than to hit a number. It also keeps the app honest
with the decision to track weight without a target.

Two rules the code holds to, both easy to break by accident:

- **"Nothing logged" and "nothing hit yet" are different states.** Telling
  someone who has been logging all day that they've logged nothing is just
  wrong. `anyFoodLogged()` decides the first; `goalsMet()` decides the second.
- **Meals out is counted, never scored.** It has no target, shows no
  denominator, and can't lower your count. It exists so a pattern is visible.

To change what's tracked, edit `FOOD` (section 7c). Anything with
`neutral: true` is observation only and stays out of `FOOD_GOALS`.

Eating used to be a yes/no "Ate well" toggle in Today's basics. That was
removed when this tab arrived — a vague daily verdict sitting directly above
real counters just contradicts them. Habits now come from the `HABITS` list,
which both the Today screen and the consistency heatmap read.

## The plan

| Phase | Weeks | What happens |
|---|---|---|
| Foundation | 1–3 | Walking only, easy bodyweight circuits. Builds the habit. |
| Build | 4–7 | Jog intervals begin. Harder movement progressions. |
| Progress | 8–12 | Longer jogs, building to 20 minutes unbroken. |

Each week is Strength A → Cardio → Strength B.

**The plan advances on sessions completed, not on the calendar.** Miss two
weeks and you resume exactly where you stopped — nothing is skipped and nothing
is "behind." That's in `currentWeek()`.

Movements auto-progress by phase — a wall push-up in week 2 is a knee push-up
by week 8. The progressions are the three-item `name` arrays in `DAY_A` and
`DAY_B`; sets and reps are the parallel `sets`/`reps` arrays, one entry per
phase.

---

## Changing things

| To change… | Edit… |
|---|---|
| Exercises, sets, reps, cues | `DAY_A` / `DAY_B` (section 1) |
| The run progression | `CARDIO` (section 1) |
| Movement demos & form tips | `FIG` (section 7b) |
| Days per week | `dayTemplate()` and the `/ 3` in `currentWeek()` |
| Colors, light/dark | the `:root` token blocks at the top of the `<style>` |
| The icon | `make_icons.py`, then re-run `python make_icons.py` |

### Timers

Starting a session starts a **session clock** in the header, which runs until
you finish and becomes the duration that gets logged. The app also asks the
phone to keep the screen awake for the session, so it doesn't sleep mid-set.

On strength days, completing a set starts a **60-second rest countdown** with
`+30s` and `Skip rest`. It ends with a tone and a buzz, and doesn't appear
after the final set — the session is over at that point. Change `REST_SEC` to
adjust the default.

On cardio days the interval timer handles the jog/walk switches, beeping and
buzzing at each change. Plank-style holds get their own countdown.

**Every timer runs on wall-clock timestamps**, not by decrementing a variable
once a second. Each phase stores the moment it ends, so a throttled or
suspended tab can't make the clock drift — on the next tick it simply
recalculates where it should be.

### When the screen was off

Phones suspend JavaScript when the screen locks, so a run can come back to the
app several minutes adrift. The app can't know whether you carried on running
during that time, and guessing wrong either invents work you didn't do or
throws away work you did. So it asks.

Gaps under 15 seconds (`GAP_ASK`) are ordinary throttling and get absorbed
silently. Anything longer pauses the timer, leaves your position untouched, and
offers two answers:

- **I kept going** — wall-clock wins. The queue fast-forwards to where you
  actually are, sounding the cue for the phase you land in.
- **I stopped** — the gap is discarded and you resume exactly where you were.

If the gap was longer than the whole remaining session, it ends the session
rather than running off the end of the queue.

One thing this can't fix: while the screen was off you didn't hear the
jog/walk cues, so you may not have switched when the plan wanted. The app
corrects the clock, not the run.

### Movement demonstrations

Tap any exercise — in the Today card, in a week's detail, or via **Show me
how** mid-session — for an animated figure of the movement plus two things to
watch for.

The figures are vector drawings, not video: a few kilobytes total, and they
work with no connection. Each one is just two poses — the top and bottom of the
rep — that the app interpolates between. The lowering phase is deliberately
slower than the lift, because that's the tempo worth copying.

To adjust one, edit its entry in `FIG`. Poses are joint coordinates in a
100×100 box, figure facing right, floor at y=92:

```js
squat: {
  props: [{ t:"floor" }],
  a: { hd:[44,16], sh:[44,28], hip:[44,52], kn:[44,72], an:[44,92], … },  // top
  b: { hd:[40,22], sh:[40,34], hip:[34,58], kn:[50,72], an:[46,92], … },  // bottom
  watch: ["…", "…"],
},
```

`hd` head, `sh` shoulder, `hip`, `kn` knee, `an` ankle, `el` elbow, `wr` wrist.
Add `kn2`/`an2` (or `el2`/`wr2`) when the two sides differ, as in single-leg
work; otherwise the far limb is drawn faintly behind at a small offset. `toe`
is optional and draws a foot — needed for the calf raise, where without it the
figure just appears to levitate. Set `hold: true` for a static position like a
plank, and give only pose `a`.

The frame is auto-fitted to whatever you draw, so you don't need to fill the
box. Anyone whose device asks for reduced motion sees the two poses side by
side instead of a loop.

After editing, hard-reload on the phone (pull down to refresh) — `sw.js` serves
the page network-first, so edits appear as soon as the phone can reach the
source.

---

## A note on the first three weeks

They will feel too easy. That's deliberate: the most common way a beginner plan
fails is week-one enthusiasm producing week-three soreness and a quiet
quit. Jogging starts in week 4, once your joints and tendons have had three
weeks of load. Don't skip ahead.
