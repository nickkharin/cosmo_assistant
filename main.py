import asyncio
import logging
from modules.interface_module import InterfaceModule
from modules.processing_module import ProcessingModule
from modules.query_form_module import QueryForm
from modules.user_profile_module import UserProfileModule

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Main:
    def __init__(self):
        self.interface = InterfaceModule()
        self.processing_module = ProcessingModule()
        self.user_profile_module = UserProfileModule()

    async def handle_query(self, user_input, user_id):
        try:
            query_form = QueryForm(user_id=user_id, query_text=user_input)
            response = await self.processing_module.process_query(query_form)
            self.interface.display_text(f"Cosmo: {response}")
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.interface.display_text("Извините, произошла ошибка при обработке вашего запроса.")

    async def main_loop(self):
        while True:
            user_input = self.interface.get_user_input()
            if user_input.lower() == 'exit':
                break

            user_id = self.user_profile_module.get_user_id(user_input)
            await self.handle_query(user_input, user_id)

if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main_loop())
