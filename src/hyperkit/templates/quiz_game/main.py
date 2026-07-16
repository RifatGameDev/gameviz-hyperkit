from hyperkit import (
    CameraShake,
    Game,
    GameObject,
    InputActionMap,
    ParticleEmitter,
    ProgressBar,
    Scene,
    ScoreManager,
    TextLabel,
)


class QuizGameScene(Scene):
    """Modern quiz template using HyperKit helpers."""

    def start(self):
        self.questions = [
            {
                "question": "What is 2 + 2?",
                "choices": ["3", "4", "5"],
                "answer": 1,
            },
            {
                "question": "Which one is a game engine?",
                "choices": ["Unity", "Excel", "Notepad"],
                "answer": 0,
            },
            {
                "question": "What input is common in mobile games?",
                "choices": ["Swipe", "Printer", "Scanner"],
                "answer": 0,
            },
        ]

        self.current_index = 0
        self.correct_count = 0

        self.score = ScoreManager(high_score_key="quiz_game_high_score")
        self.particles = ParticleEmitter(self)
        self.camera_shake = CameraShake(self)
        self.actions = InputActionMap()

        self.add(
            TextLabel(
                x=90,
                y=1180,
                text="Quiz Game",
                font_size=38,
                bold=True,
                color=(1, 1, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=60,
                y=1125,
                text="Correct: 0",
                font_size=30,
                color=(1, 1, 1, 1),
            )
        )

        self.best_label = self.add(
            TextLabel(
                x=60,
                y=1085,
                text=f"Best: {self.score.high_score}",
                font_size=26,
                color=(0.8, 0.9, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=60,
            y=1015,
            width=600,
            height=32,
            value=0,
            max_value=len(self.questions),
            fill_color=(0.25, 0.75, 1.0, 1),
            text_format="Question: {value:.0f}/{max_value:.0f}",
            name="quiz_progress",
        )

        self.question_label = self.add(
            TextLabel(
                x=60,
                y=900,
                text="",
                font_size=30,
                bold=True,
                color=(1, 0.9, 0.4, 1),
            )
        )

        self.message_label = self.add(
            TextLabel(
                x=80,
                y=380,
                text="Tap an answer.",
                font_size=26,
                color=(0.9, 0.9, 0.9, 1),
            )
        )

        self.choice_buttons = []
        self.choice_labels = []

        for i in range(3):
            y = 720 - i * 130

            button = self.add(
                GameObject(
                    x=90,
                    y=y,
                    width=540,
                    height=90,
                    color=(0.2, 0.45, 0.9, 1),
                    name=f"choice_button_{i}",
                )
            )

            label = self.add(
                TextLabel(
                    x=125,
                    y=y + 28,
                    text="",
                    font_size=28,
                    color=(1, 1, 1, 1),
                )
            )

            self.choice_buttons.append(button)
            self.choice_labels.append(label)

        self.load_question()
        self.start_game()

    def update_labels(self):
        self.score_label.set_text(f"Correct: {self.correct_count}")
        self.best_label.set_text(f"Best: {self.score.high_score}")
        self.progress_bar.set_value(self.current_index + 1)

    def load_question(self):
        self.actions.clear()

        question = self.questions[self.current_index]
        self.question_label.set_text(question["question"])

        for i, choice in enumerate(question["choices"]):
            self.choice_buttons[i].color = (0.2, 0.45, 0.9, 1)
            self.choice_labels[i].set_text(f"{i + 1}. {choice}")

            self.actions.map_area(
                action=f"answer_{i}",
                x=self.choice_buttons[i].x,
                y=self.choice_buttons[i].y,
                width=self.choice_buttons[i].width,
                height=self.choice_buttons[i].height,
                callback=self.answer_question,
                data={"choice_index": i},
            )

        self.update_labels()

    def answer_question(self, event):
        if not self.is_playing():
            return

        selected = event.data["choice_index"]
        question = self.questions[self.current_index]

        if selected == question["answer"]:
            self.correct_count += 1
            self.score.add(1)
            self.choice_buttons[selected].color = (0.2, 0.8, 0.35, 1)
            self.message_label.set_text("Correct!")

            self.particles.burst(
                x=360,
                y=650,
                count=22,
                color=(0.2, 1.0, 0.45, 1),
                lifetime=0.5,
            )
            self.camera_shake.shake(intensity=5, duration=0.08)
        else:
            self.choice_buttons[selected].color = (1.0, 0.25, 0.25, 1)
            self.message_label.set_text("Wrong answer.")
            self.camera_shake.shake(intensity=14, duration=0.18)

        self.current_index += 1

        if self.current_index >= len(self.questions):
            self.complete_quiz()
        else:
            self.load_question()

    def complete_quiz(self):
        self.end_game()
        self.update_labels()
        self.message_label.set_text("Quiz complete! Tap to restart.")
        self.camera_shake.shake(intensity=18, duration=0.25)

        self.particles.burst(
            x=360,
            y=640,
            count=36,
            color=(1.0, 0.85, 0.2, 1),
            lifetime=0.8,
        )

    def on_tap(self, x, y):
        if self.is_game_over():
            self.reset_round()
            return

        event = self.actions.handle_tap(x, y)

        if event is None:
            self.message_label.set_text("Tap an answer button.")

    def update(self, dt):
        self.particles.update(dt)
        self.camera_shake.update(dt)
        super().update(dt)

    def reset_round(self):
        self.clear()
        self.start()


if __name__ == "__main__":
    Game(title="Quiz Game", width=720, height=1280).set_scene(
        QuizGameScene()
    ).run()
