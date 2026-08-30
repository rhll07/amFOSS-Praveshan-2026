t = int(input())

for _ in range(t):
    n, c = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    diff = sum(a) - sum(b)

    if all(x >= y for x, y in zip(a, b)):
        print(diff)
        continue

    a.sort()
    b.sort()

    if all(x >= y for x, y in zip(a, b)):
        print(diff + c)
    else:
        print(-1)