#!/usr/bin/env bash
# Copies each skill in shared-skills/ to the repos shared-skills/TARGETS names.
#   scripts/sync-shared-skills.sh          copy, then list what changed
#   scripts/sync-shared-skills.sh --check  only report drift; exit 1 if any
set -euo pipefail
home="$(cd "$(dirname "$0")/.." && pwd)"
check=false; [[ "${1:-}" == "--check" ]] && check=true
drift=0
while read -r repo skills; do
  [[ -z "$repo" || "$repo" == \#* ]] && continue
  dir="$(cd "$home" && cd "$repo" 2>/dev/null && pwd)" || { echo "skip $repo: not cloned"; continue; }
  for s in $skills; do
    src="$home/shared-skills/$s"; dst="$dir/.claude/skills/$s"
    if diff -rq "$src" "$dst" >/dev/null 2>&1; then continue; fi
    drift=1
    if $check; then echo "drift: $repo/.claude/skills/$s"; else
      rm -rf "${dst:?}"; mkdir -p "$(dirname "$dst")"; cp -R "$src" "$dst"; echo "synced: $repo/.claude/skills/$s"; fi
  done
done < "$home/shared-skills/TARGETS"
$check && exit $drift || exit 0
