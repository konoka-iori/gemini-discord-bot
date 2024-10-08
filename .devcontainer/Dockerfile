FROM python:3.11-slim

# タイムゾーンをJSTに設定
ENV TZ Asia/Tokyo

# ユーザーを作成
RUN useradd -m gemini-discord-bot

# ワーキングディレクトリを指定
WORKDIR /home/gemini-discord-bot

# requirements.txtを先にコピーしてpip installを実行
COPY requirements.txt /home/gemini-discord-bot/requirements.txt

# pipで必要なパッケージをインストール
RUN pip install --upgrade pip && \
    pip install -r /home/gemini-discord-bot/requirements.txt

# 残りのファイルをコピー
COPY . /home/gemini-discord-bot

# ユーザーを切り替える
USER gemini-discord-bot

# コンテナ起動時に実行するコマンドを指定
CMD ["python", "src/bot.py"]
