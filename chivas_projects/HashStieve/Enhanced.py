def sieve(limit):

    if limit < 2:

        return []
    res = [False] * (limit + 1)
    res[2] = True
    res[3] = True

    i = 1

    while i <= limit:

        j = 1

        while j <= limit:



            n = (4 * i * i) + (j * j)
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                res[n] = not res[n]

            n = (3 * i * i) + (j * j)

            if n <= limit and n % 12 == 7:
                res[n] = not res[n]

            n = (3 * i * i) - (j * j)
            if i > j and n <= limit and n % 12 == 11:
                res[n] = not res[n]
            j += 1

        i += 1



    r = 5

    while r * r <= limit:

        if res[r]:
            for i in range(r * r, limit + 1, r):
                res[i] = False



        r += 1

    return res



def pick_prime(primes, min_size=1000):

    """returns a suitable prime to use as modulus"""
    for i in range(min_size, len(primes)):
        if primes[i]:
            return i
    for i in range(len(primes) - 1, -1, -1):
        if primes[i]:
            return i
    return 2  # Fallback to smallest prime if none found

def hash(string, modulus):
    """implements a polynomial hash of string keys"""
    hash_value = 0
    p = 31
    for char in string:
        hash_value = (hash_value * p + ord(char)) 
    return hash_value % modulus



if __name__ == '__main__':

    # generate primes list to use as modulus

    primes = sieve(10000) # modify limit based on your needs



    modulus = pick_prime(primes, 1000)



    test_array = ["alpha","beta","gamma","delta","epsilon"]



    for string in test_array:

        hash_value = hash(string, modulus)

        print(f"Hash of {string} is {hash_value}")