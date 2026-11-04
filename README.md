# herdr-pokemon-agents

A [Herdr](https://herdr.dev) mod: every agent is a pixel-art Pokémon (the first
151) roaming a strip at the bottom of the window. Working agents walk, idle ones
stroll and nap, blocked ones stop and call for you. Click a Pokémon to jump to
its agent, right-click to choose which Pokémon it is.

![Pokémon agents](preview.png)

## Install

Ask your agent: *"add the Herdr mod at github.com/mathieucroset/herdr-pokemon-agents"*.
Or by hand:

```sh
cp -r mods/pokemon-agents ~/.config/herdr-app/mods/
herdr-app check ~/.config/herdr-app/mods/pokemon-agents
```

Then put a `{ "type": "block", "content": { "mod": "pokemon-agents" }, "size": { "px": 112 } }`
at the bottom of your layout's main column (see [RECIPE.md](RECIPE.md)).
Optional key: merge [keys.json](keys.json) (`alt-shift-p` opens the picker).

Needs `curl` and [ImageMagick](https://imagemagick.org) on PATH.

## What it reaches

On first use the mod downloads sprites and icons from raw.githubusercontent.com
into `~/.config/herdr-app/data/pokemon-agents/` and cuts them into GIFs with
ImageMagick. It doesn't read anything else and sends nothing anywhere.

## Credits

- Sprites: [PMD SpriteCollab](https://github.com/PMDCollab/SpriteCollab) by the
  PMDCollab artists, CC BY-NC 4.0 (per-sprite credits in their repo). They are
  downloaded at run time, not shipped here.
- Menu icons: [PokeAPI/sprites](https://github.com/PokeAPI/sprites).
- Pokémon and all related names are trademarks of Nintendo, Creatures and
  GAME FREAK. This is an unofficial fan mod, not affiliated with them.
- `preview.png` is a mock-up drawn by `tools/make-preview.py`; agent names in it are made up.

Code: MIT.
