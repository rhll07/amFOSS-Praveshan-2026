# Level 2 - Whiskey Peak

The current `Whiskey_Peak` directory only contained `feast_manifest.txt`, so I
checked the Git history of the directory.

I found a previous commit:

```text
bc5aff3 Level 2: Implemented
```

Using `git show`, I found a hidden script that had existed in that commit:

```text
.baroque_works_cache/unlock_vault.sh
```

The script required the `AWAKENING_SIGNATURE` from Level 1, so I exported it:

```bash
export AWAKENING_SIGNATURE='ONE_PIECE{GITO_GITO_NO_AWAKENING}'
```

I restored the historical script and ran it. It generated two log files:

```text
marine_intercept.log
bounty_hunter_feed.log
```

The script itself suggested comparing them with `diff`, so I ran:

```bash
diff marine_intercept.log bounty_hunter_feed.log
```

The only difference was on line 42:

```text
42c42
< LOG_STREAM_ENTRY_SECURE_NODE_042_VALID
---
> BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
```

This revealed the Level 2 clue.

## Clue

`BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}`

## Screenshot

![Level 2](level2.png)