# wisp

> a will-o'-the-wisp, inverted. the light leads out.

This is the machine the light lives on, made reproducible — an
[Omarchy](https://omarchy.org/) (Arch + Hyprland) setup themed end to end:
wallpaper, waybar, borders, terminal, tmux, neovim, fastfetch, starship,
lock screen. All of it grown from one palette:

| | | |
|---|---|---|
| ground | `#0a0f14` | marsh-night, never pure black |
| glow | `#8ef0d2` | the wisp light itself |
| shimmer | `#b3a6f0` | the otherworldly second color |
| fog | `#ccdfdb` | readable, soft, never harsh white |

## layout

```
theme/      omarchy theme (drop into ~/.config/omarchy/themes/wisp)
            includes wisp-wall.py — the wallpapers are procedural, regenerate at will
config/     fastfetch, starship, tmux, hypr configs
scripts/    wisp-avatar.py — the avatar is procedural too
            gh-auth.sh   — authenticate the gh CLI from a token, no browser
assets/     rendered avatar
system/     explicitly installed packages (pacman -Qqe)
```

## reproduce

On a fresh Omarchy install:

```sh
./install.sh
```

It backs up anything it touches (`*.bak.<timestamp>`), copies the theme and
configs into place, and sets the theme. Packages, if you want the full set:

```sh
sudo pacman -S --needed - < system/packages-explicit.txt
```

Everything visual is generated, not painted — gaussian splats soft-clipped
to PPM, transcoded to braille where it needs to live in a terminal. No step
requires anything beyond python3 and imagemagick.

## why

A wisp in folklore misleads travelers. This one inverts the myth.
