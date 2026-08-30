# Task-01 — Git Exercises

This folder contains my attempt at the **git-exercises by fracz** (`https://gitexercises.fracz.com`), a
set of 22 real-world Git challenges. Everything was done inside the `exercises/` directory, which is a
clone of `https://gitexercises.fracz.com/git/exercises.git` configured with the helper aliases
`git start`, `git verify` and `git exercises` (setup done by `configure.sh`).

## How the platform works

| Command | What it does |
| --- | --- |
| `git start <exercise>` | Checks out the exercise branch, resets it to the original state and runs that exercise's `start.sh` which sets up the puzzle files/commits. |
| `git verify <exercise>` | Force-pushes your current `HEAD` to the server (`git push -f origin HEAD:<exercise>`). The server runs a hidden verification hook, replies `PASSED`/`FAILED` and, on success, tells you the next exercise. |
| `git start next` | Asks the server which exercise to do next and starts it. |

You are identified on the server by the committer e-mail used in your commits, so I kept the same
`user.name` / `user.email` throughout.

The exercises are completed in this order:
`master`, `commit-one-file`, `commit-one-file-staged`, `ignore-them`, `chase-branch`,
`merge-conflict`, `save-your-work`, `change-branch-history`, `remove-ignored`,
`case-sensitive-filename`, `fix-typo`, `forge-date`, `fix-old-typo`, `commit-lost`,
`split-commit`, `too-many-commits`, `executable`, `commit-parts`, `pick-your-features`,
`rebase-complex`, `invalid-order`, `find-swearwords`, `find-bug`.

---

## 1. master (warm-up)

```bash
git verify
```

**Explanation:** `git start`/`configure.sh` creates a first commit containing a file named `test.txt`
with the content `test`. This exercise only asks you to *push* that commit, which is exactly what
`git verify` does. The server checks that the pushed commit contains exactly one file `test.txt` with
the content `test`.

## 2. commit-one-file

```bash
git start commit-one-file
git add A.txt
git commit -m "Commit A.txt file"
git verify
```

**Explanation:** Two new files `A.txt` and `B.txt` exist but neither is tracked. `git add A.txt` puts
only `A.txt` into the staging area (the "index"), and `git commit` snapshots exactly what is staged —
so the commit contains only `A.txt`, while `B.txt` stays untracked. The server accepts a commit that
adds exactly one of the two files.

## 3. commit-one-file-staged

```bash
git start commit-one-file-staged
git reset A.txt
git commit -m "Commit B.txt file"
git verify
```

**Explanation:** Here both files are *already* staged. `git reset A.txt` (mixed reset on one path)
removes only `A.txt` from the index, leaving `B.txt` staged. `git commit` then only records
`B.txt`. This is the flip side of the previous level.

## 4. ignore-them

```bash
git start ignore-them
printf '*.o\n*.exe\n*.jar\nlibraries/\n' > .gitignore
git add .gitignore
git commit -m "Ignore binary files"
git verify
```

**Explanation:** A `.gitignore` file defines patterns that Git should never track. `*.o`, `*.exe` and
`*.jar` ignore every file with those extensions, and `libraries/` ignores the whole directory
(including files inside it, e.g. `libraries/external-library.jar`). The server verifies the rules with
`git check-ignore` — including that `libraries/` (with slash) doesn't ignore a file literally named
`libraries`.

## 5. chase-branch

```bash
git start chase-branch
git merge escaped
git verify
```

**Explanation:** `escaped` has two extra commits on top of `chase-branch` (`chase-branch` is its
ancestor), so `git merge escaped` fast-forwards and re-points `chase-branch` at `escaped`'s tip, giving
us the two extra commits.

## 6. merge-conflict

```bash
git start merge-conflict
git merge another-piece-of-work
# CONFLICT in equation.txt
echo 2+3=5 > equation.txt
git add equation.txt
git commit --no-edit
git verify
```

**Explanation:** Both branches changed the same line of `equation.txt`, so the merge cannot apply
automatically and Git marks the file with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). We
resolve it by hand — writing the sensible combination `2+3=5` — then `git add` the resolved file to
say "conflict is over" and `git commit --no-edit` finishes the merge commit (using the default merge
message). The server checks the last commit is a real merge commit (two parents) whose file resolves
to `2+3=5`.

