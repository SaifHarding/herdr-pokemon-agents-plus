# Pokémon agents

A strip along the bottom of the Herdr window where every agent is a pixel-art
Pokémon from the first 151. Working agents walk back and forth, idle ones
stroll and fall asleep after a while, a blocked agent stops and shows a
pulsing "!", and a finished one shows a "✓". Click a Pokémon to jump to its
agent; right-click it to choose which Pokémon it is.

![Pokémon agents](preview.png)

## What you see

- **One strip, 112 px tall**, full width, at the bottom of the window's main
  column (above the status bar in the default layout). Background is the
  theme's `chrome`. A 1 px `border` line runs across it 20 px above the
  bottom: the ground.
- **One Pokémon per agent**, standing on the ground line in a 128 px wide
  column. Sprites come from PMD SpriteCollab sheets, pixel-doubled (2×) with
  nearest-neighbour scaling; Pokémon whose walk frame is taller than 64 px
  (Onix, Gyarados, ...) are drawn at 1×. Each has a soft shadow ellipse
  (`#00000030`, 6 px tall, 70 % of the sprite's visible width) under its feet.
  The sprite is aligned by its visible pixels: feet on the ground, body
  centered on the column.
- **A name tag** under each Pokémon, 10.5 px text in `muted` (`foreground`
  when hovered or focused), preceded by a 6 px dot in the agent's status color
  (`theme().working | blocked | done | idle`). The tag is the tab's name when
  the tab was named, otherwise the space's name. Hovered, it reads
  `<Pokémon> · <tag>`. Tags never overlap: when two would collide, the one
  that matters more stays (hovered > blocked > done > focused > the rest).
- **Bubbles above the head**, 12.5 px bold white on a 7 px-rounded pill:
  `!` on `blocked` (opacity pulse 0.7 ↔ 1 every 900 ms), `✓` on `done`.
  A sleeping Pokémon shows `z` → `zZ` → `zZz` → `zZ` in `muted`, 700 ms apart.
- **While a sprite downloads**, a small Poké Ball (18 px circle, red
  `#e3350d` top, `#f4f4f4` bottom, `foreground` outline) pulses in its place.
- **No agents**: centered 12 px `dim` text, "No agents yet. Each agent you
  start shows up here as a Pokémon."
- **No ImageMagick**: Poké Balls stay, and a note at the top right says
  "Install ImageMagick (magick) to see the Pokémon".
- **The picker** (dialog, 640×560): title "Choose a Pokémon" (15 px
  semibold), a line "for <tag> · now <Pokémon>", a search input with an
  `accent` border, then a scrolling grid of all 151 in Pokédex order: 92×96
  cells with the Gen VII menu icon (80×60), `#025` in `dim` and the name.
  The current pick has an `accent` border and `selected` background.

## How it behaves

- **working**: walks. Picks a random spot at least 60 px away, faces that
  way (side-walking animation), walks there at 70 px/s, pauses 0.3–1.8 s,
  repeats.
- **idle**: strolls at 32 px/s with 4–12 s pauses, standing (idle
  animation, facing the viewer slightly left or right, the way it last
  walked) between strolls. After 3 minutes without a change in its tab
  (`changed_at`), it lies down and sleeps (sleep animation + `zZz`).
- **blocked**: stops where it is (mid-walk too), stands, `!` bubble; its tag
  wins over neighbours.
- **done**: stops, stands, `✓` bubble. Herdr turns `done` into `idle` once
  the person looks at the tab.
- **Click**: `pane.focus { pane }`: Herdr shows that agent's tab and pane
  (`agent.focus { terminal }` for a sub-agent, which has no pane).
- **Right-click**: opens the picker for that agent. Click a Pokémon (or type
  until one is left and press Enter, the input's `submit` event) to choose;
  Esc closes. Search matches names and numbers (`25`, `#025`). The choice is
  saved per pane in shared state, so it survives restarts and a new agent in
  the same pane keeps the same Pokémon.
- **New agents** get a Pokémon from a hash of their pane id, skipping ones
  already on screen, and that pick is saved at once so it never shifts.
- **Key** (optional, `keys.json`): `alt-shift-p` → `pokemon-agents.pick`
  opens the picker for the focused agent (else the first one).

## Built from

- **Layout**: one block `{ "id": "pokemon-agents", "type": "block",
  "content": { "mod": "pokemon-agents" }, "size": { "px": 112 }, "min": 72,
  "max": 240 }` placed in the main (`work`) column, below the tab content and
  above the status bar. `mod.json` is `{ "place": "bottom", "size": 112 }`;
  in a layout whose root is a row, Herdr docks it as a right-hand column
  instead, so move the block into the column by hand.
- **One mod, two roles**: `mods/pokemon-agents/main.js` draws the strip, and
  the same mod opened with `openOverlay({ mod: "pokemon-agents", kind:
  "dialog", width: 640, height: 560, props: { picker: true, slot, current,
  tag } })` draws the picker. It decides which in `init` from `props().picker`.
- **herdr functions**: `agents()`, `spaces()` (tab `named` / `changed_at`),
  `theme()`, `run("pane.focus")` / `run("agent.focus")`, `shared` / `setShared("pokemon-agents",
  { panes: { <pane id>: <dex no> } })` (oldest entries dropped past 300),
  `openOverlay` / `closeOverlay`, `nextCommand()` (`pick`), `exec`, `appHome()`,
  `fs/promises` (`exists`, `mkdir`, `readFile`, `writeFile`).
- **Motion**: one `cx.timer.every(250)` that only calls `cx.notify()` when a
  walk starts or ends, a mood changes, or an agent comes or goes. Each
  Pokémon's 128 px column is absolutely positioned with
  `.transition("left", { duration: <walk time>, easing: "linear" })`, so the
  walk itself is native. Sprite frames are animated GIFs (`image()` plays
  them); bubbles use `.loop("opacity")` and `.frames()`.
- **Art, fetched at first use** into `~/.config/herdr-app/data/pokemon-agents/`
  (nothing Pokémon ships in the repo):
  - Sprites: `https://raw.githubusercontent.com/PMDCollab/SpriteCollab/master/sprite/<0025>/`
    `AnimData.xml`, `Walk-Anim.png`, `Idle-Anim.png`, `Sleep-Anim.png` (follow
    `<CopyOf>`: some Idle animations are copies of Walk). Sheets have one
    row per facing: 0 down, 1 down-right, 2 right, 6 left, 7 down-left.
    Cut `walkR` (row 2), `walkL` (6), `idleR` (1), `idleL` (7), `sleep` (0,
    or the last row if fewer) with ImageMagick:
    `magick sheet.png -crop <n·fw>x<fh>+0+<row·fh> +repage -crop <fw>x<fh> +repage -scale 200% -set delay '%[fx:t==0?13:t==1?17:…]' -set dispose Background -loop 0 out.gif`
    (durations are 1/60 s game frames, GIF delays 1/100 s). Then measure the
    visible box with `-coalesce -background none -flatten -format %@ info:`
    and store sizes and boxes in `meta.json`, written last as the "done" mark.
  - Picker icons: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vii/icons/<id>.png`,
    all 151 in one `curl --parallel` call, then one `magick mogrify -scale 200%`.
- **Programs it runs**: `curl`, `magick` (or ImageMagick 6's
  `convert` / `identify` / `mogrify`).

## Watch out

- **Network and programs**: the mod downloads from raw.githubusercontent.com
  and runs `curl` and ImageMagick. It writes only under
  `~/.config/herdr-app/data/pokemon-agents/`. Say so before installing.
- Don't draw an image before its file exists: render the Poké Ball until
  `loadSprite` resolves, so a missing file is never cached as broken.
- `init(props, cx)`'s first argument isn't the overlay's props; read
  `props()` to tell the picker from the strip.
- An agent can briefly have no `pane` when it appears: don't persist picks
  keyed by anything but a pane id, or that agent's Pokémon will change once
  the pane shows up.
- `transition("left")` animates from the last drawn position, so the
  element needs a stable `.id()` per agent, and a stop mid-walk must
  compute the current position (`from + (target − from) · progress`).
- Herdr's `done` becomes `idle` as soon as the tab is seen, so the `✓` is
  short-lived on the shown tab.
- Limits: 151 Pokémon; up to ~1 Pokémon per 128 px of width before they
  crowd (tags then hide). exec calls time out after 30 s; one sprite needs
  ~4 small downloads, and failures retry after a minute.
- Tested on Linux with ImageMagick 7 and Herdr app 0.1.12; macOS and Windows
  need `curl` and ImageMagick on PATH.

## Done when

- `herdr-app check mods/pokemon-agents` passes.
- With agents running, each one has a Pokémon in the bottom strip within a
  few seconds of first use (Poké Balls until the art is ready); a second start
  is instant (cached).
- A working agent walks left and right facing the way it moves; an idle one
  strolls rarely and, 3 minutes after its last change, sleeps with `zZz`.
- An agent waiting for permission stops and shows a pulsing `!`, and its
  name tag stays visible next to a crowd.
- Clicking a Pokémon shows its agent; right-clicking opens the picker with
  151 icons; searching "pika" leaves Pikachu, Enter or a click picks it, and
  the strip shows the new Pokémon. After restarting Herdr it is still there.
- `alt-shift-p` (with the `keys.json` snippet) opens the picker for the
  focused agent.
