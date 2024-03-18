import json
import logging

class HeuristicMatrix:
    def __init__(self, file_path='./data/heuristic_matrix.json', other_modules=None):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        self.matrix = self.load_heuristic_matrix()
        self.other_modules = other_modules or {}

        logging.basicConfig(level=logging.INFO)

    def load_heuristic_matrix(self):
        try:
            with open(self.file_path, 'r') as file:
                self.logger.info("Loading heuristic matrix.")
                return json.load(file)
        except FileNotFoundError:
            self.logger.error("Heuristic matrix file not found, initializing empty matrix.")
            return {}

    def get_suggested_action(self, state):
        actions = self.matrix.get(state, {})
        if actions:
            action = max(actions, key=actions.get)
            self.logger.info(f"Suggested action for state {state} is {action}.")
            return action
        self.logger.warning(f"No action found for state {state}.")
        return None

    def update_heuristic_matrix(self, state, action, value):
        if state not in self.matrix:
            self.matrix[state] = {}

        self.matrix[state][action] = value
        self.logger.info(f"Updated heuristic matrix for state {state}: {action} = {value}.")
        self.save_heuristic_matrix()

    def save_heuristic_matrix(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.matrix, file, indent=4)
        self.logger.info("Heuristic matrix saved.")

    def integrate_with_other_modules(self):
        """
        Интегрирует данные из других модулей для улучшения эвристических решений.
        """
        self.logger.info("Integrating with other modules.")
        for module_name, module in self.other_modules.items():
            # Получаем необходимые данные из каждого модуля
            data = module.get_data()
            # Интеграция данных в эвристическую матрицу может быть реализована здесь
            self.logger.info(f"Integrated data from {module_name}: {data}")
            # Пример обновления эвристической матрицы на основе полученных данных
            # self.update_heuristic_matrix(state, action, value) можно вызывать здесь

# Пример использования
# other_modules = {'module_name': module_instance}
# heuristic_module = HeuristicMatrix(other_modules=other_modules)
# heuristic_module.integrate_with_other_modules()
