import spacy
import logging
from modules.characteristics_module import CharacteristicsModule


class ProcessingModule:
    def __init__(self, learning_module=None, heuristic_module=None, emotions_module=None, user_profile_module=None,
                 characteristics_module=None):
        self.logger = logging.getLogger(__name__)
        self.nlp = spacy.load('ru_core_news_sm')
        self.characteristics_module = characteristics_module
        self.learning_module = learning_module
        self.heuristic_module = heuristic_module
        self.emotions_module = emotions_module
        self.user_profile_module = user_profile_module

    async def process_query(self, query_form):
        #        self.logger.info(f"Processing query: {query_form.query_text}")
        doc = self.nlp(query_form.query_text)

        query_form.intent = self._determine_intent(doc)
        self.logger.info(f"Determined intent: {query_form.intent}")

        query_form.entities = self._extract_entities(doc)
        self.logger.info(f"Extracted entities: {query_form.entities}")

        query_form.context = self._get_context(query_form.user_id)
        #        self.logger.info(f"Context for user {query_form.user_id}: {query_form.context}")

        query_form.emotion = self.emotions_module.get_emotion(query_form.user_id)
        self.logger.info(f"Emotion for user {query_form.user_id}: {query_form.emotion}")

        response = self._generate_response(query_form)
        #        self.logger.info(f"Generated response: {response}")
        return response

    def _determine_intent(self, doc):
        self.logger.debug("Determining intent.")
        intents = []
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                intents.append(token.lemma_)

        # Можно добавить более сложные условия для определения намерений
        if intents:
            intent = max(set(intents), key=intents.count)  # Пример выбора наиболее частого намерения
        else:
            intent = 'unknown'

        self.logger.debug(f"Determined intent: {intent}")
        return {'action': intent}

    def _extract_entities(self, doc):
        self.logger.debug("Extracting entities.")
        entities = []
        for ent in doc.ents:
            entity = {
                'text': ent.text,
                'type': ent.label_,
                'start_pos': ent.start_char,
                'end_pos': ent.end_char,
                'sentence': ent.sent.text,
                'context_words': [token.lemma_ for token in ent.sent if not token.is_stop and not token.is_punct]
            }
            entities.append(entity)

        self.logger.debug(f"Extracted entities: {entities}")
        return entities

    def _get_context(self, user_id):
        self.logger.debug("Getting user context.")
        history_limit = 5
        user_history = self._get_user_history(user_id, limit=history_limit)

        context = {
            'recent_dialogues': user_history,
            'topics': set(),
            'intents': set(),
            'entities': set()
        }

        for dialogue in user_history:
            context['topics'].update(dialogue['topics'])
            context['intents'].add(dialogue['intent'])
            context['entities'].update([entity['text'] for entity in dialogue['entities']])

        #        self.logger.debug(f"Context for user {user_id}: {context}")
        return context

    def _get_user_history(self, user_id, limit=5):
        self.logger.debug("Getting user history.")
        return [
            {'text': 'Какая погода в Москве?', 'intent': 'weather_query',
             'entities': [{'text': 'Москва', 'type': 'location'}], 'topics': ['weather']},
            # Дополните другими диалогами по мере необходимости
        ]

    def _generate_response(self, query_form):
        self.logger.debug("Generating response.")
        intent = query_form.intent.get('action', 'unknown')
        entities = query_form.entities
        context = query_form.context
        user_emotion = query_form.emotion

        if intent == 'приветствовать':
            return self._handle_greeting(user_emotion)
        elif intent == 'спрашивать':
            return self._handle_inquiry(entities, context)
        elif intent == 'сделать':
            return 'Что именно вы хотели бы сделать?'
        else:
            return 'Извините, я не уверен, как на это ответить.'

    def _handle_greeting(self, user_emotion):
        if user_emotion == 'joy':
            return 'Привет! Рад видеть тебя в хорошем настроении!'
        elif user_emotion == 'sadness':
            return 'Привет. Я здесь, чтобы поднять тебе настроение.'
        else:
            return 'Привет! Как я могу помочь тебе сегодня?'

    def _handle_inquiry(self, entities, context):
        if entities:
            return f'Ты спрашиваешь о {entities[0]["text"]}...'
        else:
            return 'Что ты хотел бы узнать?'
