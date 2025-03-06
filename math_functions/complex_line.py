#%%
import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
from math import pi

def complex_line(r, theta, num_points=100):
    """Copy of the function for reference"""
    if not isinstance(r, (int, float)) or r <= 1 or r >= 10:
        raise ValueError("r must be a positive number at range of 1 to 10")
    
    if not np.isfinite(theta):
        raise ValueError("theta must be a finite number")
        
    r_values = np.linspace(-r, r, num_points)
    real_parts = r_values * np.cos(theta)
    imaginary_parts = r_values * np.sin(theta)
    
    return real_parts, imaginary_parts

real, imag = complex_line(5, float('nan'))
print(real, imag)



# %%
