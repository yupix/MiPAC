# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- 以下のエンドポイントがサポートされます。
    - `emoji`
- `CustomEmoji` に `host` プロパティを追加
- `ClientManager` の属性に　`emoji` を追加

### Changed

- `mipac.util` モジュールは `mipac.utils` 配下の `auth`, `cache`, `format`, `log`, `util`の5つに分離しました。そのため `v0.5.0`で削除されます。
    - 今後は `mipac.utils.*` をご利用ください

### Removed

- `LiteUser` から `name` プロパティが削除されました。
    - 今後は `nickname` をご利用ください

## [0.4.2] 2023-03-22

### Added

#### `config.features` が追加されました

MiPACはv13, v12, v11という大きな区切りでエンドポイントが利用可能かを確認しています。その都合上、v13でサポートされいた物、例えばチャットが`13.7.0`で廃止されたような場合、MiPACは最新のMisskeyに追従しているため、デフォルトの挙動を変更します。これにより、`13.7.0`に更新してなかったり、`fork`を使用していてチャットが存在する場合でもチャットを使用すると例外である`NotSupportVersion`が発生してしまいます。その対策としてこの機能が追加されました。
このconfigの主な役割は以下の通りです。

- 最新のMisskeyでは使用できないが、自身が使用しているサーバーのバージョンでは使用できる場合に該当する物を有効にすることで例外を返さず、使用できるようにする

使い方は以下の通りです。また、現在サポートされているfeatureは`chat`のみです。

```py
async def main():
    client = Client(auth.currentUser.url, auth.currentUser.token)
    await client.http.login()
    api = client.api
    client.config.from_dict(features={'chat': True})
```

#### `config.limits` が追加されました

MiPACでは文字数等にデフォルトで最新のMisskeyの値を入れています。しかし、一部のForkで文字数の制限が緩和されている・制限されている場合に正しくエラーを返せなくなる可能性があります。その対策としてこの機能が追加されました。


また、自分で作成・使用しているForkでこれ存在するからデフォルトでサポートしてくれない？という物がありましたら、Issueを作成してくだされば検討します。

- Note周りのメソッドで`visibility`の型を正確に
- 以下のエンドポイントがサポートされます。
    - `i/claim-achievement`
    - `blocking/create`
    - `blocking/delete`
    - `blocking/list`
    - `admin/ad/create`
    - `admin/ad/delete`
    - `admin/ad/list`
    - `admin/ad/update`
- Added `IT_ACHIEVEMENT_NAME` fixed variable.
- Added class the given below.
    - Channel
        - `IChannelLite`
        - `ChannelLite`
        - `ChannelActions`
        - `ChannelManager`
    - Blocking
        - `BlockingUser`
        - `IBlockingUser`
        - `BlockingActions`
        - `BlockingManager`
    - Ad
        - `AdminAdvertisingModelActions`
        - `AdminAdvertisingActions`
        - `Ad`
        - `IAd`
        - `AdminAdvertisingModelManager`
        - `AdminAdvertisingManager`
- Added `block` attribute to `UserManager`.
- Added `channel` attribute to `ClientManager`.
- Added `reaction_emojis` property to `Note`.
- Added `reaction_acceptance` property to `Note`.
### Changed

- chatがv13で廃止された為v13を利用している際は例外を返すように変更しました。
    - v13だが、forkやchatが廃止される前のバージョンを使用していてチャットが使用したい際は新しい機能である `config.features` をご利用ください
- aiohttpのバージョンを `3.8.4`に固定
- Tokenを使用しなくてもAPIが一部使用できるようになりました。当然ですが、認証が必要なAPIを使用した場合はエラーが出ます。
- `Config.from_dict` の引数が全てキーワード引数になりました。これは今後Configに引数が増えた際など、変更に強くするためです。

### Removed

- サポートする気が無いため、sphinxを用いたドキュメントを削除

### Fixed

- `Note.reply`のキーが`renote`になっていて取得不可になっていた

## [0.4.1] 2023-03-14

### Added

#### バージョンの自動検出機能が追加されました（β）

これはデフォルトで有効になっており、有効の間は自動的に `/api/meta` からバージョンを推論します。機能としては以下の通りです

