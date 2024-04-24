import math
import ast
import unittest


# Abstraction: Calculator class defines abstract methods for calculating expressions and displaying results.
class Calculator:
    def __init__(self):
        self.result = None

    def calculate(self, expr):
        raise NotImplementedError("Subclasses must implement the calculate method.")

    def display_result(self):
        raise NotImplementedError("Subclasses must implement the display_result method.")


# Polymorphism: Each calculator class implements the abstract methods of the Calculator class, allowing them to be
# used interchangeably.
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


# Inheritance: CalculatorFactory inherits from object.
class CalculatorFactory(object):
    _instance = None

    # Singleton: Ensures only one instance of the factory exists.
    @staticmethod
    def get_instance():
        if CalculatorFactory._instance is None:
            CalculatorFactory._instance = CalculatorFactory()
        return CalculatorFactory._instance

    # Factory Method: Creates calculator instances based on the provided type.
    @staticmethod
    def create_calculator(Calctype):
        if Calctype.lower() == "basic":
            return BasicCalculator()
        elif Calctype.lower() == "scientific":
            return ScientificCalculator()
        elif Calctype.lower() == "smart":
            return SmartCalculator()
        else:
            raise ValueError("Invalid calculator type")


# Unit tests: TestCalculators class defines unit tests for each calculator class.
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
