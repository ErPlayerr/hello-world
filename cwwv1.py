import math
import ast


class Calculator:
    def __init__(self):
        self.result = None

    def calculate(self, expr):
        # Abstract method for calculating expressions, to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement the calculate method.")

    def display_result(self):
        # Abstract method for displaying the result, to be implemented by subclasses
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
            # Try parsing the expression
            parsed_expr = ast.parse(expr, mode='eval')

            # Check if the parsed expression contains any dangerous nodes
            if any(isinstance(node, (ast.Call, ast.Attribute)) for node in ast.walk(parsed_expr)):
                # If so, raise an error
                raise ValueError("Expression contains unsupported function calls or attributes")

            # Evaluate the parsed expression
            self.result = eval(expr)

        except (SyntaxError, ValueError):
            # If an error occurs, fallback to ScientificCalculator
            self.result = eval(expr, {'__builtins__': None}, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan})

    def display_result(self):
        if self.result is None:
            return "No result"
        return self.result


def create_calculator(calculator_type):
    if calculator_type.lower() == "Basic" or "basic" in calculator_type.lower():
        return BasicCalculator()
    elif calculator_type.lower() == "Scientific" or "scientific" in calculator_type.lower():
        return ScientificCalculator()
    elif calculator_type.lower() == "Smart" or "smart" in calculator_type.lower():
        return SmartCalculator()
    else:
        raise ValueError("Invalid calculator type use without caps")


class CalculatorFactory:
    _instance = None

    @staticmethod
    def get_instance():
        if CalculatorFactory._instance is None:
            CalculatorFactory._instance = CalculatorFactory()
        return CalculatorFactory._instance


# Prompt user for calculator type
calculator_type = input("select calculator(Basic, Scientific, Smart): ").strip()

# Get singleton instance of CalculatorFactory
factory = CalculatorFactory

# Create calculator instance based on user input
try:
    calculator = factory.create_calculator(calculator_type)
except ValueError as e:
    print(e)
    exit()

# Prompt user for expression
expression = input("Give the equation: ").strip()

# Calculate and display result
calculator.calculate(expression)
print("Answer:", calculator.display_result())
