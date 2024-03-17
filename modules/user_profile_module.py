import json


class UserProfileModule:
    def __init__(self, filepath="./data/user_profiles.json"):
        self.filepath = filepath
        self.profiles = self.load_profiles()

    def load_profiles(self):
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def get_user_profile(self, user_id):
        return self.profiles.get(user_id, None)

    def update_user_profile(self, user_id, updates):
        if user_id in self.profiles:
            self.profiles[user_id].update(updates)
            self.save_profiles()

    def save_profiles(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.profiles, file, indent=4)

# Использование
# filepath = 'path_to_your_user_profiles.json'
# user_profile_module = UserProfileModule(filepath)
