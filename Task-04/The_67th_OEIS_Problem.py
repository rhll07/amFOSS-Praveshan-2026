import sys

def primes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    return [i for i in range(2, n + 1) if sieve[i]]

t = int(input())
tests = [int(input()) for _ in range(t)]
p = primes(110000)

for n in tests:
    ans = [p[i] * p[i + 1] for i in range(n)]
    print(*ans)