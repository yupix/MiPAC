# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- None

## [0.1.0] - 2022-05-28

### Added

- `__all__` の定義
- utils.pyに `AuthClient` クラスを追加しました
- `Config` クラスを追加しました
- `Client` クラスの引数に `config` を追加しました
- `FileActions` クラスを追加しました
- `FolderActions` クラスを追加しました
- README.mdに使い方を追加

### Changed

- `Note` クラスの`created_at` 属性のtype hintを `Optional[str]` => `Optional[datetime]` に変更
- `Note` クラスの `cw` 属性の取得方法がgetではなかったので修正
- **BREAKING CHANGE** `FileManager`, `FolderManager`, `DriveManager`の役割が変わりました
    - 例だと `FolderManager.get_files()` だったコードが `FolderManager.action.get_files()` と行ったふうにActionsクラスを経由するようになりました
- 開発者向け情報 `Folder` クラスの引数に `client` を追加しました
### Fixed

- configが無く動かなかった場所の修正
- 誤った型の修正

### Removed

- 重複した属性を削除
- 不要なimportの削除
- 終わっているTODOを削除しました
