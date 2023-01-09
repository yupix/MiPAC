# MiPAC

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-axblack-8bd124.svg"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=shield"/></a>

## 概要

MiPAのCoreとなるライブラリです。issueは[こちら](https://code.teamblackcrystal.com/projects/120/issues)で管理しています

## サポートしているMisskey

- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Ayuskey latest](https://github.com/teamblackcrystal/misskey)

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

### Collaborators

<table>
    <tr>
        <td><img src="https://avatars.githubusercontent.com/u/50538210?s=120&v=4"></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/yupix">Author | @yupix</a></td>
    </tr>
</table>


### 開発者向け情報

このプロジェクトでは [black](https://github.com/psf/black)のforkである、[axblack](https://github.com/axiros/axblack)を利用しています。主な違いはダブルクォートがデフォルトではなく、シングルクォートになっている点です

# LICENSE

準備中

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPAC.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPAC?ref=badge_large)

<p align="center">
    <a href="">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