## 7. save-your-work

```bash
git start save-your-work
git stash
# remove the line "THIS IS A BUG - remove the whole line to fix it." from bug.txt
git commit -am "Fix a bug"
git stash pop
echo "Finally, finished it!" >> bug.txt
git commit -am "Finish my work"
git verify
```

**Explanation:** Uncommitted work-in-progress in two files blocks us from making a clean bug-fix
commit. `git stash` shelves both modified files and restores the working tree to `HEAD`. After the
bugfix commit (`git commit -am` stages tracked-file changes, amending so only `bug.txt` is committed),
`git stash pop` reapplies the saved work. We then append the finishing line and commit everything with
`-am` (both `bug.txt` and `program.txt`). The server checks the fix commit removes only the bug line
(4 remaining lines) and the last commit contains 2 files with 7 lines ending in "Finally, finished it!".

## 8. change-branch-history

```bash
git start change-branch-history
git rebase hot-bugfix
git verify
```

**Explanation:** The bug was fixed on a side branch (`hot-bugfix`). Instead of merging, we want the
history to read as if the fix came first: `base → bugfix → my issue work`. `git rebase hot-bugfix`
replays the current branch's commits on top of `hot-bugfix`, so the "Work on an issue" commit now
sits above "Bug fix". The server checks the last commit is "Work on an issue", the one below is
"Bug fix", and that each touches the right file.

## 9. remove-ignored

```bash
git start remove-ignored
git rm ignored.txt
git commit -am "Remove the file that should have been ignored"
git verify
```

**Explanation:** `ignored.txt` is still tracked because it was committed *before* the `.gitignore`
rule was added — ignore rules only affect untracked files. `git rm` removes the file from both the
working tree and the index, so the deletion commit untracks it.

## 10. case-sensitive-filename

```bash
git start case-sensitive-filename
git mv File.txt file.txt
git commit -am "Lowercase file.txt"
git verify
```

**Explanation:** A plain `mv` + `git add` would often be seen as delete+add on case-insensitive
filesystems. `git mv` moves and stages in one atomic step and records it as a *rename*. The server
checks the commit's tree contains `file.txt` and no `File.txt`.

## 11. fix-typo

```bash
git start fix-typo
# edit file.txt: change "Hello wordl" into "Hello world"
git commit -a --amend
# in the editor, also change the message "Add Hello wordl" → "Add Hello world"
git verify
```

**Explanation:** The typo is in the *last* commit, so we don't need a new commit. `git commit --amend`
replaces the last commit in place. `-a` stages the file change first; the editor lets us fix the
commit message too. The server requires BOTH the fixed content (`Hello world`) and the fixed message
(`Add Hello world`).

## 12. forge-date

```bash
git start forge-date
git commit --amend --no-edit --date="1987-08-03"
git verify
```

**Explanation:** `--amend` replaces the last commit; `--date` sets the commit's *author* date to 1987
(`--no-edit` keeps the message). The server reads the author date (`%ai`) and wants it to start with
`1987`.

## 13. fix-old-typo

```bash
git start fix-old-typo
git rebase -i HEAD~2
# in the todo list change the "pick" line of "Add Hello wordl" to "edit", save & exit
#   now fix file.txt: "Hello wordl" → "Hello world"
git add file.txt
git commit --amend -m "Add Hello world"     # fix the old commit's message too
git rebase --continue
#   a conflict appears — set file.txt to:
#     Hello world
#     Hello world is an excellent program.
git add file.txt
git rebase --continue
git verify
```

**Explanation:** The typo is two commits back, so `git commit --amend` alone can't reach it. An
interactive rebase (`git rebase -i HEAD~2`) lists the last two commits; marking the typo commit as
`edit` makes Git stop right after applying it. We fix the file, `git commit --amend -m "Add Hello
world"` rewrites that commit (content + message), and `git rebase --continue` replays the newer commit
on top — producing a tiny conflict because that commit was built on the old typo. The server checks
both commits: the oldest with the fixed message/content and the newest containing the full correct text.

