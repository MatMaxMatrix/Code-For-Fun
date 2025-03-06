import unittest

def linear_estim(X, Y):
    if len(X) != len(Y):
        raise ValueError("X e Y devono avere la stessa lunghezza")
    
    for x, y in zip(X, Y):
        if not (0 <= x <= 10 and -10 <= y <= 0):
            raise ValueError("X deve essere compreso in [0, 10] e Y in [-10, 0]")
    
    n = len(X)
    sum_x = sum(X)
    sum_y = sum(Y)
    sum_xy = sum(x * y for x, y in zip(X, Y))
    sum_x_squared = sum(x ** 2 for x in X)
    
    denominator = n * sum_x_squared + sum_x ** 2
    if denominator == 0:
        raise ZeroDivisionError("Denominatore pari a zero (X contiene valori identici)")
    
    m = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / n
    return m, b

class TestLinearEstim(unittest.TestCase):

    def test_basic_functionality(self):
        X = [1, 2, 4, 6, 8]
        Y = [-2, -4, -5, -7, -9]
        m, b = linear_estim(X, Y)
        self.assertAlmostEqual(m, -0.93, places=2)
        self.assertAlmostEqual(b, -1.48, places=2)

    def test_same_length_input(self):
        X = [1, 2, 3]
        Y = [-1, -2, -3]
        try:
            linear_estim(X, Y)
        except ValueError as e:
            self.fail("linear_estim sollevato un ValueError inesperato: " + str(e))

    def test_different_length_input(self):
        X = [1, 2, 3]
        Y = [-1, -2]
        with self.assertRaises(ValueError):
            linear_estim(X, Y)

    def test_invalid_X(self):
        X = [5, 11, 2]  # 11 non è compreso tra [0, 10]
        Y = [-1, -2, -3]
        with self.assertRaises(ValueError):
            linear_estim(X, Y)

    def test_invalid_Y(self):
        X = [2, 5, 7]
        Y = [-1, -12, -3]  # -12 non è compreso in [-10, 0]
        with self.assertRaises(ValueError):
            linear_estim(X, Y)

    def test_identical_x_values(self):
        X = [5, 5, 5]  # Valori identici di X
        Y = [-2, -4, -6]
        with self.assertRaises(ZeroDivisionError):
            linear_estim(X, Y)

    def test_extreme_values(self):
        X = [0, 10]
        Y = [-10, -0]
        m, b = linear_estim(X, Y)
        self.assertAlmostEqual(m, 1, places=2)
        self.assertAlmostEqual(b, -10, places=2)

if __name__ == '__main__':
    unittest.main()
