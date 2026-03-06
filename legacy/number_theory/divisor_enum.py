def divisors(n):
    lower_divisors = []
    upper_divisors = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]

def divisors_from_factor(prime_factor:dict):
    divisors = [1]
    for base,exp in prime_factor.items():
        for i in range(len(divisors)):
            val = 1
            for _ in range(exp):
                val *= base
                divisors.append(divisors[i] * val)
    return sorted(divisors)