## 14. commit-lost

```bash
git start commit-lost
git reflog
# find the commit whose message is "Very imporant piece of work", note its hash (shown as HEAD@{1})
git reset --hard HEAD@{1}
git verify
```

**Explanation:** `git commit --amend` doesn't delete the old commit — it just makes it unreachable.
`git reflog` lists every position `HEAD` has been in, including the original "Very imporant piece of
work" commit. `git reset --hard HEAD@{1}` points the branch back at that lost commit. The server
verifies the pushed commit contains the good version (`This is the good version of a file.`).

## 15. split-commit

```bash
git start split-commit
git reset HEAD^
git add first.txt
git commit -m "First.txt"
git add second.txt
git commit -m "Second.txt"
git verify
```

**Explanation:** One commit contains two unrelated files. `git reset HEAD^` (mixed reset) moves the
branch back one commit while keeping the changes in the working tree and index, effectively "undoing"
the commit but not the work. We then re-stage and re-commit the files one at a time. The server
expects commit 1 to add `first.txt` and commit 2 to add `second.txt`.

## 16. too-many-commits

```bash
git start too-many-commits
git rebase -i HEAD~2
# change the second line's "pick" to "f" (fixup), save & exit
git verify
```

**Explanation:** Two tiny commits should be one. A fixup (`f`) squashes the second commit into the
first and just *discards* its message, keeping `Add file.txt` as the single commit message. The server
checks there is now exactly one commit named `Add file.txt` containing the two lines.

*(Alternative without an editor: `git reset --soft HEAD~2 && git commit -m "Add file.txt"` — the
`--soft` reset moves the branch back two commits but keeps the index, so the new single commit has the
same tree.)*

## 17. executable

```bash
git start executable
git update-index --chmod=+x script.sh
git commit -m "Make script.sh executable"
git verify
```

