# MiPAC

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<a href="https://www.codacy.com/gh/yupix/MiPAC/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yupix/MiPAC&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/c9bf85f195f94ab58bc72ad018a2be9f"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?
ref=badge_shield" alt="FOSSA Status">
<a><img src="https://img.shields.io/pypi/dm/MiPAC?label=PyPI"></a>
<img src="https://app.fossa.com/api/projects/
git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=shield"/></a>

![Alt](https://repobeats.axiom.co/api/embed/b7734178610a63a16de4b789aa9b43d22686e390.svg "Repobeats analytics image")

## 概要

MiPA の Core となるライブラリです。

MiPAC は Misskey v11, 12, 13 をサポートしている Api Wrapper です。
本来気にしないといけないバージョンごとの API の違い等を吸収してくれます。

> 現在大規模な作業を行っています。詳細については[こちら](https://github.com/yupix/MiPAC/issues/94)を御覧ください。
> GitHub から何らかの理由でインストールする場合は以下のコマンドで `shared` ブランチを使用することをおすすめします。
> `pip install git+https://github.com/yupix/Mi.py.git@shared`

## サポート状況

サポート状況は [こちら](./compiler/datas/support_status.md) からご覧いただけます。もし使いたいエンドポイントがサポートされていない場合は Issue を作成することで優先的にサポートを行える可能性があります。

## 使い方

MiPAC には PyPi と独自のリポジトリの 2 つがあります、PyPi は比較的安定してからのリリースになりますが、独自のリポジトリはコミットごとにビルドが行われ公開されるようになっています。

お好きなほうをご利用いただけると幸いです。

https://onedev.akarinext.org/yupix/mipac-sync/MiPAC/~packages

```
#安定したビルド(推奨)
pip install mipac

#最新の成果物
pip install --extra-index-url https://onedev.akarinext.org/yupix/mipac-sync/MiPAC/~pypi/simple/ mipac
```

```python
import asyncio

from mipac.client import Client

async def main():
    client = Client(url, token)
    api = client.api
    note = await api.note.action.send('Hello World')
    print(note.author.name, note.content)

if __name__ == '__main__':
    asyncio.run(main())
```

### 注意事項

### 一部サーバー(インスタンス)のバージョンによっては正常に動作しない可能性があります

MiPAC の特徴として、v11,v12,v13 のバージョンごとに生じる変更点をなるべく気にしなくてよいように作成していますが、現状の最新版である v13 でも v13 の中で削除されたり、増えたりした物があります。結果的に追従しきれていない箇所があることがあります。そのため、そのような物を見つけた場合は、使用しているサーバーのバージョンと使用できないエンドポイント名を Issue に送信してください。

### モデルを自分でインスタンス化することは想定されていません

MiPAC のモデルでは多くの場合、キーワード引数に `client`を受け取り、それを用いて`api` プロパティを生成します。しかし、サポート途中の機能なのではそこが省かれ、リリース後にモデルのインスタンス化に必要な引数として `client` が追加されることがあります。また、他にもモデルの更新のために引数が変更される可能性があります。そのため、引数の変更に関することを CHANGELOG 等で通知することはありません。

## LICENSE

MiPAC is provided with [MIT LICENSE](./LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?ref=badge_large)

<p align="center">
    <a href="https://mipac.akarinext.org/ja/">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
