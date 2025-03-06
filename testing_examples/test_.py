
#%%
def sieve(limit):
    """Generate primes using the Sieve of Atkin."""
    if limit < 2:
        return []
    
    # Initialize the sieve
    res = [False] * (limit + 1)
    if limit >= 2:
        res[2] = True
    if limit >= 3:
        res[3] = True

    # Mark sieve with Atkin's conditions
    for x in range(1, int(limit**0.5) + 1):
        for y in range(1, int(limit**0.5) + 1):
            n = 4 * x * x + y * y
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                res[n] = not res[n]

            n = 3 * x * x + y * y
            if n <= limit and n % 12 == 7:
                res[n] = not res[n]

            n = 3 * x * x - y * y
            if x > y and n <= limit and n % 12 == 11:
                res[n] = not res[n]

    # Eliminate multiples of squares
    for r in range(5, int(limit**0.5) + 1):
        if res[r]:
            for k in range(r * r, limit + 1, r * r):
                res[k] = False

    # Collect prime numbers
    primes = [i for i, is_prime in enumerate(res) if is_prime]
    return primes


def pick_prime(primes, min_size=1000):
    """Return a suitable prime to use as modulus."""
    for prime in primes:
        if prime >= min_size:
            return prime
    # If no prime large enough exists, use the largest one
    return primes[-1]


def polynomial_hash(string, modulus):
    """Implements polynomial rolling of string keys."""
    hash_value = 5381
    for char in string:
        # hash = hash * 33 XOR ord(c)
        hash_value = ((hash_value << 5) + hash_value) ^ ord(char)
    return hash_value % modulus


if __name__ == '__main__':
    # Generate primes list to use as modulus
    primes = sieve(10000)  # Modify limit based on your needs

    # Pick a prime for the modulus
    modulus = pick_prime(primes, 1000)

    test_array = ["alpha", "beta", "gamma", "delta", "epsilon"]

    for string in test_array:
        hash_value = polynomial_hash(string, modulus)
        print(f"Hash of {string} is {hash_value}")

# %%
def sieve(limit):
    if limit < 2:
        return []
    
    res = [False] * (limit + 1)
    
    # Handle base cases
    if limit >= 2:
        res[2] = True
    if limit >= 3:
        res[3] = True

    # Main sieve loop
    for i in range(1, int(limit ** 0.5) + 1):
        for j in range(1, int(limit ** 0.5) + 1):
            # First quadratic using binary XOR to flip values
            n = (4 * i * i) + (j * j)
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                res[n] ^= True

            # Second quadratic
            n = (3 * i * i) + (j * j)
            if n <= limit and n % 12 == 7:
                res[n] ^= True

            # Third quadratic
            n = (3 * i * i) - (j * j)
            if i > j and n <= limit and n % 12 == 11:
                res[n] ^= True

    # Remove squares of primes and their multiples
    for r in range(5, int(limit ** 0.5) + 1):
        if res[r]:
            for i in range(r * r, limit + 1, r * r):
                res[i] = False

    # Convert boolean array to list of prime numbers
    primes = [i for i in range(len(res)) if res[i]]
    return primes

def pick_prime(primes, min_size=1000):
    """Returns a suitable prime to use as modulus"""
    for prime in primes:
        if prime >= min_size:
            return prime
    # if no prime large enough exists, use last one in list
    return primes[-1] if primes else min_size

def hash_string(string, modulus):
    """Implements polynomial rolling of string keys using DJB2 algorithm"""
    hash_value = 5381
    for char in string:
        # hash = 33 * hash XOR ord(c)
        hash_value = ((hash_value << 5) + hash_value) ^ ord(char)
    return hash_value % modulus

if __name__ == '__main__':
    # Generate primes list to use as modulus
    primes = sieve(10000)  # modify limit based on your needs
    
    modulus = pick_prime(primes, 1000)
    
    test_array = ["alpha", "beta", "gamma", "delta", "epsilon"]
    
    for string in test_array:
        hash_value = hash_string(string, modulus)
        print(f"Hash of {string} is {hash_value}")
# %%













def sieve(limit):
    if limit < 2:
        return []
    sieve_list = [False] * (limit + 1)
    if limit >= 2:
        sieve_list[2] = True
    if limit >= 3:
        sieve_list[3] = True

    i = 1
    while i * i <= int(limit**0.5) + 1:
        j = 1
        while j * j <= int(limit**0.5) + 1:
            n = (4 * i * i) + (j * j)
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                sieve_list[n] ^= True
            n = (3 * i * i) + (j * j)
            if n <= limit and n % 12 == 7:
                sieve_list[n] ^= True
            n = (3 * i * i) - (j * j)
            if i > j and n <= limit and n % 12 == 11:
                sieve_list[n] ^= True
            j += 1
        i += 1

    r = 2
    while r * r <= int(limit**0.5) + 1:
        if sieve_list[r]:
            for i in range(r * r, limit + 1, r * r):
                sieve_list[i] = False
        r += 1
    return sieve_list

def pick_prime(primes_list, min_size=1000):
    """Returns a suitable prime to use as modulus"""
    for prime in primes_list:
        if prime >= min_size:
            return prime
    return primes_list[-1]

