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

The session clock and rest timer work off wall-clock timestamps rather than
counting down a variable, so a locked screen or a backgrounded tab can't make
them drift.

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
