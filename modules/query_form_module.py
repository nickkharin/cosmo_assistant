class QueryForm:
    def __init__(self, query_text, user_id=1):
        self.user_id = user_id  # Идентификатор пользователя
        self.query_text = query_text.text  # Текст запроса
        self.intent = ""  # Намерение пользователя
        self.object = ""
        self.date = ""
        self.time = ""
        self.entities = []  # Сущности, извлеченные из запроса
        self.context = {}  # Контекст запроса (например, предыдущие запросы и ответы)
        self.response = None  # Ответ ассистента
        # Дополнительные поля, которые могут быть нужны для обработки запроса

    def form_filling(self):
        for token in self.query_text:
            if token.dep_ == "ROOT":
                self.intent = token.text
            if token.dep_ == "obj":
                self.object = token.text
        self.entities = [ent for ent in self.query_text.ents]


