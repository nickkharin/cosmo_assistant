import json


class Emotions:
    def __init__(self, emotion_matrix_file):
        with open(emotion_matrix_file, 'r') as file:
            self.emotion_matrix = json.load(file)

    def get_emotion(self, situation):
        # Возвращение эмоции, соответствующей конкретной ситуации.
        return self.emotion_matrix.get(situation, "neutral")


# Использование
emotion_matrix_file = "path_to_your_emotion_matrix.json"
emotions = Emotions(emotion_matrix_file)
emotion = emotions.get_emotion("some_situation")
