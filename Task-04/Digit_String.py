t = int(input())

for _ in range(t):
    s = input().strip()
    pref2 = 0
    suf13 = sum(c == '1' or c == '3' for c in s)
    best = pref2 + suf13

    for c in s:
        if c == '2':
            pref2 += 1
        elif c == '1' or c == '3':
            suf13 -= 1

        best = max(best, pref2 + suf13)

    print(len(s) - best)