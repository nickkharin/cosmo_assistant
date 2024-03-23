import asyncio
import logging
from modules.interface_module import InterfaceModule
from modules.processing_module import ProcessingModule
from modules.query_form_module import QueryForm
from modules.user_profile_module import UserProfileModule
from modules.learning_module import LearningModule
from modules.characteristics_module import CharacteristicsModule
from modules.emotions_module import EmotionsModule
from modules.heuristic_module import HeuristicMatrix

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Main:
    def __init__(self):
        self.interface = InterfaceModule()
        self.user_profile_module = UserProfileModule()
        self.learning_module = LearningModule()
        self.characteristics_module = CharacteristicsModule()
        self.emotions_module = EmotionsModule()
        self.heuristic_module = HeuristicMatrix()

        self.processing_module = ProcessingModule(
            user_profile_module=self.user_profile_module,
            emotions_module=self.emotions_module,
            learning_module=self.learning_module,
            characteristics_module=self.characteristics_module
        )

        self.current_state = 'awaiting_user_id'
        self.current_user_id = None

    async def handle_query(self, user_input, user_id):
        try:
            query_form = QueryForm(user_id=user_id, query_text=user_input, user_profile_module=self.user_profile_module,
                                   emotions_module=self.emotions_module, learning_module=self.learning_module)
            response = await self.processing_module.process_query(query_form)
            self.interface.display_text(response)
        except Exception as e:
            logging.error(f"Error processing request for user {user_id} with input '{user_input}': {e}")
            self.interface.display_text("Извините, произошла ошибка при обработке вашего запроса.")

    async def main_loop(self):
        self.interface.display_text(self.interface.translations[self.interface.language]['greeting'])
        while True:
            user_input = self.interface.get_user_input()
            if user_input.lower() == 'exit':
                break

            if self.current_state == 'awaiting_user_id':
                self.current_user_id = user_input  # Сохраняем user_id
                self.current_state = 'awaiting_command'
                self.interface.display_text("Как я могу помочь вам сегодня?")
            elif self.current_state == 'awaiting_command':
                await self.handle_query(user_input, self.current_user_id)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main_loop())
