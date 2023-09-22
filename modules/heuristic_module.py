import json

class HeuristicMatrix:
    def __init__(self, file_path='path_to_your_json_file.json'):
        with open(file_path, 'r') as f:
            self.heuristic_matrix = json.load(f)

    def get_suggested_action(self, state):
        actions = self.heuristic_matrix.get(state, {})
        if not actions:
            return None
        return max(actions, key=actions.get)  # return the action with the highest value
