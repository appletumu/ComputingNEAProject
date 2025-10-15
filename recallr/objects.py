from recallr.backend import JsonManager

class Accounts:
    def __init__(self):
        json_manager = JsonManager("settings/app_settings.json")
        account = json_manager.read_json("account") 

        self.display_name = account.get('displayName')
        self.username = account.get('username')