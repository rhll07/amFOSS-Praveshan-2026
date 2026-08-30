t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    for i in range(1, n):
        if a[i - 1] > a[i]:
            a[i - 1], a[i] = a[i], a[i - 1] + a[i]

    print(a[-1])