FROM python:3.11

# apt updateしてpipをインストール
RUN apt update && \
    apt upgrade -y && \
    apt install -y python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

# ユーザーを作成
RUN useradd -m gemini-discord-bot

# ワーキングディレクトリを指定
WORKDIR /home/gemini-discord-bot

# ユーザーを切り替える
USER gemini-discord-bot

COPY . /home/gemini-discord-bot

# pipで必要なパッケージをインストール
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# コンテナ起動時に実行するコマンドを指定
CMD ["python", "src/bot.py"]
