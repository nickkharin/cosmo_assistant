import json


class Emotions:
    def __init__(self, emotion_matrix_file):
        with open(emotion_matrix_file, 'r') as file:
            self.emotion_matrix = json.load(file)

    def get_emotion(self, situation):
        # Возвращение эмоции, соответствующей конкретной ситуации.
        return self.emotion_matrix.get(situation, "neutral")

    def update_emotions(self, stimulus):
        # В этом методе вы можете обновить эмоциональные состояния на основе входящего стимула.
        # Например, если стимул увеличивает радость, вы можете изменить остальные эмоции, используя матрицу.
        for emotion in self.emotions:
            self.emotions[emotion] += self.matrix[emotion][stimulus]

    def get_dominant_emotion(self):
        dominant_emotion = max(self.emotions, key=self.emotions.get)
        return f"Текущее доминирующее эмоциональное состояние: {dominant_emotion} - {self.emotions[dominant_emotion]}"


# Использование
emotion_matrix_file = "path_to_your_emotion_matrix.json"
emotions = Emotions(emotion_matrix_file)
emotion = emotions.get_emotion("some_situation")
