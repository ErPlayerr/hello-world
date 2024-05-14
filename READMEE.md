```markdown
# Design Patterns, SOLID Principles, and Other Usages

## Singleton Pattern
```python
class CalculatorFactory(object):
    _instance = None

    @staticmethod
    def get_instance():
        if CalculatorFactory._instance is None:
            CalculatorFactory._instance = CalculatorFactory()
        return CalculatorFactory._instance
```

## Factory Method Pattern
```python
class CalculatorFactory(object):

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
```

## SOLID Principles
### Single Responsibility Principle (SRP)
Each class has a single responsibility.

### Open/Closed Principle (OCP)
The code is open for extension but closed for modification.

### Liskov Substitution Principle (LSP)
Subclasses can be used interchangeably with the base class.

### Interface Segregation Principle (ISP)
The base class defines a clear interface without forcing subclasses to implement unnecessary methods.

### Dependency Inversion Principle (DIP)
Depends on abstractions rather than concrete implementations.

```python
# Each class definition follows SRP and other SOLID principles.
# Methods in Calculator classes follow the open/closed principle, allowing for extension without modification.
# Subclasses can be used interchangeably with the base class.
# Base class defines a clear interface for all subclasses without unnecessary methods.
# Factory class depends on abstractions (Calculator) rather than concrete implementations.
```

## Polymorphism
Implemented through method overriding in subclasses of `Calculator`.
```python
class BasicCalculator(Calculator):
    def calculate(self, expr):
        self.result = eval(expr)

    def display_result(self):
        return self.result

# Other subclasses and methods follow similar polymorphic behavior.
```

## Exception Handling
Used in the `SmartCalculator` class to handle errors in parsing expressions.
```python
class SmartCalculator(Calculator):
    def calculate(self, expr):
        try:
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
```

## Input/Output
User input for selecting calculator type and providing the equation to calculate is facilitated through standard input/output operations (`input` function).
```python
if __name__ == '__main__':
    # Prompt user for calculator type
    calculator_type = input("Select calculator (Basic, Scientific, Smart): ").strip()

    # Get singleton instance of CalculatorFactory
    factory = CalculatorFactory.get_instance()

    # Create calculator instance based on user input
    try:
        calculator = factory.create_calculator(calculator_type)
    except ValueError as e:
        print(e)
        exit()

    # Prompt user for expression
    expression = input("Enter the equation: ").strip()

    # Calculate and display result
    calculator.calculate(expression)
    print("Result:", calculator.display_result())
```
