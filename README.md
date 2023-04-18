# MiPAC

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-axblack-8bd124.svg"></a>
<a href="https://www.codacy.com/gh/yupix/MiPAC/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yupix/MiPAC&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/c9bf85f195f94ab58bc72ad018a2be9f"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?
ref=badge_shield" alt="FOSSA Status">
<a><img src="https://img.shields.io/pypi/dm/MiPAC?label=PyPI"></a>
<img src="https://app.fossa.com/api/projects/
git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=shield"/></a>

## 概要

MiPAのCoreとなるライブラリです。

MiPACはMisskey v11, 12, 13をサポートしているApi Wrapperです。
本来気にしないといけないバージョンごとのAPIの違い等を吸収してくれます。

## サポートしているMisskey

|name|version|supported|
|---|---|---|
|[Misskey Official](https://github.com/misskey-dev/misskey)|v13, v12, v11|〇|
|[Ayuskey](https://github.com/teamblackcrystal/misskey)|v5, v6|〇|

## 使い方

```python
import asyncio

from mipac.client import Client

async def main():
    client = Client(url, token)
    await client.http.login()
    api = client.api
    note = await api.note.action.send('Hello World')
    print(note.author.name, note.content)

if __name__ == '__main__':
    asyncio.run(main())
```

### Migration from v0.3.0 to v0.4.0

#### configの属性が変更されました

- `is_official` が削除されました

##### **重要** `use_version` が追加されました

Misskeyではv11,v12,v13とバージョンがあり、バージョンによっては使用できないAPIがあったりします。MiPACでは`use_version`を指定することで事前に使用できるかどうかを確認し、使用できない場合は`NotSupportVersion`という例外を返します。このようにご自分のインスタンスのバージョンを書いていただくだけで、よくわからないエラーを事前に防ぐことが出来ます。（issue等にエラーを報告場合は必ず適切に設定されているか確認してください）

v13はまだリリースされて日が浅く、全てのインスタンスがアップデートしたとは考えにくいため、現在のデフォルト値は`12`となっています。

#### `Client` のオプションから `config`が削除されました

今後configを参照する際は `Client.config` を使用してください。
また、値を更新する場合はClient.config.from_dict()を用いることをお勧めします。
通常の変更方法との違いは以下の通りです。

```python
Client.config.is_ayuskey = True
Client.config.use_version = 13
Client.config.from_dict(is_ayuskey=True, use_version=13)
```

上記のように複数の値を同時に更新する場合特に`from_dict`は有効な方法になります。

### 注意事項

### 一部サーバー(インスタンス)のバージョンによっては正常に動作しない可能性があります

MiPACの特徴として、v11,v12,v13のバージョンごとに生じる変更点をなるべく気にしなくてよいように作成していますが、現状の最新版であるv13でもv13の中で削除されたり、増えたりした物があります。結果的に追従しきれていない箇所があることがあります。そのため、そのような物を見つけた場合は、使用しているサーバーのバージョンと使用できないエンドポイント名をIssueに送信してください。

### モデルを基本的に自分でインスタンス化することは推奨しません

MiPACのモデルでは多くの場合、キーワード引数に `client`を受け取り、それを用いて`api` プロパティを生成します。しかし、サポート途中の機能なのではそこが省かれ、リリース後にモデルのインスタンス化に必要な引数として `client` が追加されることがあります。また、他にもモデルの更新のために引数が変更される可能性があります。そのため、引数の変更に関することをCHANGELOG等で通知することはありません。

### 開発者向け情報

このプロジェクトでは [black](https://github.com/psf/black)のforkである、[axblack](https://github.com/axiros/axblack)を利用しています。主な違いはダブルクォートがデフォルトではなく、シングルクォートになっている点です

## LICENSE

準備中

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?ref=badge_large)

<p align="center">
    <a href="">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