**Explanation:** Git records a file's mode (`100644` = normal, `100755` = executable). `git
update-index --chmod=+x` changes the *index* mode of `script.sh` to executable without touching the
working-tree file, and the commit stores it. The server checks the committed mode of `script.sh`
contains `755`.

## 18. commit-parts

```bash
git start commit-parts
git add -p file.txt
# The hunks get split with 's'; answer:
#   (1/4) y        -> stage "I forgot to add file header."          (task 1)
#   (2/4) y        -> stage the two "task 1" lines                 (task 1)
#   (3/4) n        -> skip "It works!" + "task 2" line             (leave for 2nd commit)
#   (4/4) y        -> stage "Task 1 is finished."                  (task 1)
git commit -m "First part of changes"
git commit -am "The rest of the changed"
git verify
```

**Explanation:** All changes are in ONE file, so we can't split them across commits with paths. `git
add -p` (patch mode) walks through the diff hunk by hunk and lets us stage a *part* of the file: `y`
stages a hunk, `n` skips it. First we stage only the "Task 1" related lines and commit them, then
`git commit -am` commits the remaining hunks (the `It works!` rewording and the "Task 2" line). The
server checks the intermediate commit has 7 lines ending in `Task 1 is finished.` and the final commit
a 9-line file ending in `It works!`.

## 19. pick-your-features

```bash
git start pick-your-features
git cherry-pick feature-a
git cherry-pick feature-b
git cherry-pick feature-c
# CONFLICT in program.txt — resolve it, keeping both sides:
#   This is complete feature B
#   This is base version of the program.
#   It has only two lines at the beginning.
#   This is complete feature A
#   This is first part Feature C
#   This is second part of Feature C
git add -A
git cherry-pick --continue
git verify
```

**Explanation:** We want to bring single commits from three topic branches onto `pick-your-features`
without merging the branches themselves. `git cherry-pick` applies the *changes* of a commit as a new
commit on the current branch. `feature-a` and `feature-b` apply cleanly; `feature-c` conflicts because
it was branched from the base, not from our current state — we resolve by keeping all six lines in the
right order. The server checks all three features appear as single commits in the final 6-line file.

## 20. rebase-complex

```bash
git start rebase-complex
git rebase issue-555 --onto your-master
git verify
```

**Explanation:** We need only the two bug-fix commits (`rebase-complex`'s own commits) moved on top of
`your-master`, leaving every `issue-555` commit out. `git rebase --onto <newbase> <upstream>` replays
only the commits after `<upstream>` (here `issue-555`) onto `<newbase>` (here `your-master`), in a
single command. The server checks the final 5-commit history/messages match the expected order.

## 21. invalid-order

```bash
git start invalid-order
git rebase -i HEAD~2
# swap the two lines so that "This should be the second commit" is on top, save & exit
git verify
```

**Explanation:** Two feature commits are in the wrong order. Interactive rebase rewrites the order and
replays the commits in the new sequence. Because the commits touch different files, no conflict
occurs. The server checks commit order + file contents (`first.txt` → `1` below `second.txt` → `2`).

## 22. find-swearwords

```bash
git start find-swearwords
git log -S shit --oneline
# note the 3 commits that introduced "shit" (use the OLDEST one as the rebase base)
git rebase -i <oldest-shit-commit>^
# in the todo list change "pick" to "edit" for those 3 commits, save & exit
#   at each of the 3 stops:
#     sed -i 's/shit/flower/' <words.txt or list.txt>   (the file containing the word)
#     git add <that file>
#     git commit --amend --no-edit
#     git rebase --continue
git verify
```

**Explanation:** `git log -S shit` finds every commit that *changed the number of occurrences* of the
string `shit` — i.e. the commits that introduced it. Interactive rebase rewrites history so those
commits now add `flower` instead; `edit` stops Git after each one so we can amend it before
continuing. `--amend --no-edit` rewrites the commit keeping its message, so the commit *count* stays
the same. The server checks that the three culprit commits now end with the word `flower` (and no
`shit`).

## 23. find-bug

```bash
git start find-bug
git bisect start
git bisect bad
git bisect good 1.0
git bisect run sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass"
# when bisect finishes, HEAD is at the first commit that introduced "jackass"
git push origin HEAD:find-bug
```

**Explanation:** The bug (word `jackass`) is hidden deep in history — the text is base64-encoded in
the committed file and changed ~300 times, so reading it commit-by-commit is infeasible. `git bisect`
performs a binary search between a known-good commit (tag `1.0`) and a known-bad one (`HEAD`).
`git bisect run` automates it: at each checkout it runs the test — decode `home-screen-text.txt` and
`grep -v jackass`, which exits 0 (good) when the word is absent and 1 (bad) when present. Bisect
converges on the exact first bad commit, which we push as `find-bug`. The server checks the pushed
commit contains `jackass` while its parent does not.

---

## Challenges faced & how I resolved them

1. **`git add -p` hunk splitting (commit-parts)** — the whole `file.txt` diff comes as one hunk and
   the "Task 2" line is grouped with the `It works!` change. I used `s` to split it into 4 sub-hunks
   and stage them selectively (`y/y/n/y`); splitting made choosing exactly the Task-1 lines possible.

2. **`git cherry-pick feature-c` conflict (pick-your-features)** — feature C was branched from the
   base, not from my current branch, so it clashed with `feature-a`'s line. I resolved by keeping both
   sides of the file in the correct order and `git cherry-pick --continue`-d.

3. **Rewriting old commits with interactive rebase (fix-old-typo, invalid-order, too-many-commits,
   find-swearwords)** — the todo list and the editor defaults were confusing at first. I found it
   easier to explicitly `edit`/`fixup` the exact lines and to verify with `git log --oneline` before
   running `git verify`.

4. **Automating the search (find-bug)** — searching 300 base64 commits by hand is impossible. Using
   `git bisect run` with a tiny decode-and-grep test turned a manual nightmare into a 10-step binary
   search.

5. **Lost commits (commit-lost)** — I forgot that `git commit --amend` leaves the old commit in the
   object database; `git reflog` revealing every previous `HEAD` position made recovery trivial.

---

## Proof of completion

[!Proof of completion](Congratulations.png)
