# Changelog

## v0.2.0 (2026-11-06): Pokémon agents plus, by SaifHarding on mathieucroset's original

### New
- Faces in the sidebar. A new mod, `pokemon-agents-list`, is Herdr's agents list with each agent's
  PMDCollab portrait in place of its program icon. The face follows the agent: Determined while it
  works, Worried while it waits on you, Happy when it's done, Normal otherwise. A Pokémon without
  that face shows Normal; one without portraits shows its menu icon.
- Cries. When an agent starts waiting on you, its Pokémon cries (an MP3 from Pokémon Showdown). When
  it finishes while you weren't looking, it chirps: the same cry, higher and at half volume. At most
  one sound every 1.5 s. Pikachu and Eevee use their voiced Let's Go cries rather than the 1996 ones.
- `mods/pokemon-agents/silent.mp3`, to point Herdr's own blocked and done sounds at.

### Changed
- The strip fetches the menu icons, each agent's portraits and its cry as soon as the agent turns
  up, so they're ready before they're needed. It needs ffmpeg for the chirp.

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
