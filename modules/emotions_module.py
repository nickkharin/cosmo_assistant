import json
import logging


class EmotionsModule:
    def __init__(self, file_path='./data/emotions_matrix.json'):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        self.emotion_matrix = self.load_emotions()
        self.user_emotions = {}

    def load_emotions(self):
        try:
            with open(self.file_path, 'r') as file:
                self.logger.info("Loading emotions matrix.")
                return json.load(file)
        except FileNotFoundError:
            self.logger.error(f"File {self.file_path} not found, initializing default emotions matrix.")
            return self.initialize_emotions()

    def get_emotion(self, user_id):
        """
        Возвращает текущее эмоциональное состояние для данного пользователя.
        Если для пользователя нет сохраненных эмоций, возвращает 'neutral'.
        """
        emotion = self.user_emotions.get(user_id)
        if emotion is None:
            self.logger.info(f"No specific emotion found for user {user_id}, returning 'neutral'.")
            return 'neutral'

        # Если эмоции пользователя хранятся как словарь, определите, какая эмоция доминирует
        if isinstance(emotion, dict):
            dominant_emotion = max(emotion, key=emotion.get)
            self.logger.info(f"Retrieved dominant emotion {dominant_emotion} for user {user_id}.")
            return dominant_emotion

        # Если эмоции хранятся по-другому, уточните логику обработки
        self.logger.info(f"Retrieved {emotion} for user {user_id}.")
        return emotion

    def update_emotion(self, user_id, new_emotion):
        """
        Обновляет эмоциональное состояние пользователя на основе взаимодействия эмоций.
        """
        self.logger.info(f"Updating emotion for user {user_id} with new emotion {new_emotion}.")

        if user_id not in self.user_emotions:
            self.logger.info(f"Initializing emotions for user {user_id}.")
            self.user_emotions[user_id] = {emotion: 0 for emotion in self.emotion_matrix}

        current_emotions = self.user_emotions[user_id]

        if new_emotion in self.emotion_matrix:
            for emotion, impact in self.emotion_matrix[new_emotion].items():
                current_emotions[emotion] += impact
                self.logger.debug(f"Updated {emotion} to {current_emotions[emotion]} for user {user_id}.")
        else:
            self.logger.warning(f"{new_emotion} not found in emotion matrix.")

        for emotion in current_emotions:
            current_emotions[emotion] = max(0, min(1, current_emotions[emotion]))

        self.user_emotions[user_id] = current_emotions
        self.save_emotions()

        dominant_emotion = max(current_emotions, key=current_emotions.get)
        self.logger.info(f"Updated dominant emotion for {user_id} is {dominant_emotion}.")

    def initialize_emotions(self):
        self.logger.info("Initializing default emotions matrix.")
        return {
            'joy': {'joy': 1, 'sadness': -1},
            'sadness': {'joy': -1, 'sadness': 1},
        }

    def save_emotions(self):
        """
        Сохраняет эмоциональные состояния в файл.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.user_emotions, file, indent=4)
            self.logger.info("Emotions saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save emotions: {e}")