def hash(string, modulus):
    """Implements polynomial rolling hash for string keys"""
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % modulus

if __name__ == '__main__':
    sieve_result = sieve(10000)
    primes_list = [i for i, is_prime in enumerate(sieve_result) if is_prime]
    modulus = pick_prime(primes_list, 1000)
    
    test_array = ["alpha", "beta", "gamma", "delta", "epsilon"]
    
    for string in test_array:
        hash_value = hash(string, modulus)
        print(f"Hash of {string} is {hash_value}")
# %%
def sieve(limit):
    if limit < 2:
        return []
    res = [False] * (limit + 1)
    if limit >= 2:
        res[2] = True
    if limit >= 3:
        res[3] = True

    i = 1
    while i * i <= int(limit**0.5) + 1:
        j = 1
        while j * j <= int(limit**0.5) + 1:
            n = (4 * i * i) + (j * j)
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                res[n] ^= True
            n = (3 * i * i) + (j * j)
            if n <= limit and n % 12 == 7:
                res[n] ^= True
            n = (3 * i * i) - (j * j)
            if i > j and n <= limit and n % 12 == 11:
                res[n] ^= True
            j += 1
        i += 1

    r = 2
    while r * r <= int(limit**0.5) + 1:
        if res[r]:
            for i in range(r * r, limit + 1, r * r):
                res[i] = False
        r += 1
    return res

def pick_prime(primes_list, min_size=1000):
    """Returns a suitable prime to use as modulus"""
    for prime in primes_list:
        if prime >= min_size:
            return prime
    return primes_list[-1]

def hash(string, modulus):
    """Implements polynomial rolling hash for string keys"""
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % modulus

if __name__ == '__main__':
    sieve_result = sieve(10000)
    primes_list = [i for i, is_prime in enumerate(sieve_result) if is_prime]
    modulus = pick_prime(primes_list, 1000)
    
    test_array = ["alpha", "beta", "gamma", "delta", "epsilon"]
    
    for string in test_array:
        hash_value = hash(string, modulus)
        print(f"Hash of {string} is {hash_value}")
# %%



def linear_least_squares(X, Y):
    """
    Compute the slope and y-intercept of a linear regression line using the least squares method.
    
    Args:
        X (list): Independent variables, values must be in range [0, 10]
        Y (list): Dependent variables, values must be in range [0, 10]
    
    Returns:
        tuple: (slope, y-intercept) of the best-fit line
        
    Raises:
        ValueError: If X and Y have different lengths, or if any value is out of range [0, 10]
        ZeroDivisionError: If denominator in slope calculation is zero
    """
    # Input validation: Check lengths
    if len(X) != len(Y):
        raise ValueError("X and Y must have the same length")
    
    # Input validation: Check value ranges
    for x, y in zip(X, Y):
        if not (0 <= x <= 10 and 0 <= y <= 10):
            raise ValueError("All values must be within range [0, 10]")
    
    n = len(X)
    
    # Calculate sums needed for least squares formulas
    sum_x = sum(X)
    sum_y = sum(Y)
    sum_xy = sum(x * y for x, y in zip(X, Y))
    sum_x_squared = sum(x * x for x in X)
    
    # Calculate denominator for slope
    denominator = n * sum_x_squared - sum_x * sum_x
    
    # Check for zero denominator
    if denominator == 0:
        raise ZeroDivisionError("Denominator in slope calculation is zero (vertical line or identical X values)")
    
    # Calculate slope (m) using least squares formula
    m = (n * sum_xy - sum_x * sum_y) / denominator
    
    # Calculate y-intercept (b) using least squares formula
    b = (sum_y - m * sum_x) / n
    
    return m, b


# Example usage and testing
if __name__ == "__main__":
    # Test case 1: Basic example
    X1 = [1, 2, 3, 4, 5]
    Y1 = [2, 4, 5, 4, 6]
    try:
        m1, b1 = linear_least_squares(X1, Y1)
        print(f"Test 1 - Slope: {m1:.2f}, Intercept: {b1:.2f}")
    except Exception as e:
        print(f"Test 1 failed: {str(e)}")
    
    # Test case 2: Values out of range
    X2 = [1, 2, 11, 4, 5]
    Y2 = [2, 4, 5, 4, 6]
    try:
        m2, b2 = linear_least_squares(X2, Y2)
        print(f"Test 2 - Slope: {m2:.2f}, Intercept: {b2:.2f}")
    except Exception as e:
        print(f"Test 2 failed: {str(e)}")
    
    # Test case 3: Different lengths
    X3 = [1, 2, 3]
    Y3 = [2, 4, 5, 4, 6]
    try:
        m3, b3 = linear_least_squares(X3, Y3)
        print(f"Test 3 - Slope: {m3:.2f}, Intercept: {b3:.2f}")
    except Exception as e:
        print(f"Test 3 failed: {str(e)}")
    
    # Test case 4: Vertical line (identical X values)
    X4 = [2, 2, 2, 2, 2]
    Y4 = [1, 2, 3, 4, 5]
    try:
        m4, b4 = linear_least_squares(X4, Y4)
        print(f"Test 4 - Slope: {m4:.2f}, Intercept: {b4:.2f}")
    except Exception as e:
        print(f"Test 4 failed: {str(e)}")

# %%
