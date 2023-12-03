# Contribution guide

Thank you for considering contributing to MiPAC!!!

## Issue

Check the going points before creating an assignment

- To avoid duplicates, please search for similar Issues
- Do not use Issue for questions, etc.
    - We welcome your questions in GitHub Discussion or on the Discord server in the README.


## About Brunch

- `master` is a branch intended for use in a production environment
- `develop` is the branch to work on for the next release
    - If you want to create a pull request, please send it to this branch

## Creating a pull request

- Create an Issue before creating a pull request.
- Please prefix the branch name with a keyword such as `feat` / `fix` / `refactor` / `chore` to identify the pull request as much as possible.  
    - Also, do not include changes other than to resolve the pull request issue
- If you have an Issue that will be resolved by a pull request, please include a link
- Any changes should be described in `CHANGELOG.md`. However, if there is no change from the user's point of view, there is no need to describe it.
- If possible, please use `flake8`, `mypy`, etc. to lint in your local environment.

Thank you for your cooperation.

## Notes

### About the Format

This project uses `axblack` and `isort` formatting. The difference between `axblack` and `black` is whether double or single quotes are used.

### About supported Misskey versions

- Ayuskey v5, 6
- Misskey v13, 12, 11

### 引数に関する例外について

Misskey側に渡すBodyにおいて、例えば `limit` に渡せる最大数が100だと分かっていても、MiPAC側で特別なことはしないものとする。これはAPIを叩いた際に帰ってくるエラーをより直接的に見れるようにするためです

### 引数のデフォルト値について

少し複雑な話になる為例を出しつつの説明になります。
例として `/api/channels/update` には `isSensitive` や `bannerId` といったキーを渡すことができます。では `update` メソッドを実際に作ってみましょう。

```python
    async def update(
        self,
        banner_id: str | None = None,
        is_sensitive: bool | None = None,
    ) -> :
    ...
```

まず、 `is_sensitive` に `None` が選べてしまうのは何か気持ち悪い所があります。次に`banner_id` は エンドポイント側がnullを許容している為、既に `banner_id` が設定してあった場合、`is_sensitive` のみを更新しようとした場合にnullに設定されてしまいます。また、`request` メソッドが持つ `remove_none=True` でNoneを消すことができますが、これでは `banner_id` を nullにする方法がなくなってしまします。

では、ここで`MISSING` を使って書き直します。

```python
    async def update(
        self,
        banner_id: str | None = MISSING,
        is_sensitive: bool = MISSING,
    ) -> :
    data = remove_dict_missing({
        "bannerId": banner_id,
        "isSensitive": is_sensitive
    })
    self._session.request(Route("POST", "/api/channels/update"), auth=True, json=data, remove_none=False)
    ...
```

`is_sensitive` のTypeHintsが `bool` のみにできるので気持ち悪さが解消されます。
また、 `remove_dict_missing` を使用することで `MISSING` のみを削除出来るため、Noneに設定したい場合は `await update(banner_id=None)` とすることで `banner_id` を null に設定できるようになります。注意点として、 `request` メソッドの `remove_none=False` に設定しないと `None` が削除されてしまうため気を付けてください。基本的に `/api/channels/create` のように作成系等では既にサーバー上にあるデータに留意する必要が無いため、`MISSING` ではなく `None` を使用しても問題ないです

