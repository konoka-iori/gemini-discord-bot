from time import time
import google.generativeai as gemini


class Chat:
    def __init__(self, token:str, model:str) -> None:
        self.__token = token
        self.__model = model

    def get_response(self, message:str) -> tuple[str, float]:
        try:
            gemini.configure(api_key=self.__token)
            config = {"max_output_tokens": 1000}
            model = gemini.GenerativeModel(model_name=self.__model, generation_config=config)
            start = time()
            response = model.generate_content(message)
            end = time()
            return str(response.text), float(end - start)
        except Exception as e:
            return f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```", float(0)

    def ping(self) -> str:
        response = self.get_response("ping")
        if response[1] == 0:
            return str(response[0])
        else:
            return f"{round(response[1], 2)} ms"


if __name__ == "__main__":
    from os import getenv
    chat = Chat(token=getenv("GEMINI_API_KEY"), model="gemini-1.5-pro-latest") #type: ignore
    test_response = chat.get_response("自己紹介してください。")
    print(test_response[0] + f"\n処理時間: {test_response[1]}")
    print(chat.ping())
    #print(chat.get_response(input(">>> ")))
