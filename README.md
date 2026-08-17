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

**To try it now:** open the `192.168.x.x` address on your phone while
`server.py` is running. On iPhone use Share → *Add to Home Screen*; on Android
use the ⋮ menu → *Add to Home screen*. You get an icon and a fullscreen app.

The catch: this only works at home with your PC on, and offline mode won't
work. Browsers only allow offline caching (service workers) over HTTPS.

**For daily use, host it.** Any free static host gives you an HTTPS URL that
works anywhere, with offline support and no PC running:

```
cd C:\Users\nkrum\fitness
git init
git add .
git commit -m "Groundwork"
gh repo create groundwork --public --source=. --push
```

Then in the repo's **Settings → Pages**, set Source to `main` / root. A minute
later it's live at `https://<your-username>.github.io/groundwork/`. Open that on
your phone and add it to your home screen. Push a change, and the phone picks
it up on next open.

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
| Days per week | `dayTemplate()` and the `/ 3` in `currentWeek()` |
| Colors, light/dark | the `:root` token blocks at the top of the `<style>` |
| The icon | `make_icons.py`, then re-run `python make_icons.py` |

After editing, hard-reload on the phone (pull down to refresh) — `sw.js` serves
the page network-first, so edits appear as soon as the phone can reach the
source.

---

## A note on the first three weeks

They will feel too easy. That's deliberate: the most common way a beginner plan
fails is week-one enthusiasm producing week-three soreness and a quiet
quit. Jogging starts in week 4, once your joints and tendons have had three
weeks of load. Don't skip ahead.
