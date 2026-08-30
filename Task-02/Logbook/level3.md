# Level 3 - Wax Jungle

The Wax Jungle directory in the current timeline only contained `.gitkeep`,
so I checked the Git history for the directory.

```bash
git log --all --oneline -- GrandLine/Wax_Jungle
```

This revealed the Level 3 implementation commit:

```text
ee6f464 Level 3: Implemented
```

Instead of checking out all the reports, I searched the historical commit
directly:

```bash
git grep -ni 'SPLIT\|TIMELINE\|MISDIRECTION\|BAROQUE' ee6f464 -- GrandLine/Wax_Jungle
```

This led to:

```text
GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log
```

I inspected that file directly from the commit:

```bash
git show ee6f464:GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log
```

The report contained a security tag and the following Poneglyph fragment:

```text
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"
```

I also decoded the security tag and confirmed that it contained the
Level 2 clue:

```text
BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
```

The Poneglyph fragment is kept exactly as found because it is a fragment
that may be needed later in the voyage.

## Poneglyph Fragment I

`KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL`

## Screenshot

![Level 3](level3.png)