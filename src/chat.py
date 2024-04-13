import google.generativeai as gemini

class Chat:
    def __init__(self, token:str, model:str) -> None:
        self.token = token
        self.model = model

    def get_response(self, message:str) -> str:
        try:
            gemini.configure(api_key=self.token)
            config = {"max_output_tokens": 1000}
            model = gemini.GenerativeModel(model_name=self.model, generation_config=config)
            return str(model.generate_content(message).text)
        except Exception as e:
            return f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```"


if __name__ == "__main__":
    from os import getenv
    chat = Chat(token=getenv("GEMINI_API_KEY"), model="gemini-1.5-pro-latest") #type: ignore
    print(chat.get_response("自己紹介してください。"))
    #print(chat.get_response(input(">>> ")))
