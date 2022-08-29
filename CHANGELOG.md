# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- added `Modeler` class
- added `RawChannel` class
- added `RawPinnedNote` class
- added `IReactionRequired` class

### Changed

- `Dict[Any, Any]` のような構文を typing モジュールを使わない `dict[any, any]` に変更
- `List[Any, Any]` のような構文を typing モジュールを使わない `list[any, any]` に変更
- `Channel` クラスを `RawChannel` を用いて作るように
- `PinnedNote` クラスを `RawPinnedNote` を用いて作るように
- change class name `PinnedNotePayload` -> `IPinnedNote`
- change class name `ChannelPayload` -> `IChannel`
- change class name `NotePayload` -> `INote`
- change class name `RenotePayload` -> `IRenote`
- change class name `ReactionPayload` -> `IReaction`

### Removed

- `RawRenote`, `Renote` クラスを削除しました。今後は `Note` クラスをご利用ください

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
