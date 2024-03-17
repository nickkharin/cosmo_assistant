import json

class HeuristicMatrix:
    def __init__(self, file_path='heuristic_matrix.json'):
        self.file_path = file_path
        self.matrix = self.load_heuristic_matrix()

    def load_heuristic_matrix(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def get_suggested_action(self, state):
        """
        Возвращает предложенное действие на основе текущего состояния.
        """
        actions = self.matrix.get(state, {})
        if actions:
            return max(actions, key=actions.get)  # Возвращает действие с максимальным значением
        return None

    def update_heuristic_matrix(self, state, action, value):
        """
        Обновляет эвристическую матрицу с новым значением для действия в данном состоянии.
        """
        if state not in self.matrix:
            self.matrix[state] = {}

        self.matrix[state][action] = value
        self.save_heuristic_matrix()

    def save_heuristic_matrix(self):
        """
        Сохраняет текущее состояние эвристической матрицы в файл.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.matrix, file, indent=4)
