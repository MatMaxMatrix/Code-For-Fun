from Initiating_agent import find_pair_with_target_sum

def test_logical_case():
    assert find_pair_with_target_sum([1, 2, 3, 4, 6], 10) == (3, 4)

def test_edge_case_multiple_pairs():
    assert find_pair_with_target_sum([1, 3, 2, 4, 5, 6], 9) == (3, 4)

def test_edge_case_with_duplicates():
    assert find_pair_with_target_sum([2, 2, 3, 3, 4, 4], 6) == (1, 5)

def test_edge_case_no_pair():
    assert find_pair_with_target_sum([1, 2, 5, 9], 20) == ()

def test_edge_case_minimum_input():
    assert find_pair_with_target_sum([1, 2], 3) == (0, 1)

def test_edge_case_empty_list():
    assert find_pair_with_target_sum([], 4) == ()