- 11, 12, 13にヒットした場合それらにバージョンを変更する
    - ヒットしなかった場合は何もしない
Misskey公式のバージョンニングを元に判断している為、独自のバージョニングを行っているフォーク等では正常に動作しない可能性があります。その際は `client.config.use_version_autodetect = False` とすることで無効にすることが可能です。また、手動でバージョンを設定する場合もoffにしてください。
一部のAPIはバージョンとフォークの種類で判断しています。そのため公式のバージョン的には使用できないが、フォークの機能として存在するという場合は報告をくださればサポートします。

- Added `role` property to `AdminManager`.
- Added `remove_none` argument to request method.
- Added method to`ClientActions` class the given below.
    - `get_announcements`
- Added class the given below.
    - `AdminUserActions`
    - `AnnouncementCommon`
    - `Announcement`
    - `AnnouncementSystem`
    - `IMetaAnnouncement`
    - `IAnnouncementSystem`
    - `AdminAnnouncementClientActions`
    - `AdminAnnouncementActions`
    - `AdminAnnouncementManager`
    - `IModerationLog`
    - `ModerationLog`
    - `ServerInfoCpu`
    - `ServerInfoMem`
    - `ServerInfoFs`
    - `ServerInfoNet`
    - `ServerInfo`
    - `IServerInfoCpu`
    - `IServerInfoMem`
    - `IServerInfoFs`
    - `IServerInfoNet`
    - `IServerInfo`
    - `ITableStats`
    - `IIndexStat`
    - `IndexStat`
    - `IUserIP`
    - `UserIP`
    - `FederationActions`
    - `FederationManager`
    - `IFederationInstanceStat`
    - `IFederationFollowCommon`
    - `IFederationFollower`
    - `IFederationFollowing`
- Roles
    - `IRolePolicieValue`
    - `IRolePolicies`
    - `IRole`
    - `RolePolicyValue`
    - `RolePolicies`
    - `Role`
    - `AdminRoleActions`
    - `AdminRolesManager`
    - `IRoleUser`
    - `RoleUser`
- Achievements
    - added `IAchievementNf` class.
    - added `NotificationAchievement` class.
    - added `Achievement` class.
    - added `get_achievements` method at `UserActions` class.
    - added `achievements` property at `UserDetailed` class.
- Note
    - content field auto convert empty string to None

### Changed

