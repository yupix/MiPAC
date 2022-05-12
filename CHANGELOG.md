# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added

- utils.pyに `AuthClient` クラスを追加しました
- README.mdに使い方を追加

### Changed

- `Note` クラスの`created_at` 属性のtype hintを `Optional[str]` => `Optional[datetime]` に変更
- `Note` クラスの `cw` 属性の取得方法がgetではなかったので修正
 
### Removed

- 重複した属性を削除

