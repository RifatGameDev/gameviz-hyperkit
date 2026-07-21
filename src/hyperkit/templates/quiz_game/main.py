from __future__ import annotations

from hyperkit import (
    AssetManager,
    BoundsManager,
    CameraShake,
    Game,
    GameObject,
    InputActionMap,
    ParticleEmitter,
    ProgressBar,
    Scene,
    ScoreManager,
    ScreenBounds,
    TextLabel,
)


class QuizGameScene(Scene):
    def start(self):
        self.questions = [
            {
                "question": "Which engine is popular for mobile games?",
                "answers": ["Unity", "Spreadsheet", "Browser"],
                "correct": 0,
            },
            {
                "question": "What input does this quiz use?",
                "answers": ["Tap", "Voice only", "GPS"],
                "correct": 0,
            },
            {
                "question": "What does a score system track?",
                "answers": ["Points", "Weather", "Battery"],
                "correct": 0,
            },
            {
                "question": "What is useful for UI feedback?",
                "answers": ["ProgressBar", "Printer", "Cable"],
                "correct": 0,
            },
        ]

        self.current_question_index = 0
        self.score_goal = len(self.questions)
        self.game_over = False
        self.answer_buttons = []
        self.answer_labels = []

        self.assets = AssetManager()
        self.score = ScoreManager(high_score_key="quiz_game_high_score")
        self.camera_shake = CameraShake(self)
        self.particles = ParticleEmitter(self)
        self.bounds_manager = BoundsManager()
        self.screen_bounds = ScreenBounds(width=720, height=1280)
        self.input_actions = InputActionMap()

        self.background = self.add(
            GameObject(
                x=0,
                y=0,
                width=720,
                height=1280,
                color=(0.08, 0.09, 0.14, 1),
                shape="rect",
            )
        )

        self.title_label = self.add(
            TextLabel(
                x=45,
                y=1180,
                text="Quiz Game",
                font_size=44,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.help_label = self.add(
            TextLabel(
                x=45,
                y=1125,
                text="Tap the correct answer and complete the quiz.",
                font_size=22,
                color=(0.82, 0.9, 1, 1),
            )
        )

        self.score_label = self.add(
            TextLabel(
                x=45,
                y=1045,
                text="Score: 0",
                font_size=34,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self.high_score_label = self.add(
            TextLabel(
                x=45,
                y=995,
                text=f"High Score: {self.score.high_score}",
                font_size=26,
                color=(0.95, 0.82, 0.3, 1),
            )
        )

        self.progress_label = self.add(
            TextLabel(
                x=45,
                y=920,
                text=f"Question: 1 / {self.score_goal}",
                font_size=24,
                color=(0.78, 0.92, 1, 1),
            )
        )

        self.progress_bar = ProgressBar(
            scene=self,
            x=45,
            y=875,
            width=630,
            height=30,
            value=0,
            max_value=self.score_goal,
        )

        self.question_label = self.add(
            TextLabel(
                x=45,
                y=760,
                text="Question",
                font_size=28,
                color=(1, 1, 1, 1),
                bold=True,
            )
        )

        self._create_answer_buttons()

        self.status_label = self.add(
            TextLabel(
                x=45,
                y=120,
                text="Ready. Choose an answer!",
                font_size=26,
                color=(0.8, 1, 0.85, 1),
            )
        )

        self._show_question()
        self.start_game()

    def _create_answer_buttons(self):
        button_y_positions = [600, 470, 340]

        for index, y in enumerate(button_y_positions):
            button = self.add(
                GameObject(
                    x=70,
                    y=y,
                    width=580,
                    height=85,
                    color=(0.18, 0.22, 0.34, 1),
                    shape="rect",
                    image_path=None,
                )
            )

            label = self.add(
                TextLabel(
                    x=100,
                    y=y + 26,
                    text=f"Answer {index + 1}",
                    font_size=24,
                    color=(1, 1, 1, 1),
                    bold=True,
                )
            )

            self.answer_buttons.append(button)
            self.answer_labels.append(label)

    def update(self, dt):
        self.camera_shake.update(dt)
        self.particles.update(dt)
        super().update(dt)

    def on_tap(self, x, y):
        if self.game_over:
            self._restart()
            return

        answer_index = self._find_tapped_answer(x, y)

        if answer_index is None:
            self.status_label.set_text("Tap one of the answer boxes.")
            return

        self._check_answer(answer_index)

    def _find_tapped_answer(self, x, y):
        for index, button in enumerate(self.answer_buttons):
            inside_x = button.x <= x <= button.x + button.width
            inside_y = button.y <= y <= button.y + button.height

            if inside_x and inside_y:
                return index

        return None

    def _check_answer(self, answer_index: int):
        current_question = self.questions[self.current_question_index]

        if answer_index == current_question["correct"]:
            self._handle_correct_answer(answer_index)
        else:
            self._handle_wrong_answer(answer_index)

    def _handle_correct_answer(self, answer_index: int):
        self.score.add(1)

        selected_button = self.answer_buttons[answer_index]
        selected_button.color = (0.25, 1.0, 0.48, 1)

        self.particles.burst(
            x=selected_button.x + selected_button.width / 2,
            y=selected_button.y + selected_button.height / 2,
            count=12,
        )

        self.current_question_index += 1
        self._update_score_ui()

        if self.current_question_index >= len(self.questions):
            self._set_quiz_complete()
            return

        self.status_label.set_text("Correct! Next question.")
        self._show_question()

    def _handle_wrong_answer(self, answer_index: int):
        selected_button = self.answer_buttons[answer_index]
        selected_button.color = (1.0, 0.28, 0.28, 1)

        self.camera_shake.shake(intensity=14, duration=0.3)
        self.status_label.set_text("Wrong answer. Try the next one carefully.")

        self.current_question_index += 1
        self._update_score_ui()

        if self.current_question_index >= len(self.questions):
            self._set_quiz_complete()
            return

        self._show_question()

    def _show_question(self):
        current_question = self.questions[self.current_question_index]

        self.question_label.set_text(current_question["question"])

        for index, answer in enumerate(current_question["answers"]):
            self.answer_labels[index].set_text(answer)
            self.answer_buttons[index].color = (0.18, 0.22, 0.34, 1)

        self.progress_label.set_text(
            f"Question: {self.current_question_index + 1} / {self.score_goal}"
        )
        self.progress_bar.set_value(self.current_question_index)

    def _update_score_ui(self):
        self.score_label.set_text(f"Score: {self.score.value}")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.progress_bar.set_value(self.current_question_index)

    def _set_quiz_complete(self):
        self.game_over = True
        self.progress_bar.set_value(self.score_goal)

        if self.score.value == self.score_goal:
            self.status_label.set_text("Perfect score! Tap to restart.")
            self.camera_shake.shake(intensity=8, duration=0.2)
        else:
            self.status_label.set_text("Quiz complete. Tap to try again.")

        for button in self.answer_buttons:
            button.color = (0.25, 0.85, 1.0, 1)

    def _restart(self):
        self.game_over = False
        self.current_question_index = 0

        self.score.reset()
        self.score_label.set_text("Score: 0")
        self.high_score_label.set_text(f"High Score: {self.score.high_score}")
        self.status_label.set_text("Ready. Choose an answer!")

        self._show_question()


if __name__ == "__main__":
    Game(
        title="HyperKit Quiz Game",
        width=720,
        height=1280,
    ).set_scene(QuizGameScene()).run()
