from genericpath import isdir, isfile
from datetime import datetime
import json


class JsonLoader:
    def __init__(self, file_path:str) -> None:
        self.__json_file = file_path
        self.data = self.load_json(self.__json_file)

    def __file_check(self, json_file:str|None) -> str:
        try:
            if not isdir("json"):
                raise IsADirectoryError("JSONディレクトリがありません")
            elif json_file is None:
                raise ValueError("JSONファイルが指定されていません")
            elif not isfile(json_file):
                raise FileNotFoundError("JSONファイルがありません")
        except IsADirectoryError as e: print(e)
        return str(json_file)

    def load_json(self, file_path:str|None) -> dict:
        with open(self.__file_check(file_path), "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            if not isinstance(data, dict):
                raise ValueError("JSONファイルの形式が正しくありません")
            return data


class jsonLoad(JsonLoader):
    def __init__(self) -> None:
        super().__init__("json/command.json")

    def __embed_formater(self, embed:dict) -> dict:
        if "color" in embed:
            embed["color"] = int(embed["color"].lstrip("#"), 16)
        if "timestamp" in embed:
            embed["timestamp"] = datetime.utcfromtimestamp(int(embed["timestamp"])).isoformat()
        return embed

    def __get_command(self, command:str, key:str) -> str | None:
        try:
            return str(self.data[command][key])
        except KeyError:
            return None

    def get_command_description(self, command:str) -> str:
        return str(self.__get_command(command, "description"))

    def get_command_embed(self, command:str) -> dict | None:
        return self.__embed_formater(self.load_json(self.__get_command(command, "embed")))

    # def get_command_value(self, command:str) -> dict:
    #     return self.__get_command(command, "value")


class ModelLoad(JsonLoader):
    def __init__(self) -> None:
        super().__init__("json/model.json")

    def __get(self, key: str) -> str | None:
        try:
            return str(self.data[key])
        except KeyError:
            return None

    def get_name(self) -> str:
        return str(self.__get("name"))

    def get_model_name(self) -> str:
        return str(self.__get("model_name"))

    def get_icon(self) -> str:
        return str(self.__get("icon"))


if __name__ == "__main__":
    data_loader = jsonLoad()

    print("---about command---")
    print(data_loader.get_command_description("about"))
    print(data_loader.get_command_embed("about"))

    print("---chat command---")
    print(data_loader.get_command_description("chat"))

    print("---model data---")
    model_loader = ModelLoad()
    print(model_loader.get_name())
    print(model_loader.get_model_name())
    print(model_loader.get_icon())
