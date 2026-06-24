from hyperkit import Game, GameObject, Scene, ScoreManager, TextLabel


QUESTIONS = [
    {
        "question": "What is the capital of Bangladesh?",
        "answers": ["Dhaka", "London", "Tokyo", "Delhi"],
        "correct": "Dhaka",
    },
    {
        "question": "2 + 3 = ?",
        "answers": ["4", "5", "6", "7"],
        "correct": "5",
    },
    {
        "question": "Which one is a game engine?",
        "answers": ["Unity", "Excel", "Chrome", "Photoshop"],
        "correct": "Unity",
    },
    {
        "question": "Which language is used for PyPI packages?",
        "answers": ["Python", "HTML", "CSS", "SQL"],
        "correct": "Python",
    },
    {
        "question": "What input is common in mobile games?",
        "answers": ["Touch", "Printer", "Scanner", "DVD"],
        "correct": "Touch",
    },
]


class QuizGameScene(Scene):
    """Educational Quiz Game template.

    Goal:
    - Show a question.
    - Tap the correct answer.
    - Score increases for correct answers.
    - Wrong answer shows feedback.
    - After all questions, show result.
    - Tap after result to restart.
    """

    def start(self):
        self.screen_width = 720
        self.screen_height = 1280

        self.question_index = 0
        self.answer_buttons = []

        self.score = ScoreManager(high_score_key="quiz_game_high_score")

        self.title_label = self.add(
            TextLabel(
                x=80,
                y=1180,
                text="Educational Quiz",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=30,
                y=1125,
                text="Score: 0",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=30,
                y=1085,
                text=f"Best: {self.score.high_score}",
                font_size=26,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.question_label = self.add(
            TextLabel(
                x=50,
                y=960,
                text="Question appears here",
                font_size=28,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.message_label = self.add(
            TextLabel(
                x=90,
                y=500,
                text="Tap the correct answer.",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.create_answer_buttons()
        self.load_question()
        self.start_game()
        self.update_labels()

    def update_labels(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.best_label.set_text(f"Best: {self.score.high_score}")

    def create_answer_buttons(self):
        self.answer_buttons.clear()

        button_width = 520
        button_height = 85
        start_x = 100
        start_y = 780
        gap = 115

        for i in range(4):
            button = self.add(
                GameObject(
                    x=start_x,
                    y=start_y - i * gap,
                    width=button_width,
                    height=button_height,
                    color=(0.2, 0.35, 0.75, 1),
                    name="answer_button",
                )
            )

            button.data["answer"] = ""
            self.answer_buttons.append(button)

            label = self.add(
                TextLabel(
                    x=start_x + 30,
                    y=start_y - i * gap + 25,
                    text="Answer",
                    font_size=26,
                    color=(1, 1, 1, 1),
                )
            )

            button.data["label"] = label

    def current_question(self):
        return QUESTIONS[self.question_index]

    def load_question(self):
        question = self.current_question()

        self.question_label.set_text(question["question"])
        self.message_label.set_text("Tap the correct answer.")

        for button, answer in zip(self.answer_buttons, question["answers"]):
            button.data["answer"] = answer
            button.data["label"].set_text(answer)
            button.color = (0.2, 0.35, 0.75, 1)

    def point_inside_button(self, button, x, y):
        return (
            button.x <= x <= button.x + button.width
            and button.y <= y <= button.y + button.height
        )

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        if not self.is_playing():
            return

        for button in self.answer_buttons:
            if self.point_inside_button(button, x, y):
                self.handle_answer(button)
                return

    def handle_answer(self, button):
        selected_answer = button.data["answer"]
        correct_answer = self.current_question()["correct"]

        if selected_answer == correct_answer:
            self.score.add(1)
            button.color = (0.2, 0.85, 0.35, 1)
            self.message_label.set_text("Correct!")
        else:
            button.color = (1.0, 0.25, 0.25, 1)
            self.message_label.set_text(f"Wrong! Correct: {correct_answer}")

        self.update_labels()
        self.next_question_or_finish()

    def next_question_or_finish(self):
        self.question_index += 1

        if self.question_index >= len(QUESTIONS):
            self.finish_quiz()
            return

        self.load_question()

    def finish_quiz(self):
        self.end_game()

        self.question_label.set_text("Quiz Complete!")
        self.message_label.set_text("Tap anywhere to restart.")

        for button in self.answer_buttons:
            button.color = (0.15, 0.15, 0.2, 1)
            button.data["label"].set_text("")

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Quiz Game", width=720, height=1280).set_scene(
        QuizGameScene()).run()
