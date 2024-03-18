import json


class CharacteristicsModule:
    def __init__(self, file_path='./data/characteristics_matrix.json'):
        self.file_path = file_path
        self.characteristics = self.load_characteristics()

    def load_characteristics(self):
        """
        Загружает характеристики ассистента из файла.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return self.initialize_characteristics()

    def save_characteristics(self):
        """
        Сохраняет характеристики ассистента в файл.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.characteristics, file, indent=4)

    def update_characteristic(self, characteristic, value):
        """
        Обновляет конкретную характеристику ассистента.
        """
        if characteristic in self.characteristics:
            self.characteristics[characteristic] = value
            self.save_characteristics()

    def initialize_characteristics(self):
        """
        Инициализирует характеристики ассистента с начальными значениями, если файл не найден.
        """
        return {
            'friendliness': 5,
            'patience': 5,
            'confidence': 5,
            # Дополнительные характеристики
        }

# Пример использования
# characteristics_module = CharacteristicsModule()
# characteristics_module.update_characteristic('friendliness', 7)
