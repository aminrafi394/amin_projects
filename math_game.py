import random
import threading
import queue

class MathQuiz:
    def __init__(self):
        self.operators = ["+", "-", "*", "/"]
        self.correct_count = 0
        self.wrong_count = 0
        self.total_questions_asked = 0

    def generate_question(self):
        k = random.randint(0, 3)
        op = self.operators[k]
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        if op == "/":
            while b == 0 or a % b != 0:
                a = random.randint(1, 100)
                b = random.randint(1, 100)
        return a, op, b

    def ask_with_timeout(self, prompt, timeout=20):
        q = queue.Queue()

        def get_input():
            try:
                user_input = input(prompt)
                q.put(user_input)
            except:
                q.put(None)

        t = threading.Thread(target=get_input)
        t.daemon = True
        t.start()

        try:
            answer = q.get(timeout=timeout)
        except queue.Empty:
            print("\n⏰ Time's up! Moving to the next question.\n")
            return None

        return answer

    def check_answer(self, a, op, b, user_input):
        try:
            user_answer = int(user_input)
        except:
            print("❌ Invalid input. Must be an integer.")
            self.wrong_count += 1
            return

        correct = {
            "+": a + b,
            "-": a - b,
            "*": a * b,
            "/": a // b
        }

        if user_answer == correct[op]:
            print("✅ Correct!")
            self.correct_count += 1
        else:
            print(f"❌ Wrong. The correct answer was {correct[op]}.")
            self.wrong_count += 1

    def start_quiz(self):
        print("🎮 Welcome to the Math Quiz Game!")
        print("🕒 You have 20 seconds to answer each question.")
        print("Type your answer and press Enter.\n")

        while True:
            a, op, b = self.generate_question()
            self.total_questions_asked += 1

            question_text = f"{a} {op} {b} = "
            print(f"\n❓ {question_text}")
            user_input = self.ask_with_timeout("Your answer: ")

            if user_input is not None:
                self.check_answer(a, op, b, user_input)
            else:
                self.wrong_count += 1

            if self.total_questions_asked % 5 == 0:
                cont = input("🔁 Do you want to continue? (yes/no): ").strip().lower()
                if cont != "yes":
                    break

        # Show final results
        print("\n📊 Quiz Finished!")
        print(f"✅ Correct Answers: {self.correct_count}")
        print(f"❌ Wrong Answers: {self.wrong_count}")
        print("👏 Thanks for playing!")

# اجرای برنامه
if __name__ == "__main__":
    quiz = MathQuiz()
    quiz.start_quiz()
