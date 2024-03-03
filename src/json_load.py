from genericpath import isdir, isfile
from datetime import datetime
import json

class jsonLoad:
    def __init__(self) -> None:
        self.__json_file = "json/command.json"
        self.__file_check()

    def __file_check(self) -> None:
        try:
            if not isdir("json"):
                raise IsADirectoryError("JSONディレクトリがありません")
            elif not isfile(self.__json_file):
                raise FileNotFoundError("JSONファイルがありません")
        except IsADirectoryError as e: print(e)
        
    def get_command_description(self, command:str) -> str:
        with open(self.__json_file, "r", encoding="utf-8") as setting_file:
            setting_json = json.load(setting_file)
            try:
                return setting_json[command]["description"]
            except KeyError:
                return None
            
    def get_command_embed(self, command:str) -> dict:
        with open(self.__json_file, "r", encoding="utf-8") as setting_file:
            setting_json = json.load(setting_file)
            embed = json.loads(setting_json[command]["embed"])
            if "color" in embed:
                embed["color"] = int(embed["color"].lstrip("#"), 16)
            else:
                pass
            if "timestamp" in embed:
                embed["timestamp"] = datetime.utcfromtimestamp(int(embed["timestamp"])).isoformat()
            else:
                pass
            try:
                return embed
            except KeyError:
                return None
        
    def get_command_value(self, command:str) -> dict:
        with open(self.__json_file, "r", encoding="utf-8") as setting_file:
            setting_json = json.load(setting_file)
            try:
                return setting_json[command]["value"]
            except KeyError:
                return None


if __name__ == "__main__":
    data_loader = jsonLoad()
    about_embed = data_loader.get_command_embed("about")
    print(about_embed["timestamp"])
    print(type(about_embed["timestamp"]))