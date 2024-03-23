import re
import operator


class MathSkill:
    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

    def handle_math(self, text):
        expression = self.parse_expression(text)
        if expression:
            return self.calculate_expression(expression)
        else:
            return "Не удалось распознать математическое выражение."

    def parse_expression(self, text):
        expression = re.sub(r'[^0-9+\-*/.() ]', '', text)
        return expression.strip()

    def calculate_expression(self, expression):
        if not re.match(r'^[\d+\-*/.() ]+$', expression):
            return "Извините, я могу выполнять расчеты только с числами и арифметическими операторами."

        try:
            result = eval(expression, {'__builtins__': None}, self.operators)
            return f"Результат: {result}"
        except Exception as e:
            return f"Ошибка при вычислении выражения: {e}"
