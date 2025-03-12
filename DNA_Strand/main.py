def longest_substrand(str1, str2):
    # Print input values
    print(f"Input: str1 = '{str1}', str2 = '{str2}'")
    
    smallest = str1 if len(str1) <= len(str2) else str2
    smallest_original = smallest
    biggest = str1 if smallest == str2 else str2
    
    smallest_length = len(smallest)
    biggest_length = len(biggest)
    
    print(f"smallest = '{smallest}', length = {smallest_length}")
    print(f"biggest = '{biggest}', length = {biggest_length}")
    
    while len(smallest) > 0:
        n = biggest_length // len(smallest)
        m = smallest_length // len(smallest)
        
        print(f"Current substring: '{smallest}', length = {len(smallest)}")
        print(f"n = {n}, m = {m}")
        print(f"smallest * n = '{smallest * n}'")
        print(f"smallest * m = '{smallest * m}'")
        print(f"Checking if '{smallest * n}' == '{biggest}' and '{smallest * m}' == '{smallest_original}'")
        
        if smallest * n == biggest and smallest * m == smallest_original:
            print(f"Found match! Returning: '{smallest}'")
            return smallest
        
        smallest = smallest[:-1]
        print(f"No match, reducing substring to: '{smallest}'")
    
    print("No common substrand found, returning empty string")
    return ''


# Test cases
def run_test_cases():
    print("\n=== Test Case 1 ===")
    result1 = longest_substrand('ATCATCATCATCATC', 'ATCATC')
    print(f"Result: '{result1}'")
    
    print("\n=== Test Case 2 ===")
    result2 = longest_substrand('CCCCCCCCC', 'CC')
    print(f"Result: '{result2}'")
    
    print("\n=== Test Case 3 ===")
    result3 = longest_substrand('ATAG', 'ATAGATAGATAGATAG')
    print(f"Result: '{result3}'")


# Run the tests
if __name__ == "__main__":
    run_test_cases() 