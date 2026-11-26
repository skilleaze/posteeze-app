# Posteeze

Posteeze is a rebranded build of [Postiz](https://github.com/gitroomhq/postiz-app) (AGPL-3.0).
This repository is its complete corresponding source, as the AGPL requires.

## Updating to a new upstream release

```bash
git remote add upstream https://github.com/gitroomhq/postiz-app.git
git fetch upstream --tags
git merge vX.Y.Z            # resolve conflicts by taking upstream, then:
python3 scripts/posteeze/rebrand.py
git commit -am "Rebrand vX.Y.Z as Posteeze"
```

`scripts/posteeze/rebrand.py` is idempotent. Brand assets live in `scripts/posteeze/assets`.

## Brand (Orbit)

| Token | Hex |
| --- | --- |
| Night | #121417 |
| Lime | #C6F432 |
| Moss | #7BA300 |
| Pale lime | #F3FCD6 |

Headings: Bricolage Grotesque. Text: Figtree.
