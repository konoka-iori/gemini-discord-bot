import google.generativeai as gemini

class Chat:
    def __init__(self, token:str) -> None:
        self.chatbot = gemini.Chatbot(token)
        self.token = token
    
    def get_response(self, message:str) -> str:
        try:
            gemini.configure(api_key=self.token)
            model = gemini.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            user_input = message
            return str(chat.send_message(user_input).text)
        except Exception as e:
            return f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```" # TODO: JSONに移すか検討。今はとりあえずこれで。