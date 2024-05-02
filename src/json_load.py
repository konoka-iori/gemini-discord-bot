import json
from datetime import datetime, timezone

from genericpath import isdir, isfile


class JsonLoader:
    def __init__(self, file_path: str) -> None:
        """JSON loader class.

        Args:
            file_path (str): JSON file path
        """
        self.__json_file = file_path
        self.data = self.load_json(self.__json_file)

    def __file_check(self, json_file: str | None) -> str:
        """Check if the JSON file exists in the correct location.

        Args:
            json_file (str | None): JSON file path
        Raises:
            IsADirectoryError: JSONディレクトリがありません
            ValueError: JSONファイルが指定されていません
            FileNotFoundError: JSONファイルがありません
        Returns:
            str: JSON file path
        """
        try:
            if not isdir("json"):
                raise IsADirectoryError("JSONディレクトリがありません")
            elif json_file is None:
                raise ValueError("JSONファイルが指定されていません")
            elif not isfile(json_file):
                raise FileNotFoundError("JSONファイルがありません")
        except IsADirectoryError as e:
            print(e)
        return str(json_file)

    def load_json(self, file_path: str | None) -> dict:
        """Load JSON file.

        Args:
            file_path (str | None): JSON file path
        Raises:
            ValueError: JSONファイルの形式が正しくありません
        Returns:
            dict: JSON data
        """
        with open(self.__file_check(file_path), "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            if not isinstance(data, dict):
                raise ValueError("JSONファイルの形式が正しくありません")
            return data


class jsonLoad(JsonLoader):
    def __init__(self) -> None:
        super().__init__("json/command.json")

    def __embed_formater(self, embed: dict) -> dict:
        """Embed formater. color are converted to hex and timestamp to isoformat.

        Args:
            embed (dict): Embed data
        Returns:
            dict: Formated embed data
        """
        if "color" in embed:
            embed["color"] = int(embed["color"].lstrip("#"), 16)
        if "timestamp" in embed:
            embed["timestamp"] = datetime.fromtimestamp(
                int(embed["timestamp"]), tz=timezone.utc).isoformat()
        return embed

    def __get_command(self, command: str, key: str) -> str | None:
        """Retrieves the value corresponding to a key for a given command.

        Args:
            command (str): The name of the command to search for.
            key (str): The key for which the value is to be retrieved.
        Returns:
            str | None: The value corresponding to the key for the specified command, or None if no such data exists.
        """
        try:
            return str(self.data[command][key])
        except KeyError:
            return None

    def get_command_description(self, command: str) -> str:
        """Get command description.

        Args:
            command (str): Command name
        Returns:
            str: Command description
        """
        return str(self.__get_command(command, "description"))

    def get_command_embed(self, command: str) -> dict | None:
        """Get Emned used in the command.

        Args:
            command (str): Command name
        Returns:
            dict | None: Embed data
        """
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
        """Get the user-friendly name of the model.

        Returns:
            str: Model name
        """
        return str(self.__get("name"))

    def get_model_name(self) -> str:
        """Get the technical name of the model.

        Returns:
            str: Model name
        """
        return str(self.__get("model_name"))

    def get_icon(self) -> str:
        """Get the URL of the model's icon.

        Returns:
            str: Model's icon URL
        """
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
