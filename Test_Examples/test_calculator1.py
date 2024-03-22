# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    @classmethod
    def setup_class(cls):
        """Setup that runs once before executing any tests in the class."""
        cls.calculator = Calculator()

    def test_add(self):
        assert self.calculator.add(2, 3) == 5

    def test_subtract(self):
        assert self.calculator.subtract(5, 2) == 3

    def test_multiply(self):
        assert self.calculator.multiply(3, 4) == 12

    def test_divide(self):
        assert self.calculator.divide(10, 2) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            self.calculator.divide(5, 0)

if __name__ == '__main__':
    pytest.main()
