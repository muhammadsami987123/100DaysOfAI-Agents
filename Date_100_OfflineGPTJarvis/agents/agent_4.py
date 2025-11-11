# agent_4.py - MathSolverAgent

import operator

class MathSolverAgent:
    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            'plus': operator.add,
            'minus': operator.sub,
            'times': operator.mul,
            'divided by': operator.truediv
        }

    def solve(self, expression):
        try:
            # A very basic and unsafe parser. 
            # In a real application, you would want to use a more robust and secure parsing library.
            parts = expression.split()
            if len(parts) != 3:
                return "Invalid expression. Please use the format: number operator number"

            num1 = float(parts[0])
            op_str = parts[1]
            num2 = float(parts[2])

            if op_str not in self.operators:
                return f"Unsupported operator: {op_str}"

            op_func = self.operators[op_str]
            result = op_func(num1, num2)
            return f"The result of {expression} is {result}"

        except ValueError:
            return "Invalid number in the expression."
        except ZeroDivisionError:
            return "Cannot divide by zero."
        except Exception as e:
            return f"An error occurred: {e}"
