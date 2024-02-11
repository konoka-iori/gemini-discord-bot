import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import google.generativeai as gemini


class Search:
    def __init__(self, google_api_key, cx_key):
        self.google_api_key = google_api_key
        self.cx_key = cx_key

    def get_search_results(self, query, num, start_index=1):
        service = build("customsearch", "v1", developerKey=self.google_api_key)
        result = service.cse().list(q=query, cx=self.cx_key, num=num, start=start_index).execute()
        return result
    
    def get_contents(self, links:list):
        contents = []
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            content = soup.get_text()
            content = re.sub(r"\s+", " ", content)
            contents.append(content)
        return contents


class Chat:
    def __init__(self, token:str, message:str) -> None:
        self.token = token
        self.message = message

    def get_query(self) -> str:
        gemini.configure(api_key=self.token)
        model = gemini.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        user_input = f"ユーザーから送信された以下のメッセージから、検索クエリを抽出してください。検索クエリ以外のものは出力しないでください。\n{self.message}"
        return str(chat.send_message(user_input).text)
    
    def get_summary(self, contents:list) -> list:
        summary = []
        for content in contents:
            gemini.configure(api_key=self.token)
            model = gemini.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            user_input = f"{self.message}\nというユーザーの質問に沿うように、以下の情報を要約してください。質問に沿う要素や参考になる情報はすべて含めてください。\n{content}"
            summary.append(str(chat.send_message(user_input).text))
        return summary
    
    def get_answer(self, content:list) -> str:
        try:
            gemini.configure(api_key=self.token)
            model = gemini.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            user_input = f"{self.message}\nというユーザーの質問に、以下の情報をもとに回答してください。回答内容には、リストの何番目を参照したのかソースを文末に数字で記載します。\n{content}"
            return str(chat.send_message(user_input).text)
        except Exception as e:
            return f"エラーが発生しました。以下の内容をコピペして管理者までお知らせください。\n```{e}```" # TODO: JSONに移すか検討。今はとりあえずこれで。


if __name__ == "__main__":
    from os import getenv
    search = Search(getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"), getenv("CX"))
    chat = Chat(getenv("GEMINI_API_KEY"), input(">>> "))

    query = chat.get_query()
    print(f"「{query}」を検索しています...")
    res = search.get_search_results(query=query, num=5)
    print("検索結果を確認しています...")
    content = search.get_contents([item["link"] for item in res["items"]])
    print("検索結果をまとめています...")
    summary = chat.get_summary(content)
    print("回答を生成しています...")
    print(chat.get_answer(summary))
    print("----------")
    print("参考情報：\n")
    for i, item in enumerate(res["items"]):
        print(f"{i}: [{item['title']}]({item['link']})")
