# AllServer
## 概要
AllServerは、非常に低コスト・低負荷で動くマインクラフトサーバー提供システムです。

一つのサーバーに集中して、マインクラフトサーバーを動かすのではなく、たくさんのサーバ提供者にランダムにマインクラフトサーバーを立てるシステムです。

サーバーは、サーバーの一覧を持っているサーバー と マインクラフトサーバーを立てれるサーバーの二種類に分かれます
図

## 必要環境
- OS Linux/Windows/OS X
- Java(Minecraft バージョンに合っている)
- Python3(最新バージョン推奨)
Requests(ライブラリ)

## インストール方法
1. pipでライブラリをインストールする。
もし、pipが入ってない場合はapt(ubuntu)などで入れてください。
```
pip install requests
```
2. インストール先が正しくパーミッション・所有者が設定されていることを確認してください。<br/>
Linux : `ls -l`<br/>
Windows : `dir /q`
3. <a href="https://github.com/stsaria/allserver/archive/refs/heads/main.zip">ダウンロード</a>からソースコードをダウンロードします。
4. allserver.pyを起動します<br/>
```
python3 allserver.py
```
## サーバーの立て方