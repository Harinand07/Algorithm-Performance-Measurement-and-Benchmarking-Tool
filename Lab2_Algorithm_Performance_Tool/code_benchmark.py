def single_loop(n):
    total=0
    for i in range(n): total += i
    return total, n

def nested_loop(n):
    total=0; operations=0
    for i in range(n):
        for j in range(n):
            total += 1; operations += 1
    return total, operations

def factorial_recursive(n):
    if n <= 1: return 1
    return n * factorial_recursive(n-1)

def factorial_iterative(n):
    result=1
    for i in range(2,n+1): result *= i
    return result
