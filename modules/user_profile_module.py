import json
import logging


class UserProfileModule:
    def __init__(self, filepath="./data/user_profiles.json"):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        self.profiles = self.load_profiles()
        logging.basicConfig(level=logging.INFO)

    def load_profiles(self):
        try:
            with open(self.filepath, 'r') as file:
                self.logger.info("Loading user profiles.")
                return json.load(file)
        except FileNotFoundError:
            self.logger.error("User profiles file not found, initializing with empty dictionary.")
            return {}

    def get_user_profile(self, user_id):
        profile = self.profiles.get(user_id, None)
        if profile:
            self.logger.info(f"Profile retrieved for user {user_id}.")
        else:
            self.logger.warning(f"No profile found for user {user_id}.")
        return profile

    def create_user_profile(self, user_id, profile_data):
        if user_id in self.profiles:
            self.logger.error(f"Profile for user {user_id} already exists.")
            return False
        if self.validate_profile_data(profile_data):
            self.profiles[user_id] = profile_data
            self.save_profiles()
            self.logger.info(f"Profile created for user {user_id}.")
            return True
        return False

    def update_user_profile(self, user_id, updates):
        if user_id in self.profiles:
            self.profiles[user_id].update(updates)
            self.save_profiles()
            self.logger.info(f"Profile updated for user {user_id}.")
        else:
            self.logger.warning(f"Profile for user {user_id} not found, cannot update.")

    def delete_user_profile(self, user_id):
        if user_id in self.profiles:
            del self.profiles[user_id]
            self.save_profiles()
            self.logger.info(f"Profile deleted for user {user_id}.")
        else:
            self.logger.warning(f"No profile found for user {user_id}, cannot delete.")

    def save_profiles(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.profiles, file, indent=4)
        self.logger.info("User profiles saved.")

    def validate_profile_data(self, profile_data):
        # Пример простой валидации
        if 'name' in profile_data and 'preferences' in profile_data:
            self.logger.info("Profile data is valid.")
            return True
        self.logger.error("Profile data validation failed.")
        return False

    def get_user_id(self, user_input):
        # Проверяем, является ли ввод пользователя идентификатором пользователя
        if user_input in self.profiles:
            self.logger.info(f"User ID found for input: {user_input}")
            return user_input
        self.logger.warning(f"No user ID found for input: {user_input}")
        return None

# Использование
# filepath = 'path_to_your_user_profiles.json'
# user_profile_module = UserProfileModule(filepath)