- Maximum number of characters has been changed from 79 to 99
    - The main reason for this change is to solve the problem that the MiPAC code is inevitably longer because of the method chain. We have kept it to the maximum of [pep8](https://peps.python.org/pep-0008/#maximum-line-length).
- Changed a method that was returning an `AsyncIterator` to return an `AsyncGenerator`.
    - Generator is more correct than Iterator because it is the correct usage.
- Changed class name the given below.
    - `IAnnouncement` -> `IMetaAnnouncement`
- `cache` decorator no longer uses `dynamic_args` decorator

### Removed

- Delete `dynamic_args` decorator.
- Delete debug log.

## [0.4.0] 2023-01-18

### Added

- added DocString.
- added `get_state` method at `ClientNoteActions` class.
- added `INoteState` class.
- added `NoteState` class.
- added `IBasePoll` class.
- added `ICreatePoll` class.
- added `MiPoll` class.
- added `PollManager` class.
- added `PollActions` class.
- added `AdminEmojiActions` class.
- added `AdminManager` class.
- added `AdminModeratorManager` class.
- added `ActiveUsersChart` class.
- added `IDriveChart` class.
- added `IDriveLocalChart` class.
- added `IDriveRemoteChart` class.
- added attribute `is_official` at `Config` class.
    - became `is_ayuskey` attribute is deprecated(I'll remove with v0.4.0)
- added `get_exception_from_id` function.
- Return an exception appropriate for the error encountered.
- [@omg-xtao](https://github.com/omg-xtao) added `users_search_by_username_and_host` method at `UserActions` class [#24](https://github.com/yupix/MiPAC/pull/24).
- [@omg-xtao](https://github.com/omg-xtao) added `note_translate` method at `UserActions` class [#24](https://github.com/yupix/MiPAC/pull/24).
- [@omg-xtao](https://github.com/omg-xtao) added `users_search` method at `UserActions` class [#24](https://github.com/yupix/MiPAC/pull/24).
- added new `ClientActions` class.
- added `avatar_color` property at `LiteUser` class.
    - Note: Since avatar_color is deprecated in v13, only None is returned for v13 instances.
- added `un_renote` method at `ClientNoteActions` class.
- added `get_children` method at `ClientNoteActions` class.
- added `invalidate` method at `FollowActions` class.
- added `cancel` method at `FollowRequestActions` class.
- added `mute` attribute at `UserManager` class.
- added `MuteManager` class.
- added `MuteActions` class.
- added `MuteUser` class.
- added `IMuteUser` class.
- added `AdminActions` class.
- added `ICustomEmojiLiteRequired` class.
- The following methods are added to the `AdminEmojiActions` class.
    - `gets`
    - `gets_remote`
- added some meta class.
    - `ICPU`
    - `IPolicies`
    - `IAnnouncement`
    - `IV12Features`
    - `IV11Features`
    - `IFeatures`
    - `IV12AdminMeta`
    - `ISharedAdminMeta`
    - `ILiteV12Meta`
    - `ILiteV11Meta`
    - `IMetaCommonV12`
    - `ICommonV11`
    - `IMetaCommon`
    - `ILiteMeta`
    - `IV12Meta`
    - `IMeta`
    - `IAdminMeta`
    - `Policies`
    - `Features`
    - `Meta`
    - `AdminMeta`
    - `CPU`
    - `MetaCommon`
    - `LiteMeta`
- added some federation class.
    - `IFederationInstanceRequired`
    - `IFederationInstance`
    - `FederationInstance`
- added some notification classes.
    - `Notification` 
    - `NotificationFollow`
    - `NotificationFollowRequest`
    - `NotificationNote`
    - `NotificationPollEnd`
    - `NotificationReaction`
    - `IUserNf`
    - `INoteNf`
    - `IPollEndNf`

### Changed

- rename `ActiveUsersChartPayload` class to `IActiveUsersChart` class.
- rename `DriveLocalChartPayload` class to `IDriveLocalChart` class.
- rename `DriveRemoteChartPayload` class to `IDriveRemoteChart` .class.
- rename `DriveChartPayload` class to `IDriveChart` class.
- The attribute `emojis` for Note and LiteUser is obsolete in misskey v13, so v13 will return an empty list.
- config is now a global variable.
    - If you want to change the config, please use `Client.config.from_dict`.
- CustomEmoji now inherits PartialCustomEmoji.
- PartialCustomEmoji url has been changed to return `str | None` to match v13.
- AdminManager's `get_invite` method has been moved to `AdminActions.
- **BREAKING CHANGE** `ClientActions` has been changed to `ClientManager`
- **BREAKING CHANGE** Some paths will be changed as follows
    - `manager.admin` -> `manager.admins`
    - `manager.admin.manager` -> `manager.admins.admin`
    - `actions.admin` -> `actions.admins`
- **BREAKING CHANGE**
    - The `action` property in the model has been changed to `api`.
        - Change `note.action.send` to `note.api.action.send`. 
    - Moved the reaction attribute of `ClientActions` to `NoteManager`.
        - Change `api.reaction` to `api.note.reaction`.
    - Moved methods from `AdminEmojiManager` to `AdminEmojiActions`.
        - Change `api.admin.emoji.add` to `api.admin.emoji.action.add`.
    - Moved methods from `AdminModeratorManager` to `AdminModeratorActions`.
        - Change `api.admin.moderator.add` to `api.admin.moderator.action.add`.
    - Moved methods from `ChartManager` to `ChartActions`.
        - Change `api.chart.get_active_user` to `api.chat.action.get_active_user`.
    - Moved methods from `FollowManager` to `FollowActions`.
        - Change `api.user.follow.add` to `api.user.follow.action.add`.
    - Moved methods from `FollowRequestManager` to `FollowRequestActions`.
        - `api.user.follow.action.get_all`.
    - Moved some attributes of `NoteActions` to `NoteManager`.
        - Change `api.note.action.reaction.add` to `api.note.reaction.action.add`.
    - Moved the reaction attribute of `NoteActions` to `ClientNoteManager`.
        - Change `api.note.action.reaction` to `api.note.reaction.action`.
        - Change `api.note.action.favorite` to `api.note.favorite.action`.

### Fixed

- can't delete emoji with v12.
- fixed `ChatMessage` model.
    - For v13, the url is automatically generated. (Although it returns None by type, it never actually returns None.
- fixed `Chat` action.
- fixed `Chat` action.

### Removed

- The following attributes have been removed `api.user.action.note`
- Delete `RawActiveUsersChart` class.
- Delete `RawDriveLocalChart` class.
- Delete `RawDriveRemoteChart` class.
- Delete `RawDriveChart` class.
- Delete `get_user` method at `FollowRequestActions` class.
- removed some meta classes.
    - `LiteInstanceMeta`
    - `IInstanceMetaLite`
    - `IInstanceFeatures`
    - `IInstancePolicies`
    - `InstanceMeta`

## [0.3.1] 2022-12-24

### Added

- added `NoteDeleted` class.
- added `INoteUpdatedDeleteBody` class.
- added `INoteUpdatedDelete` class.
- `str_to_datetime` 関数を追加

### Fixed

- `PartialReaction` クラスで `user_id` が取得できない
- `INoteUpdatedReaction` の型が間違っている

## [0.3.0] 2022-12-24

### Fixed

- fix `INoteUpdated` type

### Changed

- **BREAKING CHANGE** Required Python version is 3.11

## [0.2.8] 2022-12-23

### Added

- `LiteUser` に `action` プロパティを追加しました。
    - これにより `UserDetailed` の方から `action`が削除されていますが、`UserDetailed` は `LiteUser` を継承しているため今まで通りご利用いただけます
- `UserActions` クラスに `get_profile_link` メソッドを追加しました

## [0.2.7] 2022-12-23

### Fixed

- fix: TypedDict type error by [@omg-xtao](https://github.com/omg-xtao) in [#20](https://github.com/yupix/MiPAC/pull/20)

## [0.2.6] - 2022-12-08

### Added

- `INoteUpdated` クラスを追加しました
- `INoteUpdatedReactionBody` クラスを追加しました
- `INoteUpdatedReaction` クラスを追加しました
- `PartialCustomEmoji` クラスを追加しました
- `PartialReaction` クラスを追加しました

## [0.2.5] - 2022-12-08

### Added

- `ISignin` クラスを追加

### Fixed

- Noteモデルの `content` が無い場合KeyErrorになる
- Noteモデルの `cw` が無い場合KeyErrorになる

## [0.2.4] - 2022-12-08

### Added

- `ClientNoteManager` クラスを追加しました
- `ClientNoteActions` クラスを追加しました

### Changed

- `NoteActions` が持っているノートに対する操作を `ClientNoteActions` に移動しました
    - 継承しているため今まで通り使用できます

### Fixed

- sendメソッドの引数 `extract_hashtags` が正常に動作しない

## [0.2.3] - 2022-11-27

### Fixed

- `NoteAction.send` メソッドで作成したノートのモデルが生成できない
- `request` メソッドで戻り値がlistではなくdistだった場合snake caseに置き換えできない

## [0.2.2] - 2022-11-27

### Added

- `LiteUser` に属性 `name` を互換性の為に再追加しましたが、非推奨です。v0.4.0で削除する予定です
    - `username` と `name` の違いを区別しにくい可能性がある為、新たに使用する際は `nickname` を使用することを推奨しています

### Changed

- deprecatedに関する仕組みを変更しました。
    - 該当するコードを表示するようになっています

### Fixed

- 型の間違い等
- 使用しているインポートが`TYPE_CHECKING`の条件式の中に入っていた為使用できない
- `get_mention` メソッドで`username` ではなく`nickname`を使用していた為正しいmentionが作れない
- `LiteUser` クラスの属性`instance` でBotと同じインスタンスのユーザーの場合はNoneを返せずKeyErrorになる可能性があった
- `LiteUser` クラスの属性 `host` を取得すると KeyErrorになる可能性があった

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
