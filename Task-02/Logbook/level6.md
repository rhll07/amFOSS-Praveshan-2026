# Level 6 - The Great Merge War at Laugh Tale

The decoded message from Level 5 led to the `Laugh-Tale-Merge-War`
repository.

The repository had two branches containing different versions of the same
Poneglyph fragments:

- `ancient_history`
- `pirate_king_path`

Both branches were based on the same initial history, but their versions of
the treasure files contained different parts of the inscription.

I compared both branches with their common ancestor:

```bash
git diff 34b8f9a..8835d14 -- .
git diff 34b8f9a..091591f -- .
```

The conflicting parts were:

```text
key_part_1.txt

ancient_history:     Line
pirate_king_path:    TheGrand
```

and:

```text
key_part_2.txt

ancient_history:     bers
pirate_king_path:    Remem
```

I merged the `pirate_king_path` branch into `ancient_history`:

```bash
git merge origin/pirate_king_path
```

This produced merge conflicts in both treasure files.

I resolved the conflicts by combining the complementary parts:

```text
TheGrand + Line = TheGrandLine

Remem + bers = Remembers
```

The completed inscription was therefore:

```text
TheGrandLine
Remembers
```

After resolving the conflicts, I committed the merge:

```bash
git add treasure/key_part_1.txt treasure/key_part_2.txt
git commit -m "Reconcile ancient histories"
```

The final password was:

```text
TheGrandLineRemembers
```

I entered this password into `victory.sh`:

```bash
./victory.sh
```

The repository accepted the restored history and revealed the final flag:

```text
FLAG{The_Grand_Line_Remembers_Your_Commit}
```

## Screenshot

![Level 6](level6.png)