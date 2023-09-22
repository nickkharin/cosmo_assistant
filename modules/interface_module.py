class InterfaceModule:
    def get_user_input(self):
        user_input = input("User: ")
        return user_input

    def send_response(self, response):
        print("Kosmo: ", response)