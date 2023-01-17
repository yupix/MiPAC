# MiPAC

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-axblack-8bd124.svg"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=shield"/></a>

## 概要

MiPAのCoreとなるライブラリです。issueは[こちら](https://code.teamblackcrystal.com/projects/120/issues)で管理しています

MiPACはMisskey v11, 12, 13をサポートしているApi Wrapperです。
本来気にしないといけないバージョンごとのAPIの違い等を吸収してくれます。

## サポートしているMisskey

|name|version|supported|
|---|---|---|
|[Misskey Official](https://github.com/misskey-dev/misskey)|v13, v12, v11|〇|
|[Ayuskey](https://github.com/teamblackcrystal/misskey)|latest|〇|

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

##### `use_version` が追加されました

`is_official` ではv12とv13を区別するには不十分であったため、このように変更されました。v13がリリースされたばかりというのもあり、現状のデフォルト値はv12となっています。v13をご利用の方は`use_version=13`と指定するなどして、バージョンを変更してください。

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
