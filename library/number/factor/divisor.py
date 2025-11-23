def enumerate_divisors(n: int) -> list[int]:
    """nの約数を昇順に列挙"""
    lower_divisors = []
    upper_divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n // i)
        i += 1
    return lower_divisors + upper_divisors[::-1]


def enumerate_divisors_from_factor(prime_factor: dict[int, int]) -> list[int]:
    """素因数から約数を列挙"""
    divisors = [1]
    for radix, exp in prime_factor.items():
        for d in divisors[:]: #appendしていくのでコピーから取り出している
            val = 1
            for _ in range(exp):
                val *= radix
                divisors.append(d * val)
    return sorted(divisors)