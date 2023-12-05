import unittest
import score

class TestScore(unittest.TestCase):
    def test_add(self):
        self.assertEqual(score.scorecalc(33,22,44,55),100)
    
    #max value inputs
    def test_minimum_values(self):
        self.assertEqual(score.scorecalc(0, 0, 0, 0), 0)

    #Arbitrary Values:
    def test_arbitrary_values(self):
        result = score.scorecalc(16, 11, 22, 28)
        self.assertIsInstance(result, int)
        self.assertNotEqual(result, 0) 

    # edge cases 
    def test_non_integer_values(self):
        # This will work if scorecalc can handle floats, otherwise, expect an error or different outcome.
        result = score.scorecalc(0.5, 0.5, 0.5, 0.5)
        self.assertIsInstance(result, int)  # Ensure the result is still an integer.

    #boundaries
    def test_boundary_values(self):
        result = score.scorecalc(32, 21, 43, 54)
        self.assertIsInstance(result, int)

    #return type
    def test_return_type(self):
        result = score.scorecalc(10, 10, 10, 10)
        self.assertIsInstance(result, int)

    #weights summation
    def test_weights_summation(self):
        self.assertEqual(score.scorecalc(33, 22, 44, 55), 100)

if __name__ == '__main__':
    unittest.main()