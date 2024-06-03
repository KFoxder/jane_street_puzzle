from functools import cache

@cache
def is_prime_num(num):
    """
    Returns True if num is a prime number
    """
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(limit):
    """Generate a list of prime numbers less than the given limit."""
    primes = []
    for num in range(2, limit):
        if is_prime_num(num):
            primes.append(num)
    return primes

primes = generate_primes(10_000)
prime_set = set(primes)

def generate_fibonacci(limit):
    """Generate a list of Fibonacci numbers less than the given limit."""
    fibonacci_numbers = [0, 1]
    while True:
        next_fib = fibonacci_numbers[-1] + fibonacci_numbers[-2]
        if next_fib >= limit:
            break
        fibonacci_numbers.append(next_fib)
    return fibonacci_numbers

fibonacci_numbers = generate_fibonacci(10**12)
fibonacci_set = set(fibonacci_numbers)

@cache
def is_square(num):
    """
    Returns True if num is a square number
    """
    return num >= 0 and (num ** 0.5).is_integer()

@cache
def is_1_more_than_palindrome(num):
    """
    Returns True if num is 1 more than a palindrome number
    """
    return is_palindrome_num(num - 1)

@cache
def is_1_less_than_palindrome(num):
    """
    Returns True if num is 1 less than a palindrome number
    """
    return is_palindrome_num(num + 1)

@cache
def is_prime_raised_to_a_prime(num):
    """
    Returns True if num is a prime number raised to a prime number
    """
    if num < 10:
        return False
    
    stop = int(num ** 0.5) + 1
    
    for prime in primes:
        if prime > stop:
            break
        root = num ** (1./prime)
        root_rounded = round(root, ndigits=10)
        if root_rounded in prime_set:
            return True
        
    return False

@cache
def is_sum_digits_7(num):
    """
    Returns True if the sum of the digits of num is 7
    """
    return sum(map(int, str(num))) == 7

@cache
def is_multiple_of_37(num):
    """
    Returns True if num is a multiple of 37
    """
    return num % 37 == 0
@cache
def is_multiple_of_88(num):
    """
    Returns True if num is a multiple of 88
    """
    return num % 88 == 0

@cache
def is_palindrome_multiple_of_23(num):
    """
    Returns True if num is a palindrome number and is a multiple of 23
    """
    return num % 23 == 0 and is_palindrome_num(num)

@cache
def is_product_ends_in_1(num):
    """
    Returns True if the product of the digits of num ends in 1
    """
    product = 1
    for digit in str(num):
        product *= int(digit)
    return product % 10 == 1

@cache
def is_fibonacci_num(num):
    """
    Returns True if num is a Fibonacci number
    """
    if num < 10:
        return False
    
    return num in fibonacci_set

@cache
def is_palindrome_num(num):
    return str(num) == str(num)[::-1]

@cache
def is_power_7(y, x=7):
    # The only power of 1
    # is 1 itself
    if (x == 1):
        return (y == 1)
         
    # Repeatedly compute
    # power of x
    pow = 1
    while (pow < y):
        pow = pow * x
 
    # Check if power of x
    # becomes y
    return (pow == y)

@cache
def multiple_of_5(num):
    return num % 5 == 0

@cache
def is_cube(num):
    """
    Returns True if num is a cube number
    """
    cube_root = num**(1./3.)
    if round(cube_root) ** 3 == num:
        return True
    else:
        return False
