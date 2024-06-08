FROM python:3.11

# apt updateしてpipをインストール
RUN apt update && apt install -y python3-pip

# ワーキングディレクトリを指定
WORKDIR /app

COPY . /app

# pipで必要なパッケージをインストール
RUN pip install -r requirements.txt

# コンテナ起動時に実行するコマンドを指定
CMD ["python", "src/bot.py"]
