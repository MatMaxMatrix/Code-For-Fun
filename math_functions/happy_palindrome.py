#%%
def is_palindrome_num(x):
    if type(x) is not int:
        return False
    if x < 0:
        return False
    s = str(x)
    return s == s[::-1]

def is_happy(n):
    if type(n) is not int or n <= 0:
        return False
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        sum_sq = 0
        temp = n
        while temp > 0:
            digit = temp % 10
            sum_sq += digit ** 2
            temp = temp // 10
        n = sum_sq
    return n == 1

def check_numbers(numbers):
    result = []
    for num in numbers:
        if type(num) is not int:
            result.append("Neither")
            continue
        pal = is_palindrome_num(num)
        happy = is_happy(num)
        if pal and happy:
            result.append("Both")
        elif pal:
            result.append("Palindrome only")
        elif happy:
            result.append("Happy only")
        else:
            result.append("Neither")
    return result

# Example usage:
input_numbers = [121, 19, 7, 2, 10, -121, True, 0, 1, '121']
print(check_numbers(input_numbers))
# Output: ['Both', 'Happy only', 'Happy only', 'Neither', 'Neither', 'Neither', 'Neither', 'Palindrome only', 'Both', 'Neither']

# %%
test_numbers = [121, 19, 7, 2, 10, -121, True, 0, 1, '121', 0, 1, 999999999999999999, -1] 
print(check_numbers(test_numbers)) 

# %%



#%%
def is_palindrome_num(x):
    if not isinstance(x, int) or isinstance(x, bool):
        return False
    if x < 0:
        return False
    s = str(x)
    return s == s[::-1]

def is_happy(n):
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        return False
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        sum_sq = 0
        temp = n
        while temp > 0:
            digit = temp % 10
            sum_sq += digit ** 2
            temp = temp // 10
        n = sum_sq
    return n == 1

def check_numbers(numbers):
    result = []
    for num in numbers:
        if not isinstance(num, int) or isinstance(num, bool):
            result.append("Neither")
            continue
        pal = is_palindrome_num(num)
        happy = is_happy(num)
        if pal and happy:
            result.append("Both")
        elif pal:
            result.append("Palindrome only")
        elif happy:
            result.append("Happy only")
        else:
            result.append("Neither")
    return result

test_numbers = [121, 19, 7, 2, 10, -121, True, 0, 1, '121', 0, 1, 999999999999999999, -1] 
print(check_numbers(test_numbers)) 

# %%





#%%
def è_palindromo_numero(x):
    if not isinstance(x, int) or isinstance(x, bool):
        return False
    if x < 0:
        return False
    s = str(x)
    return s == s[::-1]

def è_felice(n):
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        return False
    visitati = set()
    while n != 1 and n not in visitati:
        visitati.add(n)
        somma_quadrati = 0
        temporaneo = n
        while temporaneo > 0:
            cifra = temporaneo % 10
            somma_quadrati += cifra ** 2
            temporaneo = temporaneo // 10
        n = somma_quadrati
    return n == 1

def verifica_numeri(numeri):
    risultato = []
    for num in numeri:
        if not isinstance(num, int) or isinstance(num, bool):
            risultato.append("Nessuno")
            continue
        palindromo = è_palindromo_numero(num)
        felice = è_felice(num)
        if palindromo and felice:
            risultato.append("Entrambi")
        elif palindromo:
            risultato.append("Solo palindromo")
        elif felice:
            risultato.append("Solo felice")
        else:
            risultato.append("Nessuno")
    return risultato

numeri_test = [121, 19, 7, 2, 10, -121, True, 0, 1, '121', 0, 1, 999999999999999999, -1] 
print(verifica_numeri(numeri_test)) 

# %%









def è_palindromo_numero(x):
    if not isinstance(x, int) or isinstance(x, bool):
        raise ValueError("è_palindromo_numero: Il valore deve essere un intero (non boolean).")

    if x < -5 or x > 20:
        raise ValueError("è_palindromo_numero: Il valore deve essere compreso tra -5 e 20.")

    s = str(x)
    return s == s[::-1]

def è_felice(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("è_felice: Il valore deve essere un intero (non boolean).")

    if n < -5 or n > 20:
        raise ValueError("è_felice: Il valore deve essere compreso tra -5 e 20.")

    visitati = set()
    while n != 1 and n not in visitati:
        visitati.add(n)
        somma_quadrati = 0
        temporaneo = n
        while temporaneo > 0:
            cifra = temporaneo % 10
            somma_quadrati += cifra ** 2
            temporaneo = temporaneo // 10
        n = somma_quadrati
    return n == 1

def verifica_numeri(numeri):
    risultato = []
    for num in numeri:
        try:
            palindromo = è_palindromo_numero(num)
            felice = è_felice(num)
        except ValueError as e:
            risultato.append(f"Errore per {num}: {e}")
            continue

        if palindromo and felice:
            risultato.append("Entrambi")
        elif palindromo:
            risultato.append("Solo palindromo")
        elif felice:
            risultato.append("Solo felice")
        else:
            risultato.append("Nessuno")
    return risultato

# Test with the provided list
numeri_test = [121, 19, 7, 2, 10, -121, True, 0, 1, '121', 0, 1, 999999999999999999, -1]
print(verifica_numeri(numeri_test))
# %%
