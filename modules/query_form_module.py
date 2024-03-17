class QueryForm:
    def __init__(self, user_id, query_text, user_profile_module, emotions_module, learning_module, history_limit=10):
        self.user_id = user_id
        self.query_text = query_text
        self.intent = None
        self.entities = []
        self.context = {}
        self.response = None
        self.dialogue_history = []
        self.history_limit = history_limit

        self.user_profile_module = user_profile_module
        self.emotions_module = emotions_module
        self.learning_module = learning_module

        self.user_profile = self.user_profile_module.get_user_profile(user_id)
        self.current_emotion = self.emotions_module.get_current_emotion(user_id)

    def set_intent(self, intent):
        self.intent = intent

    def add_entity(self, text, category=None, confidence=1.0):
        self.entities.append({
            'text': text,
            'category': category,
            'confidence': confidence
        })

    def set_context(self, context):
        self.context = context

    def set_response(self, response):
        self.response = response
        self._update_dialogue_history()

    def _update_dialogue_history(self):
        if len(self.dialogue_history) >= self.history_limit:
            self.dialogue_history.pop(0)
        self.dialogue_history.append({
            'query': self.query_text,
            'intent': self.intent,
            'entities': self.entities,
            'response': self.response
        })

    def get_summary(self):
        return {
            'user_id': self.user_id,
            'query_text': self.query_text,
            'intent': self.intent,
            'entities': self.entities,
            'context': self.context,
            'response': self.response,
            'dialogue_history': self.dialogue_history
        }

    def analyze_context(self):
        # Пример контекстного анализа, использующий историю диалогов
        if not self.dialogue_history:
            return "No previous context."

        # Анализ предыдущих запросов и ответов для определения повторяющихся тем или изменений в намерениях
        previous_intents = [dialogue['intent'] for dialogue in self.dialogue_history]
        common_intent = max(set(previous_intents), key=previous_intents.count) if previous_intents else None

        # Определение изменений в эмоциональном состоянии
        emotion_changes = [dialogue['emotion'] for dialogue in self.dialogue_history if 'emotion' in dialogue]
        current_emotion = self.current_emotion
        previous_emotion = emotion_changes[-1] if emotion_changes else None

        # Сбор контекстной информации
        self.context = {
            'common_intent': common_intent,
            'previous_emotion': previous_emotion,
            'current_emotion': current_emotion,
            'emotion_changed': previous_emotion != current_emotion
        }

        return self.context

    def add_feedback(self, feedback):
        # Добавление обратной связи в историю диалогов для будущего анализа и обучения
        self.dialogue_history[-1]['feedback'] = feedback
        # Обновление модели может происходить здесь или в отдельном процессе обучения
        self.learning_module.process_feedback(feedback, self.dialogue_history[-1])

    def train(self):
        # Обучение модели на основе собранных данных
        if self.dialogue_history:
            self.learning_module.train(self.dialogue_history)
        else:
            print("No dialogue history to train on.")
