import math
import ast

class Calculator:
    def __init__(self):
        self.result = None

    def calculate(self, expr):
        raise NotImplementedError("implement the calculate method.")

    def display_result(self):
        raise NotImplementedError("implement display_result method.")


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
                raise ValueError("i dont support bro")
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


if __name__ == '__main__':
    calculator_type = input("Select calculator (Basic, Scientific, Smart): ").strip()

    factory = CalculatorFactory.get_instance()

    try:
        calculator = factory.create_calculator(calculator_type)
    except ValueError as e:
        print(e)
        exit()

    expression = input("Enter the equation: ").strip()

    calculator.calculate(expression)
    print("Result:", calculator.display_result())