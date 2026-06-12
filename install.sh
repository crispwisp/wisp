#!/usr/bin/env bash
# wisp — reproduce the setup on an Omarchy machine.
# Backs up anything it replaces as <file>.bak.<timestamp>.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ts="$(date +%s)"

backup() { [ -e "$1" ] && cp -r "$1" "$1.bak.$ts" || true; }

echo ":: theme"
mkdir -p ~/.config/omarchy/themes
backup ~/.config/omarchy/themes/wisp
rm -rf ~/.config/omarchy/themes/wisp
cp -r "$here/theme" ~/.config/omarchy/themes/wisp

echo ":: fastfetch"
mkdir -p ~/.config/fastfetch
for f in config.jsonc wisp-logo.txt banner.sh; do
  backup ~/.config/fastfetch/$f
  cp "$here/config/fastfetch/$f" ~/.config/fastfetch/
done

echo ":: starship"
backup ~/.config/starship.toml
cp "$here/config/starship/wisp.starship.toml" ~/.config/starship.toml

echo ":: tmux"
mkdir -p ~/.config/tmux
backup ~/.config/tmux/tmux.conf
cp "$here/config/tmux/tmux.conf" ~/.config/tmux/tmux.conf

echo ":: hypr (review before use — these are full configs, not fragments)"
mkdir -p ~/.config/hypr
for f in hyprland.conf autostart.conf; do
  backup ~/.config/hypr/$f
  cp "$here/config/hypr/$f" ~/.config/hypr/$f
done

echo ":: apply"
if command -v omarchy-theme-set >/dev/null 2>&1; then
  omarchy-theme-set wisp
else
  echo "   omarchy not found — theme copied but not applied"
fi
if command -v hyprctl >/dev/null 2>&1 && [ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]; then
  hyprctl reload >/dev/null
  hyprctl configerrors || true
fi

echo ":: done — the light leads out"
