# file: test_find_pair.py
#%%
def find_pair_with_target_sum(numbers, target):
    # Remove duplicates
    unique_numbers = set(numbers)
    unique_numbers = list(unique_numbers)
    
    # Dictionary to store index of elements in the original list
    index_map = {value: index for index, value in enumerate(numbers)}
    
    # Initialize result to keep track of valid pairs
    result = ()
    
    for i in range(len(unique_numbers)):
        for j in range(i + 1, len(unique_numbers)):
            if unique_numbers[i] + unique_numbers[j] == target:
                i_index = index_map[unique_numbers[i]]
                j_index = index_map[unique_numbers[j]]
                
                # Update result with the current pair based on conditions
                if not result or (result[0] < i_index) or (result[0] == i_index and result[1] < j_index):
                    result = (i_index, j_index)
                    
    return result

find_pair_with_target_sum([4, 3, 2, 4, 5, 6], 9)

# %%

# Test for logical case

# Test case where there is a clear pair adding up to the target

# Input list: [1, 2, 3, 4, 6], target: 10, expected result: (3, 4) as indices of numbers 4 and 6



def test_logical_case():

  assert find_pair_with_target_sum([1, 2, 3, 4, 6], 10) == (3, 4)



# Test for edge case

# Test case where multiple pairs could match but one has the highest index

# Input list: [1, 3, 2, 4, 5, 6], target: 9, expected result: (3, 4) as indices of numbers 4 and 5



def test_edge_case_multiple_pairs():

  assert find_pair_with_target_sum([1, 3, 2, 4, 5, 6], 9) == (1, 5)



# Test for edge case

# Test case where list contains duplicates

# Input list: [2, 2, 3, 3, 4, 4], target: 6, expected result: (1, 5) as indices of numbers 2 and 4



def test_edge_case_with_duplicates():

  assert find_pair_with_target_sum([2, 2, 3, 3, 4, 4], 6) == (1, 5)



# Test for edge case

# Test case where no pair adds up to the target

# Input list: [1, 2, 5, 9], target: 20, expected result: ()



def test_edge_case_no_pair():

  assert find_pair_with_target_sum([1, 2, 5, 9], 20) == ()



# Test for edge case

# Test case where smallest possible list is used

# Input list: [1, 2], target: 3, expected result: (0, 1) as indices of numbers 1 and 2



def test_edge_case_minimum_input():

  assert find_pair_with_target_sum([1, 2], 3) == (0, 1)



# Test for edge case

# Test case where list is empty

# Input list: [], target: 4, expected result: () as list is empty



def test_edge_case_empty_list():
  # Empty list
  # Input list: [], target: 4, expected result: () as list is empty

  assert find_pair_with_target_sum([], 4) == ()


def test_ties_for_highest_index():
    # Ties on highest index; prioritize second index
    # Input list: [1, 5, 5, 1], target: 6, expected result: (2, 3) as indices of numbers 5 and 5
    assert find_pair_with_target_sum([1, 5, 5, 1], 6) == (2, 3)

def test_negative_numbers():
    # Negative numbers
    # Input list: [-3, 7, 10], target: 4, expected result: (0, 1) as indices of numbers -3 and 7
    assert find_pair_with_target_sum([-3, 7, 10], 4) == (0, 1)

def test_large_list():
    # Large list
    # Input list: [1, 2, 3, ..., 10000], target: 19999, expected result: (9998, 9999) as indices of numbers
    assert find_pair_with_target_sum(list(range(1, 10001)), 19999) == (9998, 9999)

def test_no_pair_two_numbers():
    # No pair with two numbers
    # Input list: [1, 2], target: 5, expected result: () as no pair exists
    assert find_pair_with_target_sum([1, 2], 5) == ()

def test_all_same_numbers():
    # All same numbers
    # Input list: [5, 5, 5, 5], target: 10, expected result: () as no pair exists
    assert find_pair_with_target_sum([5, 5, 5, 5], 10) == ()