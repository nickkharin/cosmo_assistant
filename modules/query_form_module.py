class QueryForm:
    def __init__(self, user_id, query_text):
        self.user_id = user_id  # Идентификатор пользователя
        self.query_text = query_text  # Текст запроса
        self.intent = None  # Намерение пользователя
        self.entities = []  # Сущности, извлеченные из запроса
        self.context = {}  # Контекст запроса (например, предыдущие запросы и ответы)
        self.response = None  # Ответ ассистента
        # Дополнительные поля, которые могут быть нужны для обработки запроса
