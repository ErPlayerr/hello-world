import math
import ast
import unittest


class Calculator:
    def __init__(self):
        self.result = None

    def calculate(self, expr):
        raise NotImplementedError("Subclasses must implement the calculate method.")

    def display_result(self):
        raise NotImplementedError("Subclasses must implement the display_result method.")


class BasicCalculator(Calculator):
    def calculate(self, expr):
        self.result = eval(expr)

    def display_result(self):
        return self.result


class ScientificCalculator(Calculator):
    def calculate(self, expr):
        self.result = eval(expr, {'__builtins__': None}, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan})

    def display_result(self):
        return self.result


class SmartCalculator(Calculator):
    def calculate(self, expr):
        try:
            parsed_expr = ast.parse(expr, mode='eval')
            if any(isinstance(node, (ast.Call, ast.Attribute)) for node in ast.walk(parsed_expr)):
                raise ValueError("Expression contains unsupported function calls or attributes")
            self.result = eval(expr)
        except (SyntaxError, ValueError):
            self.result = eval(expr, {'__builtins__': None}, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan})

    def display_result(self):
        if self.result is None:
            return "No result"
        return self.result


class CalculatorFactory(object):
    _instance = None

    @staticmethod
    def get_instance():
        if CalculatorFactory._instance is None:
            CalculatorFactory._instance = CalculatorFactory()
        return CalculatorFactory._instance

    @staticmethod
    def create_calculator(calctype):
        if calctype.lower() == "basic":
            return BasicCalculator()
        elif calctype.lower() == "scientific":
            return ScientificCalculator()
        elif calctype.lower() == "smart":
            return SmartCalculator()
        else:
            raise ValueError("Invalid calculator type")


class TestCalculators(unittest.TestCase):
    def test_basic_calculator(self):
        calc = BasicCalculator()
        calc.calculate('2 + 3')
        self.assertEqual(calc.display_result(), 5)

    def test_scientific_calculator(self):
        calc = ScientificCalculator()
        calc.calculate('sin(0)')
        self.assertEqual(calc.display_result(), 0)

    def test_smart_calculator(self):
        calc = SmartCalculator()
        calc.calculate('2 * 3')
        self.assertEqual(calc.display_result(), 6)

    def test_factory_method(self):
        factory = CalculatorFactory()
        calc = factory.create_calculator("basic")
        self.assertIsInstance(calc, BasicCalculator)

    def test_singleton_instance(self):
        factory1 = CalculatorFactory.get_instance()
        factory2 = CalculatorFactory.get_instance()
        self.assertIs(factory1, factory2)


if __name__ == '__main__':
    unittest.main()
