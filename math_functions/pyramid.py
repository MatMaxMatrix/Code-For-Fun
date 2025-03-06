#%%
from typing import List  
import unittest  

# Code to test  
class Solution:  
    def maximumTotal(self, triangle: List[List[int]]) -> int:  
        # [Your provided code here]  
        if not (1 <= len(triangle) <= 80):  
            raise ValueError("Triangle must have between 1 and 200 rows")  
        if len(triangle[0]) != 1:  
            raise ValueError("First row must contain exactly one element")  
        for i in range(1, len(triangle)):  
            if len(triangle[i]) != len(triangle[i-1]) + 1:  
                raise ValueError("Each row must have one more element than the previous")  
        for row in triangle:  
            for num in row:  
                if not (-10**4 <= num <= 10**4):  
                    raise ValueError("All elements must be between -10^4 and 10^4")  
        for i in range(len(triangle) - 2, -1, -1):  
            for j in range(len(triangle[i])):  
                triangle[i][j] += max(triangle[i+1][j], triangle[i+1][j+1])  
        return triangle[0][0]  

# Generate unit tests for the `maximumTotal` function. Include:  
# 1. Normal scenarios (e.g., the sample input)  
# 2. Edge cases (e.g., single-row triangle, all negative values)  
# 3. Error cases (invalid triangle structure, out-of-bounds values)  
# Use Python's `unittest` framework. 
# 
triangle = [
    [1] * (i + 1) for i in range(81)
]
s = Solution()
print(s.maximumTotal(triangle))
#%%
class TestMaximumTotal(unittest.TestCase):  
    def test_sample_input(self):  
        sol = Solution()  
        self.assertEqual(sol.maximumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]), 21)  

    # Normal scenarios  
    def test_small_triangle(self):  
        sol = Solution()  
        self.assertEqual(sol.maximumTotal([[5], [2, 3]]), 5 + 3)  

    def test_negative_values(self):  
        sol = Solution()  
        self.assertEqual(sol.maximumTotal([[-1], [-2, -3], [-4, -5, -6]]), -1 + (-2) + (-4))  

    # Edge cases  
    def test_single_row(self):  
        sol = Solution()  
        self.assertEqual(sol.maximumTotal([[100]]), 100)  

    def test_max_row_size(self):  
        sol = Solution()  
        triangle = [[0] * (i + 1) for i in range(200)]  # Valid 200-row triangle  
        self.assertEqual(sol.maximumTotal(triangle), 0)  

    # Error cases  
    def test_invalid_row_length(self):  
        sol = Solution()  
        with self.assertRaises(ValueError):  
            sol.maximumTotal([[1], [2]])  # Second row should have 2 elements  

    def test_value_out_of_bounds(self):  
        sol = Solution()  
        with self.assertRaises(ValueError):  
            sol.maximumTotal([[10**4 + 1]])  # Exceeds upper bound  

    def test_empty_triangle(self):  
        sol = Solution()  
        with self.assertRaises(ValueError):  
            sol.maximumTotal([])  

    def test_non_increasing_row_size(self):  
        sol = Solution()  
        with self.assertRaises(ValueError):  
            sol.maximumTotal([[1], [2, 3], [4]])  # Third row breaks the rule  

if '__main__' == __name__:
    unittest.main()