import json
import random


class Question:
    def __init__(self, prompt, choices, correct_answer, subject):
        self.prompt = prompt
        self.choices = choices
        self.correct_answer = correct_answer
        self.subject = subject

    def check_answer(self, user_choice):
        index = int(user_choice) - 1
        selected_choice = self.choices[index]
        if selected_choice == self.correct_answer:
            return True
        else:
            return False

    def display_question(self):
        print(f"\n{self.prompt}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")


class Quiz:
    def __init__(self):
        self.questions = []
        self.subjects = []
        self.score = 0

    def add_question(self, question):
        self.questions.append(question)

    def start_quiz(self):
        for i, question in enumerate(self.questions, 1):
            print(f"\n--- Question {i} of {len(self.questions)} ---")
            question.display_question()
            while True:
                try:
                    user_choice = input("\nEnter your answer (Pick a number): ")

                    if question.check_answer(user_choice):
                        print("Correct!\n")
                        self.score += 1
                    else:
                        print("Wrong!\n")
                    break
                except ValueError:
                    print("Please enter a valid number.")

                except IndexError:
                    print("Please enter a number on the list.")

        score_percentage = int(self.score / len(self.questions) * 100)
        print(f"\nQuiz Over! Final score is: {self.score} / {len(self.questions)}"
              f" ({score_percentage}%)")

    def load_questions(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for item in data:
                q = Question(item["prompt"], item["choices"], item["correct_answer"], item["subject"])
                self.add_question(q)

            for subjects in self.questions:
                self.subjects.append(subjects.subject)

            return list(set(self.subjects))

    def choose_subject(self, available_subjects):
        while True:
            try:
                print("\nChoose a subject:")
                for i, subject in enumerate(available_subjects, 1):
                    print(f"{i}. {subject}")

                choice = int(input("\nPick a number: ")) - 1
                selected_subject = available_subjects[choice]

                self.questions = [q for q in self.questions if q.subject == selected_subject]
                self.questions = random.sample(self.questions, min(5, len(self.questions)))
                break
            except ValueError:
                print("Please enter a valid number.")

            except IndexError:
                print("Please enter a number on the list.")


my_quiz = Quiz()

available_subjects = my_quiz.load_questions('questions.json')

my_quiz.choose_subject(available_subjects)

my_quiz.start_quiz()
