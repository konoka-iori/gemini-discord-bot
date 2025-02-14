# gemini-discord-bot

これは簡易的なDiscordチャットボットです。Geminiとの会話機能が実装されています。
[@konoka-iori](https://github.com/konoka-iori) が個人的に使用するために作成されました。主に小規模なDiscordサーバーでの利用を想定しています。
Gemini APIを使ったDiscordのチャットボット作ってみたいよという方への参考になれば幸いです。

# 機能一覧と使い方

## スラッシュコマンド

テキストチャンネルで以下のコマンドを入力することで、対応するBOTの機能を利用できます。

- `/about`: BOTの説明を表示します。
- `/ping`: BOTの生存確認を行い、応答速度を表示します。
- `/chat`: Geminiとチャットができます。一問一答方式で、会話履歴はBOT側で保存されません。

## ~~コンテキストメニュー~~

~~メッセージを右クリックされると表示されるメニューから「アプリ」を選択すると以下のコマンドが表示され、対応するBOTの機能を利用できます。~~

- ~~`Gemini replies to message`: すでに送信されているメッセージを選択してこのコマンドを使用すると、選択されたメッセージにBOTが返信します。一問一答形式で、会話はBOT側で保存されません。~~

> [!WARNING]
> この機能はCogs移行に伴い停止されています。
>
> 将来的に復活する可能性はありますが、しばらくの間利用できませんのでご了承ください。

# インストール方法

1. このリポジトリをクローンします。
2. `.env.sample` を `.env` にリネームします。
3. `.env` の `DISCORD_TOKEN` にDiscordのBOTのトークンを入力します。
4. `.env` の `GEMINI_API_KEY` にGeminiのAPI Keyを入力します。
5. 以下のコマンドを実行し、コンテナを起動します。

```shell
docker-compose -f .\.devcontainer\docker-compose.yml up -d
```

> [!CAUTION]
> **使用するときは必ず `.env.sample` を `.env` にリネームしてください。**
>
> `.env` は `.gitignore` に登録されているため、GitHubにアップロードされません。
>
> この操作を忘れ、 `.env.sample` にAPI Keyなどの情報を入力すると正常に動作しないどころか、うっかりGitHubにアップロードするとAPI Keyなどの重要な情報が漏洩する可能性があります。必ず `.env` にリネームしてから情報を入力してください。

## Discordの権限設定

このBOTを正常に動作させるには以下の権限が必須です。

SCOPES:

- bot
- applications.commands

BOT PERMISSIONS / TEXT PERMISSIONS:

- Send Messages
- Send Messages in Threads (スレッド内でもBOTを利用したい場合は必須)
- Embed Links
- Read Message History

# ブランチ命名規則

- `main`: 動作確認済みのブランチです。
- `develop`: 開発用のブランチです。こちらは動作確認が行われていません。
- `add/`: New Featureブランチです。新機能などの追加に使用します。`develop` から派生。
- `improvement/`: Improvement用ブランチです。既存の機能の改善に使用します。`develop` から派生。

# 注意事項

- このBOTは個人利用を想定して作成されています。
- このBOTはDiscordで動くものです。DiscordのアカウントやBOTの作成方法、利用規約、サーバーの作成方法などについては公式サイト等を確認してください。
- このBOTはGemini APIを利用しています。Geminiの概要、利用規約、APIの利用方法・API Keyの取得などについては公式サイト等を確認してください。
- 会話の内容が @konoka-iori に送信されることはありませんが、Gemini側で保存されて学習等に利用される場合があります。詳細は公式サイトを確認してください。
- このプロジェクトはみんな大好きMITライセンスです。BOTを使うときは自己責任で、かつこのリポジトリのURLを明記してください。詳細はLICENSEをご覧ください。
- 不具合報告、機能追加要望などはIssueください。Pull Requestも歓迎です！

# バージョン履歴

- [1.0](https://github.com/konoka-iori/gemini-discord-bot/pull/1):
  - 初版リリース（ `/about` と `/chat` の追加）
- [1.1](https://github.com/konoka-iori/gemini-discord-bot/pull/7):
  - ユーザーが送信した内容を返信に表示するよう改善 [#3](https://github.com/konoka-iori/gemini-discord-bot/issues/2)
- [1.2](https://github.com/konoka-iori/gemini-discord-bot/pull/10):
  - Pythonのバージョンを3.9から3.11に変更
  - 不具合修正 [#9](https://github.com/konoka-iori/gemini-discord-bot/issues/9)
- [1.3](https://github.com/konoka-iori/gemini-discord-bot/pull/12):
  - ドキュメントの拡充 [#6](https://github.com/konoka-iori/gemini-discord-bot/issues/6)
  - 不具合修正 [#11](https://github.com/konoka-iori/gemini-discord-bot/issues/11)
  - `/about` のEmbedを変更
  - EmbedのタイムスタンプをUTC時間に変換し、より正確なタイムスタンプを表示できるように対応
- [2.0](https://github.com/konoka-iori/gemini-discord-bot/pull/14):
  - 機能追加 [#2](https://github.com/konoka-iori/gemini-discord-bot/issues/2)
  - ドキュメント修正
- `[2.1](https://github.com/konoka-iori/gemini-discord-bot/pull/17):
  - JSONの形式を更新 [#15](https://github.com/konoka-iori/gemini-discord-bot/issues/15)
  - グローバルコマンドに対応
  - 依存関係を更新
  - **Gemini 1.5 Proに対応**
  - カスタムアクティビティに対応
  - 全体的なリファクタリングを実施
  - `/about` のEmbedを変更
  - ドキュメント修正
- [2.2](https://github.com/konoka-iori/gemini-discord-bot/pull/21):
  - `/ping` コマンドを追加 [#19](https://github.com/konoka-iori/gemini-discord-bot/issues/19)
  - 回答にかかった時間がEmbedに表示されるように変更
  - Embedのフッターとタイムスタンプを追加
  - `/about` のEmbedに `/ping` の説明を追加し、スラッシュコマンドのリンクを追加
  - 不具合修正（グローバルコマンドが正常に同期されない問題を修正）
  - コードのリファクタリング
  - ドキュメント修正（botの権限設定を追加）
- [2.3](https://github.com/konoka-iori/gemini-discord-bot/pull/30):
  - `/about` のレスポンスにこのリポジトリへのGitHubリンクを追加
  - 不具合修正 [#22](https://github.com/konoka-iori/gemini-discord-bot/issues/22)
  - README.mdに `/ping` の説明を追加 [#23](https://github.com/konoka-iori/gemini-discord-bot/issues/23)
  - ドキュメントの可読性向上（注意書き `CAUTION` を追加）
  - 不具合修正（レイテンシ計算を修正）
  - コードの可読性の向上（PEP8の適用、DocStringの拡充など）
  - Gemini APIの `system_instruction` メソッドに対応 [#18](https://github.com/konoka-iori/gemini-discord-bot/issues/18)
  - 不具合修正（ `.env` が正常に読み込まれない問題を修正）
  - Cogsに移行と大規模なリファクタリング
  - 依存関係を更新
- [2.4](https://github.com/konoka-iori/gemini-discord-bot/pull/37):
  - **Dockerに対応** [#29](https://github.com/konoka-iori/gemini-discord-bot/issues/29)
  - 脆弱性の修正 [#32](https://github.com/konoka-iori/gemini-discord-bot/pull/32) [#34](https://github.com/konoka-iori/gemini-discord-bot/pull/34) [#36](https://github.com/konoka-iori/gemini-discord-bot/pull/36)
  - 不具合修正 [#31](https://github.com/konoka-iori/gemini-discord-bot/issues/31)
  - `DISCORD_SERVER_ID` が不要に [#35](https://github.com/konoka-iori/gemini-discord-bot/issues/35)
  - 詳細なロギングに対応 [#33](https://github.com/konoka-iori/gemini-discord-bot/issues/33)
  - 全体的なリファクタリング
  - 依存関係を更新
- [2.5](https://github.com/konoka-iori/gemini-discord-bot/pull/41)
  - **Gemini 2.0 Flashに対応** [#39](https://github.com/konoka-iori/gemini-discord-bot/issues/39)
  - 脆弱性の修正 [#38](https://github.com/konoka-iori/gemini-discord-bot/pull/38)
  - 全体的なリファクタリングとエラー処理の改善
  - 依存関係を更新
