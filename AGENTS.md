# Home

Marcin's home repo. Agent sessions start here and work in the repos below. This repo holds what every repo shares: the cross-repo rules, the wiki, planning skills and the shared skill copies.

## Other repos

Each is cloned inside this repo, under `repos/` (gitignored). If one is missing, clone it there. For parallel tasks in one repo, use a git worktree inside that clone.

- Portfolio (Next.js site, www.marcinsieradzki.com): `repos/portfolio`. Clone from https://github.com/marcin-sieradzki/portfolio if missing.
- Perron (design system, published as `@mylder/perron`, perron.marcinsieradzki.com): `repos/perron`. Clone from https://github.com/marcin-sieradzki/perron if missing. Read its CLAUDE.md before changing it.
- Mylder (live map of Copenhagen transit, mylder.marcinsieradzki.com): `repos/mylder`. Clone from https://github.com/marcin-sieradzki/mylder if missing. Read its CLAUDE.md before changing it.

How they relate, and what each runs on: [wiki/repos.md](wiki/repos.md).

## Across repos

- Never merge a PR without Marcin's go-ahead: main deploys to production in all three.
- Mylder's CI fails on session links: no `Claude-Session:` line in commits, and no `claude.ai/code/session_` link or "Generated with Claude Code" footer in PR bodies. See [wiki/github-and-ci.md](wiki/github-and-ci.md).
- A Perron change reaches Mylder only after a Perron release and a version bump in Mylder.
- Full test suites and long builds run on Marcin's computer, not in the cloud. See [wiki/testing.md](wiki/testing.md).
- Each repo's own CLAUDE.md, checks and skills win inside that repo.

## Skills

- `.claude/skills/` holds the skills for work that starts here: `/grill-me`, `/grill-with-docs` (also writes a glossary and ADRs), `/wayfinder`, `/prototype`, `/research`, `domain-modeling`, `writing-for-agents`.
- `shared-skills/` holds the one master copy of each skill that several repos carry. Edit a shared skill there, never in a repo, then run `scripts/sync-shared-skills.sh` and open a PR in each repo it changed. `shared-skills/TARGETS` says which repo gets which skill.
- Skills and this file: write them with the `writing-for-agents` skill.
