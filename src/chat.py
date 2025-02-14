import logging
from time import time

import google.generativeai as gemini


class Chat:
    def __init__(self, token: str, model: str, default_prompt: str) -> None:
        self.__token = token
        self.__model = model
        self.__default_prompt = default_prompt
        self.__logger = logging.getLogger("chat")

    def get_response(self, message: str, prompt: str = "") -> tuple[str, float]:
        """Gemini APIからの応答を取得します。

        Args:
            message (str): User message
            prompt (str): System instruction.
        Returns:
            tuple[str, float]: [0]: Gemini response, [1]: Processing time. Unit: ms
        """
        # promptが空の場合はデフォルトのpromptを使用する。この処理がないとsystem_instructionが空になってエラーでる。
        if prompt == "":
            prompt = self.__default_prompt
        try:
            gemini.configure(api_key=self.__token)
            config = gemini.GenerationConfig(max_output_tokens=1000)
            model = gemini.GenerativeModel(
                system_instruction=prompt,
                model_name=self.__model, generation_config=config)
            start_s = time()
            response = model.generate_content(message)
            end_s = time()
            return str(response.text), float((end_s - start_s) * 1000)
        except Exception as e:
            self.__logger.error(f"{e}")
            return f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```", float(0)

    def ping(self) -> str:
        """Gemini APIにpingを送信し、応答速度を取得します。

        Returns:
            str: Ping result.
        """
        response = self.get_response("ping")
        if response[1] == 0:
            return str(response[0])
        else:
            return f"{round(response[1], 2)} ms"


if __name__ == "__main__":
    from os import getenv
    chat = Chat(token=getenv("GEMINI_API_KEY"),  # type: ignore
                model="gemini-2.0-flash", default_prompt="次の文章に回答してください。")
    test_response = chat.get_response("自己紹介してください。")
    print(test_response[0] + f"\n処理時間: {test_response[1]}")
    print(chat.ping())
    # print(chat.get_response(input(">>> ")))
