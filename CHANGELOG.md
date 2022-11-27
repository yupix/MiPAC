# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- `LiteUser` に属性 `name` を互換性の為に再追加しましたが、非推奨です。v0.4.0で削除する予定です
    - `username` と `name` の違いを区別しにくい可能性がある為、新たに使用する際は `nickname` を使用することを推奨しています

### Removed

- `deprecated_property` decorator を削除しました
- `deprecated_func` decorator を削除しました

## [0.2.1] - 2022-11-27

### Added

- `NoteActions` に `gets` メソッドが追加されました #MP-20
- Type Hintの追加

### Changed

- WebSocketを使用した際のレスポンスクラスを `MisskeyClientWebSocketResponse` クラス に
- `Reaction` クラスを `NotificationReaction` に変更しました
- `IUserLite` を `ILiteUser` に変更しました
- `LiteUser` の属性 `name` を `nickname` に変更しました。 `LiteUser` を継承しているクラスも同様に変更されていますのでご注意ください。

### Removed

- printを使用したデバッグログを削除しました

## [0.2.0] - 2022-11-02

### Added

- added `Modeler` class
- added `IReactionRequired` class
- added `IAds` class
- added `LiteInstance` class
- added `IReactionNf` class
- added `INote` class
- added `ICustomEmoji` class
- added `CustomEmoji` class
- added `InstanceMeta` class
- added `LiteInstanceMeta`
- added `IInstanceMetaLiteRequired` class
- added `IInstanceMetaLite` class
- added `IInstanceMeta` class
- added `IPage` class
- added `IPageRequired` class
- added `IUserDetailedField` class
- added `IUserDetailedRequired` class
- added `IUserDetailed` class
- added `ChatGroup` class
- added `ChatMessage` class
- added `IChatGroup` class
- NoteActionsクラスに `get` `fetch` メソッドを追加
- データをキャッシュするためのツールをutils.pyに追加
- orjsonが使用者の環境にある場合はjsonではなくorjsonを使用するようになりました
### Changed

- `Dict[Any, Any]` のような構文を typing モジュールを使わない `dict[any, any]` に変更
- `List[Any, Any]` のような構文を typing モジュールを使わない `list[any, any]` に変更
- `Channel` クラスを `RawChannel` を用いて作るように
- `PinnedNote` クラスを `RawPinnedNote` を用いて作るように
- change class name `PinnedNotePayload` -> `IPinnedNote`
- change class name `ChannelPayload` -> `IChannel`
- change class name `NotePayload` -> `INote`
- **BREAKING CHANGE** renamed `Client.action` to `Client.api`.

### Removed

- `Renote` クラスを削除しました。今後は `Note` クラスをご利用ください
- `IRenote`, `RenotePayload` クラスを削除しました。今後は `INote` クラスをご利用ください
- `RawEmoji`, `Emoji` クラスを削除しました。 今後は `CustomEmoji` クラスをご利用ください
- `EmojiPayload` クラスを削除しました。今後は  `ICustomEmoji` クラスをご利用ください
- `IReactionRequired`, `ReactionPayload`を削除しました。 今後は `IReactionNf` クラスをご利用ください
- `RawUser`, `User` クラスを削除しました。今後は `UserDetailed`, `LiteUser` クラスをご利用ください
- `RawInstance` クラスを削除しました。今後は `LiteInstance` クラスをご利用ください
- `RawProperties` クラスを削除しました。今後は `FileProperties` クラスをご利用ください
- `RawFolder` クラスを削除しました。今後は `Folder` クラスをご利用ください
- `RawFile` クラスを削除しました。 今後は `File` クラスをご利用ください
- `RawChat`, `Chat` クラスを削除しました。 今後は `ChatMessage` クラスをご利用ください
- `ChatPayload` クラスを削除しました。 今後は `IChatMessage` クラスをご利用ください
- `get_note` メソッドを削除しました。今後は `get` もしくは `fetch` メソッドをご利用ください
- `aiocache` を使用しないようになりました

### Fixed

- 一部の型が正しくないのを修正しました

## [0.1.0] - 2022-05-28

### Added

- `__all__` の定義
- utils.py に `AuthClient` クラスを追加しました
- `Config` クラスを追加しました
- `Client` クラスの引数に `config` を追加しました
- `FileActions` クラスを追加しました
- `FolderActions` クラスを追加しました
- README.md に使い方を追加

### Changed

- `Note` クラスの`created_at` 属性の type hint を `Optional[str]` => `Optional[datetime]` に変更
- `Note` クラスの `cw` 属性の取得方法が get ではなかったので修正
- **BREAKING CHANGE** `FileManager`, `FolderManager`, `DriveManager`の役割が変わりました
    - 例だと `FolderManager.get_files()` だったコードが `FolderManager.action.get_files()` と行ったふうに Actions クラスを経由するようになりました
- 開発者向け情報 `Folder` クラスの引数に `client` を追加しました

### Fixed

- config が無く動かなかった場所の修正
- 誤った型の修正

### Removed

- 重複した属性を削除
- 不要な import の削除
- 終わっている TODO を削除しました
