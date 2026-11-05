# Changelog

## v0.1.2 (2026-11-05)

### Fixed
- Idle agents fall asleep again when nothing has happened in their tab since
  Herdr started. Herdr reports no change time for those tabs, and the strip
  read that as "awake", so long-idle Pokémon never slept.

## v0.1.1 (2026-11-04)

### Fixed
- With Herdr's zoom set to anything other than 1, Pokémon no longer walk out of
  the window, and the name tags show again. The strip now converts its reported
  size by the zoom ([#1](https://github.com/mathieucroset/herdr-pokemon-agents/issues/1)).
- If the window gets narrower while a Pokémon is walking, it stops inside the
  strip instead of walking past the new edge ([#1](https://github.com/mathieucroset/herdr-pokemon-agents/issues/1)).

Thanks to [@Blasg2](https://github.com/Blasg2) for the report and the fixes.

## v0.1.0 (2026-11-04)

First release. Every agent is a pixel-art Pokémon (from the first 151) roaming a
strip at the bottom of the window: working agents walk, idle ones stroll and
nap, blocked ones stop and call for you. Click a Pokémon to jump to its agent;
right-click it (or press `alt-shift-p`) to choose which Pokémon it is.
