import unittest

import validation_functions

class TestValidationFunctions(unittest.TestCase):

    def test_is_square__1(self):
        self.assertTrue(validation_functions.is_square(16))
        self.assertTrue(validation_functions.is_square(1444))
        self.assertTrue(validation_functions.is_square(444889))
        self.assertTrue(validation_functions.is_square(11122233444))
    
    def test_is_square__2(self):
        test_val = 17
        self.assertFalse(validation_functions.is_square(test_val))

    def test_is_1_more_than_palindrome__1(self):
        self.assertTrue(validation_functions.is_1_more_than_palindrome(102))
        self.assertTrue(validation_functions.is_1_more_than_palindrome(13332))
        self.assertTrue(validation_functions.is_1_more_than_palindrome(3444))

    def test_is_1_more_than_palindrome__2(self):
        self.assertFalse(validation_functions.is_1_more_than_palindrome(111))
    
    def test_is_1_less_than_palindrome__1(self):
        self.assertTrue(validation_functions.is_1_less_than_palindrome(100))
        self.assertTrue(validation_functions.is_1_less_than_palindrome(100))

    def test_is_1_less_than_palindrome__2(self):
        self.assertFalse(validation_functions.is_1_less_than_palindrome(111))

    def test_is_prime_raised_to_a_prime__1(self):
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(4))
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(8))
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(11))
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(22))
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(111))
        self.assertFalse(validation_functions.is_prime_raised_to_a_prime(41457661182))
    
    def test_is_prime_raised_to_a_prime__2(self):
        # 2211169 = 1487 ^ 2
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(2211169))
        # 823543 = 7^7
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(823543))
        # 844596301 = 61^5
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(844596301))
        # 41457661181 = 3461^3
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(41457661181))
        # 32 = 2^5
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(32)) 
        # 25 = 5^2
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(25))
        # 27 = 3^3
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(27))
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(1331))
        self.assertTrue(validation_functions.is_prime_raised_to_a_prime(734449))

    def test_is_sum_digits_7__1(self):
        self.assertTrue(validation_functions.is_sum_digits_7(16))
        self.assertTrue(validation_functions.is_sum_digits_7(115))
        self.assertTrue(validation_functions.is_sum_digits_7(151))
        self.assertTrue(validation_functions.is_sum_digits_7(502))
        self.assertTrue(validation_functions.is_sum_digits_7(133))
        self.assertTrue(validation_functions.is_sum_digits_7(100411))
    
    def test_is_sum_digits_7__2(self):
        self.assertFalse(validation_functions.is_sum_digits_7(187))

    def test_is_multiple_of_37__1(self):
        self.assertTrue(validation_functions.is_multiple_of_37(37))
        self.assertTrue(validation_functions.is_multiple_of_37(74444))
        self.assertTrue(validation_functions.is_multiple_of_37(74888))

    def test_is_multiple_of_37__2(self):
        self.assertFalse(validation_functions.is_multiple_of_37(36))
        self.assertFalse(validation_functions.is_multiple_of_37(388))
    
    def test_is_multiple_of_88__1(self):
        self.assertTrue(validation_functions.is_multiple_of_88(88))
        self.assertTrue(validation_functions.is_multiple_of_88(1144))
        self.assertTrue(validation_functions.is_multiple_of_88(79992))

    def test_is_multiple_of_88__2(self):
        self.assertFalse(validation_functions.is_multiple_of_88(388))
        self.assertFalse(validation_functions.is_multiple_of_88(85))

    def test_is_palindrome_multiple_of_23__1(self):
        self.assertTrue(validation_functions.is_palindrome_multiple_of_23(161))
        self.assertTrue(validation_functions.is_palindrome_multiple_of_23(7714177))
        self.assertTrue(validation_functions.is_palindrome_multiple_of_23(989))

    def test_is_palindrome_multiple_of_23__2(self):
        self.assertFalse(validation_functions.is_palindrome_multiple_of_23(232))

    def test_is_product_ends_in_1__1(self):
        self.assertFalse(validation_functions.is_product_ends_in_1(123))
    
    def test_is_product_ends_in_1__2(self):
        self.assertTrue(validation_functions.is_product_ends_in_1(7777))
        self.assertTrue(validation_functions.is_product_ends_in_1(77111779999))

    def test_is_fibonacci_num__1(self):
        self.assertTrue(validation_functions.is_fibonacci_num(13))
        self.assertTrue(validation_functions.is_fibonacci_num(21))
        self.assertTrue(validation_functions.is_fibonacci_num(144))
        self.assertTrue(validation_functions.is_fibonacci_num(4181))

    def test_is_fibonacci_num__2(self):
        self.assertFalse(validation_functions.is_fibonacci_num(22))

        for i in range(1_000_000_000):
            validation_functions.is_fibonacci_num(i)

    def test_is_palindrome_num__1(self):
        test_val = 121
        self.assertTrue(validation_functions.is_palindrome_num(test_val))
    
    def test_is_palindrome_num__2(self):
        test_val = 123
        self.assertFalse(validation_functions.is_palindrome_num(test_val))

    def test_is_prime_num__1(self):
        test_val = 2
        self.assertTrue(validation_functions.is_prime_num(test_val))

    def test_is_prime_num__2(self):
        test_val = 8
        self.assertFalse(validation_functions.is_prime_num(test_val))


if __name__ == '__main__':
    unittest.main()
