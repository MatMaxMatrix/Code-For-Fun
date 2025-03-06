#%%

from typing import List

class JumpInput:
    def __init__(self, nums: List[int]):
        if not (1 <= len(nums) <= 20):
            raise ValueError("La lunghezza di nums deve essere tra 1 e 20.")
        if not all(0 <= num <= 5 for num in nums):
            raise ValueError("Tutti gli elementi di nums devono essere tra 0 e 5.")
        self.nums = nums

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        val = 0
        for i in nums:
            if val < 0:
                return False
            elif i > val:
                val = i
            val -= 1
        return True

# Funzione per eseguire i test
def run_tests():
    test_cases = [
        ([6, 1, 2], ValueError),
        ([1], True),  # Un singolo elemento, quindi è sempre True
        ([0], True),  # Arrivo all'indice 0
        ([0, 0], False),  # Non può saltare oltre il primo indice
        ([2, 3, 1, 1, 4], True),  # Posso saltare all'ultimo indice
        ([3, 2, 1, 0, 4], False),  # Non posso raggiungere l'ultimo indice
        ([1, 0, 0], False),  # C'è un ostacolo
        ([1, 2, 0, 0], False),  # C'è un ostacolo
        ([2, 5, 0, 0], True),  # Posso saltare oltre l'ostacolo
        ([5, 4, 3, 2, 1, 0], True),  # Posso saltare direttamente all'ultimo indice
        ([4, 0, 0, 0, 0], True),  # Posso saltare fino all'ultimo indice
        ([3, 2, 5, 0, 0, 1], True),  # Posso saltare fino all'ultimo indice
        ([1, 2, 3, 4, 5], True),  # Sempre possibile
        ([1, 2, 3, 0, 5], False),  # C'è un ostacolo
        ([4, 1, 1, 1, 1, 1], True),  # Posso saltare oltre
        ([0, 2, 3], False),  # Non posso muovermi
        # Valori fuori dall'intervallo 0-5
        ([-1, 2, 3], ValueError),  # Valore negativo
        ([6, 1, 2], ValueError),   # Valore > 5
        # Lunghezze array non valide
        ([], ValueError),           # Array vuoto
        ([1] * 21, ValueError),     # Array troppo lungo
    ]

    for index, (nums, expected) in enumerate(test_cases):
        try:
            input_data = JumpInput(nums)
            solution = Solution()
            result = solution.canJump(input_data.nums)
            assert result == expected, f"Test {index + 1} fallito: atteso {expected}, ottenuto {result}"
            print(f"Test {index + 1}: passato")
        except ValueError as e:
            print(f"Test {index + 1}: errore di validazione - {e}")

# Eseguire i test
run_tests()
# %%


