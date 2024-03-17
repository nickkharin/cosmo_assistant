import spacy
from query_form_module import QueryForm
from emotions_module import Emotions
from characteristics_module import Characteristics


class ProcessingModule:
    def __init__(self):
        self.nlp = spacy.load('ru_core_news_sm')
        self.emotions = Emotions('path_to_emotion_matrix.json')
        self.characteristics = Characteristics('path_to_characteristics.json')

    async def process_query(self, query_form):
        doc = self.nlp(query_form.query_text)

        query_form.intent = self._determine_intent(doc)
        query_form.entities = self._extract_entities(doc)
        query_form.context = self._get_context(query_form.user_id)
        query_form.emotion = self.emotions.get_emotion(doc)

        response = self._generate_response(query_form)
        return response

    def _determine_intent(self, doc):
        root_verb = None
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                root_verb = token.lemma_
                break

        action_objects = [child for child in token.children if child.dep_ in ['dobj', 'attr', 'prep']]
        adjectives = [child.lemma_ for child in action_objects if child.pos_ == 'ADJ']

        intent = {
            'action': root_verb,
            'objects': [obj.lemma_ for obj in action_objects],
            'descriptions': adjectives
        }

        return intent if root_verb else 'unknown'

    def _extract_entities(self, doc):
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

        return entities

    def _get_context(self, user_id):
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

        return context

    def _get_user_history(self, user_id, limit=5):
        return [
            {'text': 'Какая погода в Москве?', 'intent': 'weather_query',
             'entities': [{'text': 'Москва', 'type': 'location'}], 'topics': ['weather']},
            # Дополните другими диалогами по мере необходимости
        ]

    def _generate_response(self, query_form):
        intent = query_form.intent['action']
        entities = query_form.entities
        context = query_form.context
        user_emotion = query_form.emotion

        if intent == 'приветствовать':
            return self._handle_greeting(user_emotion)
        elif intent == 'спрашивать':
            return self._handle_inquiry(entities, context)
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
