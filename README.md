# home-repo

Marcin's home repo, after [the Home Repo pattern](https://www.aihero.dev/the-home-repo-pattern): start agent sessions here, and they reach portfolio, Perron and Mylder from it. See [AGENTS.md](AGENTS.md).

## Local layout

The other repos are cloned inside this one, under `repos/`, which git ignores:

```
~/home-repo/
  AGENTS.md
  repos/
    portfolio/
    perron/
    mylder/
```

Missing repos are cloned there by the agent on first use.
