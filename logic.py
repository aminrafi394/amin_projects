# logic.py
import random

class MathQuiz:
    def __init__(self):
        self.operators = ["+", "-", "*", "/"]
        self.correct_count = 0
        self.wrong_count = 0
        self.total_questions_asked = 0

    def generate_question(self):
        op = random.choice(self.operators)
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        if op == "/":
            while b == 0 or a % b != 0:
                a = random.randint(1, 100)
                b = random.randint(1, 100)

        self.total_questions_asked += 1
        return a, op, b

    def check_answer(self, a, op, b, user_input):
        try:
            user_answer = int(user_input)
        except ValueError:
            return False, None  # پاسخ نامعتبر

        correct_result = {
            "+": a + b,
            "-": a - b,
            "*": a * b,
            "/": a // b
        }[op]

        if user_answer == correct_result:
            self.correct_count += 1
            return True, correct_result
        else:
            self.wrong_count += 1
            return False, correct_result

    def get_stats(self):
        return self.correct_count, self.wrong_count, self.total_questions_asked

    def reset(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.total_questions_asked = 0
