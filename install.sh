#!/usr/bin/env bash
# Idea to Orbit installer, for any Claude Code surface (terminal, VS Code, desktop) where
# `/plugin install` is not available. Copies the skills and the /orbit command into your
# Claude config folder and registers the session-start hook in its settings.json.
#
#   ./install.sh               install, or update to this copy (safe to run again)
#   ./install.sh --uninstall   remove exactly what it added; your own settings stay
#
# Config folder: $CLAUDE_CONFIG_DIR if set, else ~/.claude. Needs bash and Python 3 (for a
# safe settings.json merge). Nothing is changed unless every check passes first.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"
cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
home="$cfg/idea-to-orbit"
mode="${1:-install}"
marker=".idea-to-orbit"   # a file in every skill folder this installer put there

py=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import json" >/dev/null 2>&1; then py="$c"; break; fi
done
if [ -z "$py" ]; then
  echo "Stopped: Python 3 is needed to edit settings.json safely. Install it, or on Windows use install.ps1." >&2
  exit 1
fi

# A path Claude Code can run on every OS: C:/Users/... on Windows, /home/... elsewhere.
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s' "$1"; fi; }

skills() { for d in "$src"/skills/*/; do basename "$d"; done; }

# check | add <command> | remove. Our hook is the one whose statusMessage is ours; nothing else is touched.
settings() {
  "$py" - "$cfg/settings.json" "$@" <<'PY'
import json, os, sys
path, action = sys.argv[1], sys.argv[2]
arg = sys.argv[3] if len(sys.argv) > 3 else ""   # add: the hook command; remove: keys the installer created
MARK = "Idea to Orbit: reading the product state"
if not os.path.exists(path):
    if action != "add":
        sys.exit(0)
    s, raw = {}, ""
else:
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    try:
        s = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        sys.exit(f"Stopped: {path} is not valid JSON ({e}). Fix it first; nothing was changed.")
if not isinstance(s, dict) or not isinstance(s.get("hooks", {}), dict) \
        or not isinstance(s.get("hooks", {}).get("SessionStart", []), list):
    sys.exit(f"Stopped: {path} does not have the shape Claude Code expects (an object, with 'hooks' an object "
             "and 'hooks.SessionStart' a list). Fix it first; nothing was changed.")
if action == "check":
    sys.exit(0)
before = json.dumps(s, sort_keys=True)
created = [k for k, there in (("hooks", "hooks" in s), ("SessionStart", "SessionStart" in s.get("hooks", {}))) if not there]
hooks = s.setdefault("hooks", {})
groups = hooks.setdefault("SessionStart", [])
kept = []
for g in groups:  # drop our hook; drop a group only if it held nothing but ours
    if isinstance(g, dict) and isinstance(g.get("hooks"), list):
        rest = [h for h in g["hooks"] if not (isinstance(h, dict) and h.get("statusMessage") == MARK)]
        if not rest and len(rest) < len(g["hooks"]):
            continue
        g["hooks"] = rest
    kept.append(g)
groups[:] = kept
if action == "add":
    groups.append({"matcher": "startup|resume|clear|compact",
                   "hooks": [{"type": "command", "command": arg, "powershell": "& " + arg, "shell": "bash",
                             "timeout": 10, "statusMessage": MARK}]})
    print(" ".join(created))
else:
    mine = arg.split()  # keys this installer created: remove them again only if they are empty
    if not groups and "SessionStart" in mine:
        del hooks["SessionStart"]
    if not hooks and "hooks" in mine:
        del s["hooks"]
if json.dumps(s, sort_keys=True) == before:
    sys.exit(0)
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
}

# Every check before any change: settings.json must be readable, and no folder we would replace may be the owner's.
settings check
if [ "$mode" != "--uninstall" ]; then
  if [ -f "$cfg/commands/orbit.md" ] && ! { [ -f "$home/orbit.md" ] && cmp -s "$cfg/commands/orbit.md" "$home/orbit.md"; } \
      && ! cmp -s "$cfg/commands/orbit.md" "$src/commands/orbit.md"; then
    echo "Stopped: $cfg/commands/orbit.md is not from this installer (it may be yours). Rename or remove it first; nothing was changed." >&2
    exit 1
  fi
  for name in $(skills); do
    if [ -e "$cfg/skills/$name" ] && [ ! -f "$cfg/skills/$name/$marker" ]; then
      echo "Stopped: $cfg/skills/$name is not from this installer (it may be yours). Rename or remove it first; nothing was changed." >&2
      exit 1
    fi
  done
fi

if [ "$mode" = "--uninstall" ]; then
  settings remove "$(cat "$home/created-keys" 2>/dev/null || true)"
  for m in "$cfg"/skills/*/"$marker"; do if [ -f "$m" ]; then rm -rf "$(dirname "$m")"; fi; done
  if [ -f "$home/orbit.md" ] && cmp -s "$cfg/commands/orbit.md" "$home/orbit.md"; then rm -f "$cfg/commands/orbit.md"; fi
  rm -rf "$home"
  echo "Idea to Orbit removed from $cfg."
  exit 0
fi

mkdir -p "$cfg/skills" "$cfg/commands" "$home"
for m in "$cfg"/skills/*/"$marker"; do if [ -f "$m" ]; then rm -rf "$(dirname "$m")"; fi; done   # ours, from any version
for name in $(skills); do
  rm -rf "$cfg/skills/$name"
  cp -R "$src/skills/$name" "$cfg/skills/$name"
  printf 'Installed by Idea to Orbit. Remove with install.sh --uninstall.\n' > "$cfg/skills/$name/$marker"
done
cp "$src/commands/orbit.md" "$cfg/commands/orbit.md"
cp "$src/commands/orbit.md" "$home/orbit.md"
rm -rf "$home/hooks"
cp -R "$src/hooks" "$home/hooks"
chmod +x "$home/hooks/run.cmd" "$home/hooks/session-start" 2>/dev/null || true
created="$(settings add "\"$(native "$home/hooks/run.cmd")\" session-start")"
[ -f "$home/created-keys" ] || printf '%s\n' "$created" > "$home/created-keys"   # the first install knows what it created

echo "Idea to Orbit installed in $cfg: $(skills | wc -l | tr -d ' ') skills, /orbit and the session-start hook."
echo "Start a new Claude Code session and type /orbit."
