# Level 1 - Loguetown

I started by checking the provided `eat.sh` script to understand how the
Devil Fruit was supposed to be found.

The important part was the executable check:

```bash
if [[ -x "$FRUIT" ]]
```

So instead of opening all the files one by one, I searched for executable
files using:

```bash
find . -type f -executable
```

This showed:

```text
./eat.sh
./sector_C/devil_fruit_6.txt
```

`eat.sh` was obviously the script itself, so the actual Devil Fruit was:

```text
sector_C/devil_fruit_6.txt
```

I then used the provided script to eat it:

```bash
./eat.sh sector_C/devil_fruit_6.txt
```

This revealed the awakening signature:

```text
ONE_PIECE{GITO_GITO_NO_AWAKENING}
```

## Flag

`ONE_PIECE{GITO_GITO_NO_AWAKENING}`

## Screenshot

![Level 1](level1.png)