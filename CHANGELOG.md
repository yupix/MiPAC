# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2026-10-16

### <!-- 0 -->🚀 Features

- User周りを最新のMisskeyに追従 #148 ([2dd1fab](https://github.com/yupix/MiPAC/commit/2dd1fab4b43c18b321a84cf42bc6d44f78ca948d))
- Avatar decorationのモデルや型を追加 ([2aa3e96](https://github.com/yupix/MiPAC/commit/2aa3e9609710eb976a87af52871e03d42dbcdb1e))
- Admin/avatar-decorations/* をサポート ([43ad589](https://github.com/yupix/MiPAC/commit/43ad5897d69bc46c9b56fa9eb66f3119da14abe2))
- RolePoliciesを最新のものに #131 ([6c9e467](https://github.com/yupix/MiPAC/commit/6c9e467b198d00ef6ebebad9649b3a21caf06fdc))
- [**breaking**] Policies系のクラスを削除しRolePoliciesに置き換え ([cac07d1](https://github.com/yupix/MiPAC/commit/cac07d10654192cb5eb8c595e844469646221424))
- SystemWebhookの型とモデルを追加 ([30637e4](https://github.com/yupix/MiPAC/commit/30637e49c2e31e15f395e8de259fed894cf6d72a))
- AdminMetaを最新に追従 #131 ([d8e471e](https://github.com/yupix/MiPAC/commit/d8e471e5922cc621dd5981d82221cf695cac2b2a))
- Format code ([eec5b41](https://github.com/yupix/MiPAC/commit/eec5b411209cdb1bf05c1731a35838e65e75ab8a))
- Admin/metaのメソッドからdetailが消えてたので引数から削除 ([6d529f9](https://github.com/yupix/MiPAC/commit/6d529f9cf435ceae6276a64a7e144e1f0ce8d78b))
- Admin/system-webhook/* 系のエンドポイントをサポート ([cf99b06](https://github.com/yupix/MiPAC/commit/cf99b06cdbf304c6d78397d2b7fa34a9abdceef9))
- Driveモジュールの初期化ファイルを追加 ([d7fe348](https://github.com/yupix/MiPAC/commit/d7fe348c5b868034a1e66ed97c9495cb5895a1bb))
- エンドポイントリストを更新し、新しいAPIを追加 ([26512b1](https://github.com/yupix/MiPAC/commit/26512b137e08fe193e8a8d77150d321d0c287dc4))
- Create_note_body関数の引数をMISSINGに変更し、remove_dict_emptyをremove_dict_missingに更新 #155 ([3a5589f](https://github.com/yupix/MiPAC/commit/3a5589f48d6cce7aa07f2533a0771543e8c8491f))
- 最新のNoteモデルに追従 ([5b7f8c3](https://github.com/yupix/MiPAC/commit/5b7f8c31f82a18d3613669a387812218655acc95))
- Date系のページネーションをサポート ([b7fdf92](https://github.com/yupix/MiPAC/commit/b7fdf92440374920513b5622ef7d4daa4a87ab05))
- Openapiの変更検知スクリプトを更新 ([e2df95d](https://github.com/yupix/MiPAC/commit/e2df95d4a2deea4d0886f382aa08f9b1f04eaa57))
- `/api/admin/announcements/list` を最新に追従 ([c25a8af](https://github.com/yupix/MiPAC/commit/c25a8afb08eb73570453c5970c3854d007cdb358))
- `api/admin/accounts/find-by-email` をサポート ([0675a02](https://github.com/yupix/MiPAC/commit/0675a027b3c5f69decad35235733d12d6d8ca0ec))
- Adスキーマを最新に追従 ([945f540](https://github.com/yupix/MiPAC/commit/945f5407840e625a51208e5baa61de3737df0bc7))
- Note周りを最新のスキーマに追従 ([d9d2b4e](https://github.com/yupix/MiPAC/commit/d9d2b4ea1a21ae50352d65fc6d11305920e695d3))
- OpenAPI 変更検知スクリプトを作り直し ([b363424](https://github.com/yupix/MiPAC/commit/b3634247db54b0ea5886367f50c13b52faff7bf6))
- OpenAPI 定義を 2026.10.1-alpha.0 に更新 ([f77e03a](https://github.com/yupix/MiPAC/commit/f77e03a7eadfef1a5dd8da9586cb2e936582df78))
- Misskey 2026.10.1-alpha.0 のスキーマ変更に追従 ([5b1a8aa](https://github.com/yupix/MiPAC/commit/5b1a8aac235cf98e13c66d7906fed08b506f2dff))
- [**breaking**] API に存在しない引数・誤ったエンドポイントの使い方を修正 ([5c47194](https://github.com/yupix/MiPAC/commit/5c4719429dfec268710b6bae90d0def536575910))

### <!-- 1 -->🐛 Bug Fixes

- IFileのuser属性に誤ってモデルのクラスを使用している ([79d2732](https://github.com/yupix/MiPAC/commit/79d2732814139bf12c798c6061dc2e39e6d4ada3))
- 循環インポート ([4ac071d](https://github.com/yupix/MiPAC/commit/4ac071d1f2cb1a62915992d892983fe311d7b3ab))
- Int型のところがfloatになってる ([12af408](https://github.com/yupix/MiPAC/commit/12af408e32733b4ad0789fb850e894c8833823e8))
- ファイルパスを動的に設定するように修正 ([d2e5635](https://github.com/yupix/MiPAC/commit/d2e5635615a6e9aac666564c1d5cb1510a06754f))
- Contentプロパティを削除し、textメソッドを使用するように更新 ([370302b](https://github.com/yupix/MiPAC/commit/370302bfba2d91d03b9b11305fe8c10bcb4f7c56))
- Deleted_atのチェックを強化し、authorプロパティを削除してuserプロパティを使用するように更新 ([7c9945f](https://github.com/yupix/MiPAC/commit/7c9945f4de0a49990cba2c010736d8dac2586304))
- Typo ([060e83c](https://github.com/yupix/MiPAC/commit/060e83c3dfa3f2d5c227bd9bb5e90e0899044eea))
- `AnnoucementIcon` -> `AnnouncementIcon` ([66f8595](https://github.com/yupix/MiPAC/commit/66f8595af7413a9f78396ca791ee61d3f7ca0f99))
- Client.apiを呼ぶたびにClientManagerを生成していたのを修正 ([09699ad](https://github.com/yupix/MiPAC/commit/09699ad167444fe57a340947505a78661a08c346))
- Pyright で検出された型エラーを修正 ([003d443](https://github.com/yupix/MiPAC/commit/003d443e8ed9110beb7988fc7f712de9f2065fa9))
- Avatar-decorations のアクションで MISSING を送信していたのを修正 ([66d7cfc](https://github.com/yupix/MiPAC/commit/66d7cfc95940da07093a2f3adf02d2b10457c33a))
- 型とモデルを v13_api.json のスキーマに合わせる ([2ef6cca](https://github.com/yupix/MiPAC/commit/2ef6ccaf8ce78dab4f789b6f0ab89226a1c44acc))
- リクエストのキー名を v13_api.json に合わせる ([ea582a6](https://github.com/yupix/MiPAC/commit/ea582a63d023773d1cd370f21bc969974cb866d3))

### <!-- 2 -->🚜 Refactor

- Role and meta models and fix imports ([4d09893](https://github.com/yupix/MiPAC/commit/4d098936662f8eb352407a44276b8a2dc610932f))
- HTTPClientで__init__内でClientSessionを作らないでRequest時に適宜作るように ([862a95b](https://github.com/yupix/MiPAC/commit/862a95ba70001db85552c4d0187855108a04b5a1))
- Client*Actions を Shared*Actions の継承から合成に変更 ([a5b9a0a](https://github.com/yupix/MiPAC/commit/a5b9a0a2d96c3ea00bbe25ef497bfba5584a2956))
- [**breaking**] 存在しない /meta の emojis を参照していた ReactionActions.get_emoji_list を削除 ([0c8f412](https://github.com/yupix/MiPAC/commit/0c8f4126811a7a94cf62504d9147607acd4192df))

### <!-- 3 -->📚 Documentation

- サポート状況を更新 ([0dc8244](https://github.com/yupix/MiPAC/commit/0dc82443951812aca65e0dbfba4ec69aac134c3c))
- 古いCHANGELOG.mdを削除 ([b1c29ed](https://github.com/yupix/MiPAC/commit/b1c29ed5c63841aa942a1ff7fe7e10115e70ad02))
- FavoriteManager.action の戻り値の記載を FavoriteActions に修正 ([cb7dc57](https://github.com/yupix/MiPAC/commit/cb7dc575fd84e029b3893e629200598326d2ed05))

### <!-- 6 -->🧪 Testing

- Pytest を導入し CI で pyright とテストを実行するように ([817877b](https://github.com/yupix/MiPAC/commit/817877b37896a1bef441b4f5a2ad2593a5ad4e01))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- -を自動で_にするように ([ee2bd25](https://github.com/yupix/MiPAC/commit/ee2bd25d2cdcf2a406ef9789d27e7d7f964dabd3))
- Format code ([8af23b7](https://github.com/yupix/MiPAC/commit/8af23b7eabf1342c94d96f2ac07ff991d8c551fd))
- 使用していないimportを削除 ([5e5f8c8](https://github.com/yupix/MiPAC/commit/5e5f8c85f8f409b611a83e8d94bcff227badd40a))
- Code format ([d5a5fa5](https://github.com/yupix/MiPAC/commit/d5a5fa5fa5e0c44114fad331ecd91bda522a320e))
- ユーザーモデルを最新のものに追従 ([a07c650](https://github.com/yupix/MiPAC/commit/a07c6508dd12df62e88337aed57b678f60513ec2))
- いろいろ最新に追従 ([445484d](https://github.com/yupix/MiPAC/commit/445484d1bdd6ef7047301cad5bee288ed5e6b200))
- QODANAのCIを削除 ([16ebfdf](https://github.com/yupix/MiPAC/commit/16ebfdfec9f14fde750ae20dbfa15a3d321eec83))
- ページネーションタイプを自動判定できるように ([6f48e5d](https://github.com/yupix/MiPAC/commit/6f48e5d222c13df9440c6a1cef1043f55ff23a5b))
- 非推奨のAPIを削除 ([825a28e](https://github.com/yupix/MiPAC/commit/825a28eb4253f440f702c3bb942ced57331bcb31))
- 型を正確に ([cc751f4](https://github.com/yupix/MiPAC/commit/cc751f4ecb65c506b0b4aa07d0d61b2f5e60be90))
- Cache_key_builder からlru_cacheを外した ([90c0ff7](https://github.com/yupix/MiPAC/commit/90c0ff7d4a136905dcda79cfa8fc4adab25ad953))
- PRのCI対象ブランチを master から develop に修正 ([a9b9766](https://github.com/yupix/MiPAC/commit/a9b97660a95ad46de462f998bbe19715098ee29f))
- Json_or_text を関数の名前通りにJsonじゃ無い場合Textを返すうに ([414949c](https://github.com/yupix/MiPAC/commit/414949cf65126b29208ecc63122ba9c6125c8b7d))
- パッケージ管理を uv に移行 ([1720c20](https://github.com/yupix/MiPAC/commit/1720c207d1bfb6c828e8b5100f8ec3f63abc149e))
- Ruff の E501 / F401 の指摘を修正 ([3dda73f](https://github.com/yupix/MiPAC/commit/3dda73fbabd231ad4ef7a752dfaa25b8236dfb89))

## [0.7.4] - 2024-10-10

### <!-- 0 -->🚀 Features

- Accounts/createでsetupPasswordパラメータを使用できるように ([8b51a98](https://github.com/yupix/MiPAC/commit/8b51a98414130984bc56cd8298558118efb04e14))
- Admin/ad/update の必須引数を ad_id のみに ([e750ab2](https://github.com/yupix/MiPAC/commit/e750ab2ddd15d6735dbb0aca507d00b5e9f2c66d))
- Admin/resolve-abuse-user-report のパラメーターを最新のものに追従 ([83d348c](https://github.com/yupix/MiPAC/commit/83d348ceb8ddf1a3b7202ec4b806550bab6bbfb8))
- エラーを最新のものに更新 ([a0c9c5e](https://github.com/yupix/MiPAC/commit/a0c9c5e6d7bf92cae967681a338ee672098dd1d1))
- Admin/roles/updateの必須引数を role_id のみに ([b025d0a](https://github.com/yupix/MiPAC/commit/b025d0a391f9fd344aa833bc577eef387a4ee386))
- Compiler/data系を更新 ([065b79d](https://github.com/yupix/MiPAC/commit/065b79d4a97b2c4b7039b9de67b64cc1df35a009))

### <!-- 1 -->🐛 Bug Fixes

- Cacheにキーがなかった場合の動作がない ([dcd1269](https://github.com/yupix/MiPAC/commit/dcd126976f89ebca1613c40333cb555ed895e80a))
- Fetchとgetメソッドの責務が逆になっている close #149 ([f4220ac](https://github.com/yupix/MiPAC/commit/f4220ac8996d49d2d673c3675222d3558c3b9e5f))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Git-cliffの設定を変更 ([f4faa67](https://github.com/yupix/MiPAC/commit/f4faa670271a2b75b0229fe0f71f6c8341bb453c))

## [0.7.3] - 2024-10-08

### <!-- 7 -->⚙️ Miscellaneous Tasks

- コミット漏れ ([a75c050](https://github.com/yupix/MiPAC/commit/a75c05027218609bdc6b6dc0472a9886094bc801))

## [0.7.2] - 2024-10-08

### <!-- 0 -->🚀 Features

- [**breaking**] 本来v0.7.0で消す予定のクラスを消し忘れていたので削除 close #100 ([5ecc256](https://github.com/yupix/MiPAC/commit/5ecc256969748fff701c28b055900bf3967ebb2b))

### <!-- 1 -->🐛 Bug Fixes

- キャッシュの上限を超えノードが削除されたときにエラーが発生する #147 ([8a2f586](https://github.com/yupix/MiPAC/commit/8a2f586379ca2466b85c7e687755a88fda414768))

## [0.7.1] - 2024-08-18

### <!-- 0 -->🚀 Features

- キャッシュシステムをFIFOからLRUに変更 close #145 ([d8b1c8d](https://github.com/yupix/MiPAC/commit/d8b1c8d9ef3802c5b72297bf7b627faded9372b6))

## [0.7.0] - 2024-06-25

### <!-- 0 -->🚀 Features

- Loginメソッドを非推奨に & クラス作成時にセッションを作るように close #132 ([8e3ef19](https://github.com/yupix/MiPAC/commit/8e3ef19c6ba4d7ef7d53e21b75a51b912a8ced6f))
- 作成したユーザーを表すモデルを追加 ([cf9460f](https://github.com/yupix/MiPAC/commit/cf9460f3a887eb8193b1fe69f559d8a8ef5aad6f))
- AdminAccountActions.create メソッドの戻り値に `CreatedUser` を使うように ([4cdc1d8](https://github.com/yupix/MiPAC/commit/4cdc1d8820b792edbaa0ed5ae03c1febb42c1338))
- /hashtags/* をサポート ([a8f61b4](https://github.com/yupix/MiPAC/commit/a8f61b48a5c7f8a63327b802d867ccbb345b48e4))
- Errors compiler ([ebb6bb5](https://github.com/yupix/MiPAC/commit/ebb6bb503e7dff39afe50e1899d136e13c943667))
- IAntennaReceiveSource に users_blacklistを追記 ([0fce39c](https://github.com/yupix/MiPAC/commit/0fce39c43aa1b82df09c5b2b9bc4fe4513039ee3))
- Docstringを追加 ([2b032ac](https://github.com/yupix/MiPAC/commit/2b032ac168b607620fb1986f1309208a48de5456))
- 文字列の長さを確認するための関数を追加 ([bf0b3d9](https://github.com/yupix/MiPAC/commit/bf0b3d95f5602c3405f023e63fc9621f73f2f2ce))
- サポート状況を更新 ([3d5b3d9](https://github.com/yupix/MiPAC/commit/3d5b3d9dfc3f1c96b2e494aa710e054748d52a89))
- Announcement周りを最新の環境に追従 ([a9a3b12](https://github.com/yupix/MiPAC/commit/a9a3b12bda948b7176b661806d331a8c4d5b9a3c))
- サポート状況を更新 ([08522a3](https://github.com/yupix/MiPAC/commit/08522a306f862a60132f8e9ac2f5baa63ee12626))
- Urlのパスを使用しないように close #138 ([051a1f5](https://github.com/yupix/MiPAC/commit/051a1f574faf81ba34d13818ddb69ebd65c6b43a))
- ロールを最新に追従 ([0a42264](https://github.com/yupix/MiPAC/commit/0a42264958f36d14ee1f080edd8774fb44fa5d48))
- アプリに関する型とモデルを追加 ([3f8b330](https://github.com/yupix/MiPAC/commit/3f8b3303dce1ef2cd0f5ce901f6a0c8dd1cf1f30))
- アプリに関するmanagerとactionを作成 ([d18a9a2](https://github.com/yupix/MiPAC/commit/d18a9a2c022ec310d76899f931516935cdc724c1))
- ID用の型とモデルを追加 ([e3fdbcf](https://github.com/yupix/MiPAC/commit/e3fdbcf4687b6404199c324c0342ef292a32915c))
- Admin/emojiを最新のものに追従 ([5f1d290](https://github.com/yupix/MiPAC/commit/5f1d290dbf441084c4a05d4d8c23aa91cb898434))
- EmojiDetailedモデルにapiプロパティを追加 ([502cd29](https://github.com/yupix/MiPAC/commit/502cd299dab29ecb2160ea248ad0dd88e5b13ab7))
- サポート状況を更新 ([f5b527e](https://github.com/yupix/MiPAC/commit/f5b527e09483637aa377c97fa9a07268b07ecd66))
- 翻訳ファイルの更新 ([fb8a617](https://github.com/yupix/MiPAC/commit/fb8a6175b389b06cdf5376eac659372bb915c2d3))
- [**breaking**] ClientNoteActionsの対象のIDを指定する引数を削除 #140 ([6d114a3](https://github.com/yupix/MiPAC/commit/6d114a35b65a7a31e55107c7e0771b4023e81f15))
- [**breaking**] ClientUserActionsの対象のIDを指定する引数を削除 #140 ([f6c7153](https://github.com/yupix/MiPAC/commit/f6c715343b3d8af20e7ac49670373dfaa2bccb59))
- [**breaking**] ClientAntennaActionsの対象のIDを指定する引数を削除 #140 ([c9e52cc](https://github.com/yupix/MiPAC/commit/c9e52cc506f3a9d2afca82ca5a839200f9efbf04))
- [**breaking**] ClientBlockingActionsの対象のIDを指定する引数を削除 #140 ([75f96de](https://github.com/yupix/MiPAC/commit/75f96de6ad9c09085bcb2b71100d1faf7b1e1621))
- [**breaking**] ClientChannelActionsの対象のIDを指定する引数を削除 #140 ([a11c9ea](https://github.com/yupix/MiPAC/commit/a11c9ea5d20e7ec2efac7de928bd254898938dd9))
- [**breaking**] ClientClipActionsの対象のIDを指定する引数を削除 #140 ([a217f3d](https://github.com/yupix/MiPAC/commit/a217f3d9769d9cdb441e877b08d8db67db3a7a36))
- [**breaking**] ClientFavoriteActionsの対象のIDを指定する引数を削除 #140 ([8077e2a](https://github.com/yupix/MiPAC/commit/8077e2adf5907bc6d7537d324ee2485d0a6b69a3))
- [**breaking**] ClientFollowActionsの対象のIDを指定する引数を削除 #140 ([da6a14d](https://github.com/yupix/MiPAC/commit/da6a14df3fbfc81691b40f7d0b7b16b5cf3bb159))
- [**breaking**] ClientInviteActionsの対象のIDを指定する引数を削除 #140 ([1992fb3](https://github.com/yupix/MiPAC/commit/1992fb399ee6618e94505af223219ff39dd4bc1f))
- [**breaking**] ClientPollActionsの対象のIDを指定する引数を削除 #140 ([54a0ac6](https://github.com/yupix/MiPAC/commit/54a0ac660e177dbd92f44101185a2c429ada1758))
- [**breaking**] ClientReactionActionsの対象のIDを指定する引数を削除 #140 ([4f965fe](https://github.com/yupix/MiPAC/commit/4f965fe1e62f3142acde30e662446c0d685eaf31))
- [**breaking**] Client*UserListActionsの対象のIDを指定する引数を削除 #140 ([7e40adb](https://github.com/yupix/MiPAC/commit/7e40adbb26be43823f36aef52865fd7091b11911))
- [**breaking**] ClientMuteActionsの対象のIDを指定する引数を削除 #140 ([61257ad](https://github.com/yupix/MiPAC/commit/61257ad655d63b97baa4dcdf149f2bec08f24643))
- [**breaking**] ClientFileActionsの対象のIDを指定する引数を削除 #140 ([9d9b509](https://github.com/yupix/MiPAC/commit/9d9b50916d59e2cd2723fc907d14f093dcfad7fc))
- [**breaking**] ClientFolderActions の対象のIDを指定する引数を削除 #140 ([62d21e5](https://github.com/yupix/MiPAC/commit/62d21e5861ee7a3368a3b91dbc5f93ed5a8a2974))
- [**breaking**] ClientAdminAdActions の対象のIDを指定する引数を削除 #140 ([520da59](https://github.com/yupix/MiPAC/commit/520da59a4718433a68761da1aa87cfe9e2cec034))
- [**breaking**] ClientAdminAnnouncementActions の対象のIDを指定する引数を削除 #140 ([a6c8fd9](https://github.com/yupix/MiPAC/commit/a6c8fd92bda836cc94be5b5fd3a78c4ccd699763))
- [**breaking**] ClientAdminEmojiActions の対象のIDを指定する引数を削除 #140 ([37aa930](https://github.com/yupix/MiPAC/commit/37aa9300586505d816f21ec4aa9312c15d5be1f5))
- [**breaking**] ClientAdminRoleActions の対象のIDを指定する引数を削除 #140 ([db28252](https://github.com/yupix/MiPAC/commit/db282522922e31d809467e6824790532590a4eac))
- [**breaking**] ClientAdminUserActions の対象のIDを指定する引数を削除 #140 ([69103b0](https://github.com/yupix/MiPAC/commit/69103b09db266601d36f1cce7c04f611fdba3d43))
- [**breaking**] Client*Actionsで 対象のIDを指定する引数を削除 #140 ([08744e6](https://github.com/yupix/MiPAC/commit/08744e68ac7415a34c98b69930363ffca5c8480d))
- サポートしてる範囲でモデルを最新に追従 ([77b665b](https://github.com/yupix/MiPAC/commit/77b665b56c4147eb3abdde3615779ea06cf1f0ce))
- Release v0.7.0 ([b6bd49e](https://github.com/yupix/MiPAC/commit/b6bd49e727e811fc1738adf1a15c26e6f0e707bd))

### <!-- 1 -->🐛 Bug Fixes

- Typo ([663912a](https://github.com/yupix/MiPAC/commit/663912a73a53c2026d9924b1e6e9ce50aa33623b))
- Mipactlのmanagerでactionを毎度作成しないように ([0ad9c7e](https://github.com/yupix/MiPAC/commit/0ad9c7e1eb19e421bcb6f3dc7078bd48b0651434))
- EmojiDetailedからlicenseが欠落している ([f85be9b](https://github.com/yupix/MiPAC/commit/f85be9ba94ad4d11f89b9504ae9fec4985d2f536))
- 循環参照を修正 ([651243b](https://github.com/yupix/MiPAC/commit/651243bf96c72989f3c227b871e161852618ca8c))
- AdminEmojiActionを複数形に ([4ebe597](https://github.com/yupix/MiPAC/commit/4ebe597e427bb82b2245eb7b5f6f6f1d8463d780))

### <!-- 3 -->📚 Documentation

- サポート状況についてREADMEで触れるように ([66dc7df](https://github.com/yupix/MiPAC/commit/66dc7df1bffdbeb214574e43e02ac7ff882c5655))
- Update documentation ([06ba45e](https://github.com/yupix/MiPAC/commit/06ba45e975ed5c162fc636206970b9ffcc299c8a))
- CHANGELOG.mdの生成にgit-cliffを使うように ([cb25c92](https://github.com/yupix/MiPAC/commit/cb25c92e5304cccc86d446358b2ad485357a1c01))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- 消し忘れていたget_all引数を削除 ([f0ce0b0](https://github.com/yupix/MiPAC/commit/f0ce0b0727567047c06608a1eb6ecae748fb96c8))
- Docstringをformat ([ff6836b](https://github.com/yupix/MiPAC/commit/ff6836bf94f40048a2f81769c77e2be4aa2811aa))
- Configから使用されていないものを削除 ([ed8275a](https://github.com/yupix/MiPAC/commit/ed8275a987d06b1c789c6e87b179c79bb11e4605))
- Configでaccount_idを保持しないように ([ca30721](https://github.com/yupix/MiPAC/commit/ca30721dda8490b9b7e1af458cfcf1fa69ed76f3))
- 使用していなかったget_cache_key関数を削除 ([87ea957](https://github.com/yupix/MiPAC/commit/87ea95775e046d5a6d37fdd18ef67183480889c3))
- Utils.formatで使用されていない関数を削除 ([7d062ba](https://github.com/yupix/MiPAC/commit/7d062bac8c34a35b99e331929cf3da4100e0db88))
- Update docstring ([5bd1c4d](https://github.com/yupix/MiPAC/commit/5bd1c4dc5db1134b736901cf6b2734d4ffc7e8de))
- Update docstring ([e495856](https://github.com/yupix/MiPAC/commit/e495856384da9ffe991b3744f18beaa3be54c5a7))
- Add example ([169f171](https://github.com/yupix/MiPAC/commit/169f1713c94294f0920bdbca73f2301283dc0ac7))
- NotificationRecieveConfig周りの更新 ([de5f88d](https://github.com/yupix/MiPAC/commit/de5f88dbf44347c47c41c2599e1057ba9fb5db93))
- IUserの型を変更 ([be56154](https://github.com/yupix/MiPAC/commit/be56154ef80e08733ff8b2c227d3d8aa94ccf664))
- Noteモデルに追加された reaction_emoji をサポート ([cf0286e](https://github.com/yupix/MiPAC/commit/cf0286e62cb1ec2b3c24e6599f7de95633d9cf5f))
- Api.jsonを2024.3.1に更新 ([058214d](https://github.com/yupix/MiPAC/commit/058214daa2ca7fc402b9884ffcba4edaf630cb73))
- Support_status.md で misskey のバージョンを表示するように ([91db9f3](https://github.com/yupix/MiPAC/commit/91db9f341ebab3cf89ea8588d4e03ba6131dfa3b))
- サポート状況を更新 ([a76f91c](https://github.com/yupix/MiPAC/commit/a76f91cbd28ad51678d6cf722001259fc652eaac))
- Errors.csvはバージョン管理する必要無いので削除 ([b7f56d6](https://github.com/yupix/MiPAC/commit/b7f56d671960cfea52d8ea94ce1057e46935ecbd))
- Update errors ([24ba7f7](https://github.com/yupix/MiPAC/commit/24ba7f777f957d30c5cfa8a6c922d19e3891a428))
- DocStringを更新 ([631fd2b](https://github.com/yupix/MiPAC/commit/631fd2b186c3e4926527140be955396bb37fa540))
- Format ([e09736b](https://github.com/yupix/MiPAC/commit/e09736b4a65d5385d959aad0738ef1bb9a7e4b00))
- Format ([98d59f9](https://github.com/yupix/MiPAC/commit/98d59f962f30a570dc097b81754428cc181f11fe))

## [0.6.3] - 2024-02-24

### <!-- 0 -->🚀 Features

- PartialUserに_get_mentionプロパティを追加 ([0e8f8b4](https://github.com/yupix/MiPAC/commit/0e8f8b4de67a9f90471527c48e3f4ceca718539e))
- ClientAdminUserManagerにaccountを追加 ([3ff41ca](https://github.com/yupix/MiPAC/commit/3ff41cac106579bb57ff9ce655fe71e1429bf9b1))
- Release v0.6.3 ([c813396](https://github.com/yupix/MiPAC/commit/c813396e7f7517b4f091699495d91fcdc59a6dd7))

### <!-- 1 -->🐛 Bug Fixes

- インスタンス変数にアクセスできない ([1056071](https://github.com/yupix/MiPAC/commit/105607133c35752b53754567128688cc80bbf40d))

### <!-- 3 -->📚 Documentation

- Update rst & po ([b8f6937](https://github.com/yupix/MiPAC/commit/b8f6937165cbf237e847d69b6d953433fbce2900))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- UserActions.get_mention メソッドを非推奨に ([26d0f4e](https://github.com/yupix/MiPAC/commit/26d0f4ea87e3a11777542b6b2014832f272abe92))

## [0.6.2] - 2024-02-21

### <!-- 0 -->🚀 Features

- Get_all_search_by_tag メソッドを追加 ([9d07afb](https://github.com/yupix/MiPAC/commit/9d07afb8668b8360f88baba750203b613da5a8ed))
- AdminAccountActionsを追加 ([60eaad7](https://github.com/yupix/MiPAC/commit/60eaad7dbeff8a62b5532d3c655ae8afaa3c4266))
- Userに対する管理アクションを容易に行えるように ([9785774](https://github.com/yupix/MiPAC/commit/97857747594506d24b5d6cfbc599985d2095f7ba))
- Release v0.6.2 ([1675f52](https://github.com/yupix/MiPAC/commit/1675f5216bbca44094cd5a641490b167a6ae1ffc))

### <!-- 2 -->🚜 Refactor

- AdminUserActionsをClientと分けた ([5297559](https://github.com/yupix/MiPAC/commit/529755930b083d46ce84ad035f6e3684228c592f))
- AdminActionsがSharedAdminUserActions を継承するように ([d37c7ae](https://github.com/yupix/MiPAC/commit/d37c7ae0588052b883f63458eeaaa83dcf8df809))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- 使用されていない例外を削除 ([80980cf](https://github.com/yupix/MiPAC/commit/80980cf263f2ee97f6e43726461a0b1f0f58efcb))
- サポート状況を更新 ([82cca9c](https://github.com/yupix/MiPAC/commit/82cca9cfcc0d1255ae9500a952fc9c2f5aab5617))

## [0.6.1] - 2024-02-21

### <!-- 0 -->🚀 Features

- FollowActionsをClientと分けた ([dc00a0e](https://github.com/yupix/MiPAC/commit/dc00a0e39543c2cb3edb5a5aee1917cd17bf4aac))
- Notes/search をサポート ([f3d04fb](https://github.com/yupix/MiPAC/commit/f3d04fb96887d9553762eacba958dc8b2b7728f0))
- Release v0.6.1 ([dc623e0](https://github.com/yupix/MiPAC/commit/dc623e05b2e5a2f61e40d8c653f96cbdab35d37d))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- FollowManagerでActionを再生成しないように ([bb93d03](https://github.com/yupix/MiPAC/commit/bb93d034c4b200e5d14a4a02e15da242f9c34827))
- FollowActions.add メソッドを非推奨に、代わりにcreateメソッドを追加 ([69c89a7](https://github.com/yupix/MiPAC/commit/69c89a79e1e02bc10286b179614f649662bc396c))
- FollowActions.remove メソッドを非推奨に、代わりにdeleteメソッドを追加 ([df2ba4f](https://github.com/yupix/MiPAC/commit/df2ba4f6744d56c059baed60f41c90d2990734e3))
- サポート状況を更新 ([be5e608](https://github.com/yupix/MiPAC/commit/be5e608f02a3a200fd19e9030e6fc5c7a3c85598))

## [0.6.0] - 2024-02-20

### <!-- 0 -->🚀 Features

- Channel周りの型とモデルを作り直した ([850e800](https://github.com/yupix/MiPAC/commit/850e8006bf9e5cd9d9d1d6b04277a0176e1bcba6))
- /channels/update をサポート ([8fc4ed3](https://github.com/yupix/MiPAC/commit/8fc4ed3dd96194855d7d2e8b50f11a059b3e57a7))
- /channels/favorite をサポート ([7122432](https://github.com/yupix/MiPAC/commit/712243277fc55b71eca2bef908610786eaf99b7c))
- /channels/unfavorite をサポート ([71ada21](https://github.com/yupix/MiPAC/commit/71ada2127e322026557b761da0fc3db305ee1a39))
- /channels/my-favorites をサポート ([bb30b47](https://github.com/yupix/MiPAC/commit/bb30b475888bf9fab68507921afdb18f21adb6e3))
- /channels/search をサポート ([90725ba](https://github.com/yupix/MiPAC/commit/90725ba4508d282e472c9e0396605c09f77f7040))
- AvatarDecoration モデルを追加 ([ce9a91f](https://github.com/yupix/MiPAC/commit/ce9a91f1115b9dfb876989136f813a64234d4666))
- UserDetailedNotMeOnly モデルを追加 ([7b98f66](https://github.com/yupix/MiPAC/commit/7b98f66bc43e6df688c09db0bdab8773c938f45b))
- Announcementに関するモデルと型を作り直した ([d4c434d](https://github.com/yupix/MiPAC/commit/d4c434d0240fbb33681fa8047d2b1cc87926ea52))
- Get_all_notesメソッドを追加 ([8d6358c](https://github.com/yupix/MiPAC/commit/8d6358c8cf10afc805461e00cf33b6c5366c0d1c))
- UserActionsをClientと分けた ([171f60b](https://github.com/yupix/MiPAC/commit/171f60bea47b1112d4d53c94872fafcb50c0db80))
- ClientUserManagerを追加 ([e91617c](https://github.com/yupix/MiPAC/commit/e91617c4c38f4e5251ec66bd755750801af864b9))
- Followに関するモデルを追加 ([80be00c](https://github.com/yupix/MiPAC/commit/80be00c0b6de15d958781e9cf0f5eeec2cc1cb96))
- PartialUserでClientUserManagerを使うように ([827a671](https://github.com/yupix/MiPAC/commit/827a671cb1988b7193f2798c80120563014242df))
- /api/users/followers をサポート ([08f5515](https://github.com/yupix/MiPAC/commit/08f551575fa973f16e3110699ef1c569e0134071))
- /api/users/following をサポート ([3b5d1ef](https://github.com/yupix/MiPAC/commit/3b5d1efb83aa579f1fd1f509464d8cddd29f17a6))
- GalleryPostモデルを追加 ([957db2a](https://github.com/yupix/MiPAC/commit/957db2ad044dbfa4c25a6016cc63bc9ab4d823e0))
- /api/users/gallery/posts をサポート ([bc844eb](https://github.com/yupix/MiPAC/commit/bc844eb0e19ad8dec56c2104d0a078e768469039))
- FrequentlyRepliedUser モデルを追加 ([403dea0](https://github.com/yupix/MiPAC/commit/403dea0760ab70d80ba2059901bcf2889491a3fc))
- /api/users/get-frequently-replied-users をサポート ([9c62357](https://github.com/yupix/MiPAC/commit/9c623577a8237dc6b3b3952a7b2df9cc215f1679))
- /api/users/featured-notes をサポート ([9285a59](https://github.com/yupix/MiPAC/commit/9285a5976e4494c9c7fe702c2acf3e5330a05c9f))
- UserListモデルを追加 ([d2ffc3a](https://github.com/yupix/MiPAC/commit/d2ffc3aaba50528cf28cc797f3ef62598d6a9e68))
- /api/users/lists/createをサポート ([5b4f535](https://github.com/yupix/MiPAC/commit/5b4f535d80ec920bdc5fb1ddeda07273efccd9c5))
- /api/users/lists/delete をサポート ([b65bc9f](https://github.com/yupix/MiPAC/commit/b65bc9fd0b74724bdeb58fcffffbf1ec4a6a9845))
- ClientUserListManagerを追加 ([fea0f37](https://github.com/yupix/MiPAC/commit/fea0f37acb669b48ecacb08e90a6c29b18dfd6cd))
- /api/users/lists/list をサポート ([e7116e8](https://github.com/yupix/MiPAC/commit/e7116e89968ce2856189bf8a543f28cca8cd604c))
- Userlist周りでuser_idを使えるように微調整 ([ad0720b](https://github.com/yupix/MiPAC/commit/ad0720b9bd06cf2a283cd554334c2060a2d6545b))
- /api/users/lists/push をサポート ([ff2eea4](https://github.com/yupix/MiPAC/commit/ff2eea48655f5885cc01c2f090069e91be7f84b3))
- /api/users/lists/show をサポート ([4cf3b80](https://github.com/yupix/MiPAC/commit/4cf3b806e34e1ad261a9c5a3ee998ee484592549))
- /api/users/lists/favorite をサポート ([ddc122a](https://github.com/yupix/MiPAC/commit/ddc122a3925a372e7db0e3decab3c1ff072b874d))
- /api/users/lists/unfavorite をサポート ([081f50e](https://github.com/yupix/MiPAC/commit/081f50e24878e51770e215fb4044bafee928b80e))
- /api/notes/user-list-timelineをサポート ([44ccd07](https://github.com/yupix/MiPAC/commit/44ccd07f46b74bd7c70fcd97ded351e555393f60))
- /api/users/lists/update をサポート ([07931fd](https://github.com/yupix/MiPAC/commit/07931fd4ed6f35d2d77ec7104efb4b3671cd9988))
- /api/users/lists/create-from-public をサポート ([e6c4756](https://github.com/yupix/MiPAC/commit/e6c475655740d16ac0441c3c59276c1a8f68dfd6))
- /users/lists/update-membership をサポート ([9e5cd95](https://github.com/yupix/MiPAC/commit/9e5cd95c7891e67e1ce655bac5f78bf4ab5a021b))
- UserlistMembership周りのモデルを追加 ([64475fc](https://github.com/yupix/MiPAC/commit/64475fcab6fc12fa21fd1b08e779f2f34390d5e3))
- /users/lists/get-memberships をサポート ([77f2735](https://github.com/yupix/MiPAC/commit/77f2735bc85de97301871e96bd1d2523f6e44ca1))
- サポート状況を更新 ([5d9a40a](https://github.com/yupix/MiPAC/commit/5d9a40afd6c9fd48107e5da7e4b8f8bbe719c03a))
- サポート状況を更新 ([5e99257](https://github.com/yupix/MiPAC/commit/5e99257b415e7a0b26ed6f6c50c2d34074b8fad7))
- より良い品質のmarkdownを出すように ([ea1a0c6](https://github.com/yupix/MiPAC/commit/ea1a0c634cf2d094b1d9b4b3f2a7a06c79af9a46))
- Python3.12のジェネリックスの書き方に ([0ed9a99](https://github.com/yupix/MiPAC/commit/0ed9a99e6eb9d0d612042ab5d011b50cb0de839c))
- Pagination_iterator を削除 ([7167a5b](https://github.com/yupix/MiPAC/commit/7167a5b86b8b2df1bc0a6adaa5a9c1424de1fe29))
- [**breaking**] AbstractModelを廃止 ([3158d0e](https://github.com/yupix/MiPAC/commit/3158d0e4d08f0cb36ac12dfb35557872816cc4b5))
- Admin/ad/create の引数を最新のものに更新 ([e3b40ab](https://github.com/yupix/MiPAC/commit/e3b40ab1258db6184d120b6bda55727b8f974cad))
- Adモデルを最新のものに更新 ([7d99e22](https://github.com/yupix/MiPAC/commit/7d99e225302f09d0aa69c8f36745f4f7d0b34497))
- Admin/ad/update をサポート ([a7a7a13](https://github.com/yupix/MiPAC/commit/a7a7a138fd7e389628a8bf2237cc97b653b67b43))
- Notes/create のメソッドをcreateに変更 ([c50e83e](https://github.com/yupix/MiPAC/commit/c50e83ed3458aa8924180b04ac54c451dc31f7ec))
- Notes/conversation をサポート ([e53fd41](https://github.com/yupix/MiPAC/commit/e53fd41e7af8535eea4d37352d782b7d221ccf57))
- Notes/featured をサポート ([a569480](https://github.com/yupix/MiPAC/commit/a5694803abd0749b18b1a9079676934ca28d3515))
- Notes/hybrid-timeline をサポート ([41e8de3](https://github.com/yupix/MiPAC/commit/41e8de38bacf0ca94d2bc179dddc976fa646ec6f))
- Notes/local-timeline をサポート ([8706750](https://github.com/yupix/MiPAC/commit/87067504ab599256b05eedd0def6d470835103a6))
- Pollのvoteをoverrideするように ([f21868f](https://github.com/yupix/MiPAC/commit/f21868f2ecd77a128fd480bd5d032c4c5fd31abe))
- Reactionのactionsとmanagerをclientで分けた ([36026a7](https://github.com/yupix/MiPAC/commit/36026a7079ee81b87c877d8d1426fa9a873cb883))
- Notes/search-by-tag をサポート ([27d3a7f](https://github.com/yupix/MiPAC/commit/27d3a7fd8097a24aa0ed733e2e16583a410969c5))
- サポート状況を更新 ([b0d7c20](https://github.com/yupix/MiPAC/commit/b0d7c20a0b3fa30ebf2405e3d594a812e5f5ac8b))
- Antennaを最新に追従 ([7b97e13](https://github.com/yupix/MiPAC/commit/7b97e139dc4ca0817d83d9dc718acf0d52013a9a))
- Antennas/createの引数を更新 ([1a57815](https://github.com/yupix/MiPAC/commit/1a578153a2271b5e8cc45a673acd79aea571d55e))
- アバターデコレーションに関するモデルを更新 ([4348598](https://github.com/yupix/MiPAC/commit/434859831c3edf4e2805b6d88d278062eb20c094))
- UserDetailedNotMeOnlyモデルを更新 ([b69b47d](https://github.com/yupix/MiPAC/commit/b69b47db66dbe61768853cc5a9aa6efe7d7db866))
- Get_invite_list を all版とで分けた ([7f9c0ac](https://github.com/yupix/MiPAC/commit/7f9c0ac12dd119f1ecdf82cbc6d69292225d8836))
- Get_moderation_logs に使える引数を追加 ([16d0287](https://github.com/yupix/MiPAC/commit/16d0287f203eadc708ba3d17ca274312bbf4cc26))
- Admin/roles/create の引数を最新に追従 ([49958d9](https://github.com/yupix/MiPAC/commit/49958d9412ab38e35838a592ac180c569f3c9b5a))
- Emojiに関するモデルを追加 ([e29b495](https://github.com/yupix/MiPAC/commit/e29b49538c4f0453745d9383a8553d0cb8e73295))
- 新しい絵文字モデルを使うように ([6a3ddff](https://github.com/yupix/MiPAC/commit/6a3ddff754af3cdc9aa4771bb0ba9bc551966357))
- Get_all_files メソッドを追加 ([0094483](https://github.com/yupix/MiPAC/commit/00944831c937061181cffe0c9259ccbf804937bb))
- Drive系に _get メソッドを追加 ([7599d20](https://github.com/yupix/MiPAC/commit/7599d20230743e244e78a35067e7f5bd7879c08b))
- Get_all_attached_notes メソッドを追加 ([6e7fd40](https://github.com/yupix/MiPAC/commit/6e7fd405b930e959a75ab234e31f4d2a79522d5a))
- FileActions.create で扱えるファイルの形式を追加 ([8677735](https://github.com/yupix/MiPAC/commit/8677735a1fad5ece53bbbe07b30dd23277409532))
- ChannelモデルにDocStringを追加 ([8cd4503](https://github.com/yupix/MiPAC/commit/8cd4503c3fb6405528f01603b5b5b537b1754950))
- Get_all_followed メソッドを追加 ([e6748ca](https://github.com/yupix/MiPAC/commit/e6748caa7d1dfcb1134d4751fb1e232940c7c5bd))
- Get_all_owned メソッドを追加 ([9439ef5](https://github.com/yupix/MiPAC/commit/9439ef5a3e6e6ee8da09c6454cef6dcca104b80a))
- Channels/timeline周りのDocStringを更新 & エラーハンドリングを追加 ([3c28646](https://github.com/yupix/MiPAC/commit/3c28646caa6e6bfc9d76da04feb4a92d5b8adc93))
- Mute用のmanagerとactionsを用意 ([45c2479](https://github.com/yupix/MiPAC/commit/45c24798798fc8d595b947eb026a4322d25849ee))
- MuteUserモデルを更新 ([3a9707f](https://github.com/yupix/MiPAC/commit/3a9707f5f2e3042143dc709442af73e4fe7d94a6))
- MuteUserをMutedUserに変更 ([d6f494d](https://github.com/yupix/MiPAC/commit/d6f494d1f5aefa945b13b14a13c18396f74abd93))
- /mute/* を再実装 ([bdd4916](https://github.com/yupix/MiPAC/commit/bdd4916de9dcbb3708cf13bcbd48f13ee719d4a6))
- MuteActionsをClientと分けた ([62ee3eb](https://github.com/yupix/MiPAC/commit/62ee3ebabe61b63393eba91cacf32a89bfe90936))
- User周りを再実装 progress #124 ([2d457e9](https://github.com/yupix/MiPAC/commit/2d457e9db846b625c9eab2f91241a78021024265))
- Blockingをclientとで分けた close #123 ([cfad9fb](https://github.com/yupix/MiPAC/commit/cfad9fb23eda85cbc2dfb4188172c7488dba2b8d))
- Blockingモデルを追加 ([b44336d](https://github.com/yupix/MiPAC/commit/b44336d23531088f59b53ede6f197fe7feb649ed))
- BlockingActions._get_listをget_all_listに分けた ([8dfc32b](https://github.com/yupix/MiPAC/commit/8dfc32b1c5f0eb2050646cbdc26712921f221a7d))
- Noteモデルにemojisプロパティを追加 ([0550155](https://github.com/yupix/MiPAC/commit/0550155f27560bc1092c38ac1064eb63d47cd7da))
- RolePoliciesを更新 ([2f0f51e](https://github.com/yupix/MiPAC/commit/2f0f51ef5235e426f3cb5880c443433dee5679cc))
- NotificationRecieveConfig を更新 ([df9a220](https://github.com/yupix/MiPAC/commit/df9a2209ef846ad7b2a6baef1605098bd16e81da))
- Pre commitを使用するように ([9ba6e8a](https://github.com/yupix/MiPAC/commit/9ba6e8a13770ed7a31d55a0e08c22f0068488393))
- Permissions型を追加 ([9b67359](https://github.com/yupix/MiPAC/commit/9b67359ddaad826b9287da48a4db5124997b2fc7))
- MiAuth用のユーティリティクラスを追加 ([a690e1c](https://github.com/yupix/MiPAC/commit/a690e1c8dd878ec6d04025364c15307520dc2bb0))
- [**breaking**] MeRoleを削除 ([a4c878c](https://github.com/yupix/MiPAC/commit/a4c878c83c4587944553b7818f59d00a79bbfbe8))
- Modelに_getメソッドを追加 ([0b5b646](https://github.com/yupix/MiPAC/commit/0b5b6463f5f96f97e3091e1e60a0c001d87b66ae))
- [**breaking**] AntennaActions.get_notesをget_allと分けた ([3a286c3](https://github.com/yupix/MiPAC/commit/3a286c31c24357187d3e310a932b996981a41eff))
- [**breaking**] MutedUserをMutingに改名 ([a7963e8](https://github.com/yupix/MiPAC/commit/a7963e8039a943120e193e13716afd9e8f868436))
- Release v0.6.0 ([749a519](https://github.com/yupix/MiPAC/commit/749a519fe7f806ac5149b1f43b7021f6254d87cf))

### <!-- 1 -->🐛 Bug Fixes

- UpdateでNoneが消されてしまう ([9054f31](https://github.com/yupix/MiPAC/commit/9054f314d35c22c1a4c74ea85b52ec1c302f5f53))
- Typo ([b98b767](https://github.com/yupix/MiPAC/commit/b98b7673d3b91d48d2e8216fa6b11d36a2d13fe4))
- Typo ([3abf722](https://github.com/yupix/MiPAC/commit/3abf7228777555ec378599619bc407e4ffd90ff7))
- Typo ([ecc8b9b](https://github.com/yupix/MiPAC/commit/ecc8b9b9c582442c1cf5480afefd512c63db6466))
- 型が間違っている ([966601e](https://github.com/yupix/MiPAC/commit/966601ed6a46065cbb99a4892c8256f17761bcd1))
- Followeeとfollowerは無い場合がある ([c277bc3](https://github.com/yupix/MiPAC/commit/c277bc37cdbd0ad149337a0bb1daf85adad582ac))
- Paginationでlimitが100以外だと全て取得できない ([1903cca](https://github.com/yupix/MiPAC/commit/1903cca5622e93c111169ec548e144a9dfde5686))
- Auth引数をつけ忘れている ([e760827](https://github.com/yupix/MiPAC/commit/e76082705d8e983b57d258a626e77fce435d778b))
- Mipactlでフォルダを作成するように ([55a2b3e](https://github.com/yupix/MiPAC/commit/55a2b3e9d7b08f6c03405caabdb90f9f5c04cc8a))
- 引数にデフォルト値が入ってる ([5340906](https://github.com/yupix/MiPAC/commit/5340906a656e0644167780407906095a53d38f0c))
- Endpoints.jsonでneedToWorkにならない ([e05af37](https://github.com/yupix/MiPAC/commit/e05af37b4cd901d4d805f07540749ec4af0c821b))
- Get_all_listのwhileの条件が間違っている ([a6de7b9](https://github.com/yupix/MiPAC/commit/a6de7b95d2c69dabb65ac818ae3ee46737354691))
- Typo ([dc3ff77](https://github.com/yupix/MiPAC/commit/dc3ff7743fc405a292bc4370281740247d252ff1))
- サポートしてないものがneedToWorkになる ([06feabb](https://github.com/yupix/MiPAC/commit/06feabb6782acb8641bda82108754e9feb568a7a))
- サポート済みじゃないとハッシュが更新されない ([29f565e](https://github.com/yupix/MiPAC/commit/29f565e9aa4f7ec465f29e41dd13c57796619874))
- Repositoryのリンクを修正 ([6c309e8](https://github.com/yupix/MiPAC/commit/6c309e8717eb4a008f37af1b114a932894733346))
- ネストしたフォルダ構造でインポートが壊れる ([a72b219](https://github.com/yupix/MiPAC/commit/a72b219971b60ccc1e47c964df97d7a6d9864d5a))
- Key がキャメルケースのまま ([63f6761](https://github.com/yupix/MiPAC/commit/63f676102c28e341788a34ebd99c7544e70f63a7))
- Propertyになってない ([99f0d55](https://github.com/yupix/MiPAC/commit/99f0d553255aa3d395170101debbc870e0f3460f))
- Setup install ([863253c](https://github.com/yupix/MiPAC/commit/863253c55c93fbdd0b282f5fff25bccce449c3de))
- 戻り値が間違っている ([a3b0568](https://github.com/yupix/MiPAC/commit/a3b05681b85ad9e365f4691fce81c9ae54250173))
- Build error & typo ([bef5c6f](https://github.com/yupix/MiPAC/commit/bef5c6f8ff41afee8510c146d2c064ff26e73015))
- Circular import ([0f066b7](https://github.com/yupix/MiPAC/commit/0f066b75dbb4433356d723988d853bd0b5d1917d))

### <!-- 2 -->🚜 Refactor

- ユーザーの型を再定義 ([b38926b](https://github.com/yupix/MiPAC/commit/b38926b79b1b37ef88eba4c17192b77a00ce965a))
- ユーザーモデルを作り直した #108 ([dc3978b](https://github.com/yupix/MiPAC/commit/dc3978bc98f9cc01713cb57b1aa54f8b6bbcef5b))
- Get_notesを通常のメソッドに ([bdcf431](https://github.com/yupix/MiPAC/commit/bdcf4312dc3e15bcb9bd806e988fe2f3b2531c82))
- Paginationクラスで使用していない引数やコードの整理 ([5bb0920](https://github.com/yupix/MiPAC/commit/5bb09209512ecee9fc767eefc51974f017c19ea0))
- ClientPartialUserListActionsを追加 ([de8b8a2](https://github.com/yupix/MiPAC/commit/de8b8a24b7a87deae191be37b1b4d030db607d38))
- Admin/ad/delete をより良い形で再実装 ([8638cee](https://github.com/yupix/MiPAC/commit/8638cee7b825aef1ce78a879d6ec0fd8d44ef569))
- ClientNoteActionsで定義した引数をoverrideで再定義するように ([7a2e647](https://github.com/yupix/MiPAC/commit/7a2e647e792681abf9ed6309ae7dd4d954177659))
- Note favorite 周りの実装を新しく ([5c11b80](https://github.com/yupix/MiPAC/commit/5c11b80e6247958e260eedc4b0ee5189b251bcb1))
- 引数の型をより正確に ([9c00909](https://github.com/yupix/MiPAC/commit/9c00909af348249e6e584c49ce430d15c6d5b846))
- ParameterError から ValueErrorに close #119 ([b4327ad](https://github.com/yupix/MiPAC/commit/b4327ad5014fe94bb614b7db94155d9c005567b3))
- Note周りを再実装 progress #124 ([9d562ee](https://github.com/yupix/MiPAC/commit/9d562eed2a862949705b1270c096360a8ed68ed5))
- Userlist周りを再実装 progress #124 ([36faacc](https://github.com/yupix/MiPAC/commit/36faacc1bc876bc688d59281d8be88a2040b39b1))

### <!-- 3 -->📚 Documentation

- Update CHANGELOG.md ([6dcbe15](https://github.com/yupix/MiPAC/commit/6dcbe15faea249f02038810b9352524636e03817))
- Update rst ([da296e4](https://github.com/yupix/MiPAC/commit/da296e436974608ea2104fd69677c124a8c59471))
- Update CONTRIBUTING.md ([103129d](https://github.com/yupix/MiPAC/commit/103129df32c4351fb0c1bd46bea5ab688f7ed921))
- サポート状況を更新 ([d089de3](https://github.com/yupix/MiPAC/commit/d089de37cff12aaa55274e59034251efb561ccd9))
- Update README.md ([3b4fa9c](https://github.com/yupix/MiPAC/commit/3b4fa9c87ed441f4b362bd9d52862fb2f6ddbaf1))
- ドキュメントのデフォルト言語を日本語に ([e2c0ad0](https://github.com/yupix/MiPAC/commit/e2c0ad04e2451cd7252c36942cd5cebb2c014843))
- Update CHANGELOG.md ([7e2ca3f](https://github.com/yupix/MiPAC/commit/7e2ca3f27ed3e13045064f80b4f91980c7c830ed))
- Update README.md ([3cf5b7e](https://github.com/yupix/MiPAC/commit/3cf5b7e909d0d7c2edd299ca92bef0e37016e253))
- Update CONTRIBUTING.md ([3f0c718](https://github.com/yupix/MiPAC/commit/3f0c71841f1ca7465edc0ee120f6e2c56b4a77ac))
- Update CONTRIBUTING.md ([a130033](https://github.com/yupix/MiPAC/commit/a1300330bc9a14214baeaed1453165de97cf7941))
- Update rst & po ([b5a734a](https://github.com/yupix/MiPAC/commit/b5a734ad1609ce91ea0d165853341e75a45a89c4))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Endpoints.pyを更新 ([f12cda8](https://github.com/yupix/MiPAC/commit/f12cda8670a1415b1ee2fe6f3a55eefe51afb9f9))
- AdminActionsのimportを整理 ([10ae56d](https://github.com/yupix/MiPAC/commit/10ae56de96ea6ca085e46654ebcd94192702421a))
- Noteモデルの引数を変更 ([feae71a](https://github.com/yupix/MiPAC/commit/feae71a738137a8235c924dad0778973187a0d9b))
- NoteActions.sendのcontetをsendに ([35ce2c6](https://github.com/yupix/MiPAC/commit/35ce2c6b7585ff56f96a80457e7030cd6016478c))
- ClientChannel系を追加 ([bc643fd](https://github.com/yupix/MiPAC/commit/bc643fdee044a6c80b52c685f1249235c622e07f))
- 些細な変更 ([35f1eae](https://github.com/yupix/MiPAC/commit/35f1eae15e6222a59ea24495fc96f8153c90f9ee))
- サポート状況を更新 ([0734e2e](https://github.com/yupix/MiPAC/commit/0734e2e72932837b1a26d6e58e1a714cc4d942cf))
- Instanceの型を修正 ([b59eab9](https://github.com/yupix/MiPAC/commit/b59eab9807b8e9312ec43c138ec0d0988f0b7588))
- Nicknameを非推奨に ([957b181](https://github.com/yupix/MiPAC/commit/957b1818bdfea096a375f1f4ea758d6efd7e14fa))
- DocStringを追加 ([59535c6](https://github.com/yupix/MiPAC/commit/59535c6ecdea7115d7f2228c6aa28715db68761c))
- Is_partial_userの正確さを向上 ([6472dd1](https://github.com/yupix/MiPAC/commit/6472dd1cf83f81bcf66950797936c9ba0c44c3f8))
- 新しいUser周りのモデルを使用するように変更 ([ee82e4f](https://github.com/yupix/MiPAC/commit/ee82e4f6f285078a0cf88da021d40b6898dfcc05))
- Importの整理 ([b2b0a02](https://github.com/yupix/MiPAC/commit/b2b0a02b60a7855406c8b63768734b61b186de3c))
- Clipの引数を変更 ([7307b8a](https://github.com/yupix/MiPAC/commit/7307b8a4893cbda3079b144fb07c1da354fa3783))
- サポート状況を更新 ([3bbd994](https://github.com/yupix/MiPAC/commit/3bbd994f44b59a9f1f4a759dd43a758c67b21909))
- メソッド名をapiに合わせた ([2e6edaa](https://github.com/yupix/MiPAC/commit/2e6edaa7ebe632f6a72bad398a913c6775e42e2e))
- Format ([4c92ad6](https://github.com/yupix/MiPAC/commit/4c92ad65b8a44b7c16ef6ea3e992cf352cb36712))
- データの更新 ([96e4002](https://github.com/yupix/MiPAC/commit/96e400217ed6190e56436f49c0849d0e3a00adb9))
- サポート状況を更新 ([e09a405](https://github.com/yupix/MiPAC/commit/e09a40516904c69d0e09253647326dc2172cfc55))
- 必要なpythonのバージョンを3.12に ([c707bcc](https://github.com/yupix/MiPAC/commit/c707bcc6396c9ed2f26de42f44b439bb394032f1))
- Python3.12に変更 ([45864df](https://github.com/yupix/MiPAC/commit/45864dfd2f241d37c827a67a95f604139982102a))
- ドキュメントのビルドに3.12を使うように ([7a9239f](https://github.com/yupix/MiPAC/commit/7a9239fec5ae95001ecf7dd4745a8810335a0c35))
- Python3.12に向けて色々変更 ([939b749](https://github.com/yupix/MiPAC/commit/939b74942dc189f019c02cf5cfeadf29eb8adc42))
- Ad周りの型を最新のMisskeyに追従 ([772b43b](https://github.com/yupix/MiPAC/commit/772b43b208a1072ddb5f9942a10c75c1d0eb3dea))
- Format code ([8871d4f](https://github.com/yupix/MiPAC/commit/8871d4f536507e609bef5b1ce7704b82a7845b1d))
- サポート状況を更新 ([bef1efe](https://github.com/yupix/MiPAC/commit/bef1efedd2bd43099b0b80db0935dad40b328ab3))
- サポート状況を更新 ([16fc12e](https://github.com/yupix/MiPAC/commit/16fc12e38630f85ea8f273cad2bce27375270da9))
- メソッドの位置を変更 ([d55f88c](https://github.com/yupix/MiPAC/commit/d55f88c0a34224d0d44626700e5988fccd434722))
- Format code ([0633853](https://github.com/yupix/MiPAC/commit/06338532d7d649472de297466b977c6f35830c4d))
- サポート状況を更新 ([3bad42b](https://github.com/yupix/MiPAC/commit/3bad42b51c33a75eff7868b69d945c42c53c0e5b))
- 使用されていない型を削除 ([0d11373](https://github.com/yupix/MiPAC/commit/0d11373a0225198f8125b3ca9c4e8312f23a7b68))
- Openapiの型を追加 ([3736ae4](https://github.com/yupix/MiPAC/commit/3736ae4f75307c4057f305a8d2026985bcf3559f))
- NoteChannelモデルを更新 ([8f7ed4f](https://github.com/yupix/MiPAC/commit/8f7ed4f33c94e6b8aa40e9c0e52e95e11b03dcca))
- データをもとに戻す ([29ca576](https://github.com/yupix/MiPAC/commit/29ca576206f43ef3e7feebfc2fac2a8b907805bb))
- データを改めて更新 ([bd825f2](https://github.com/yupix/MiPAC/commit/bd825f2ffe0c1adbfb99fb9e6cee4ef97cec0a32))
- プログレスバーを出すように ([7e2eb93](https://github.com/yupix/MiPAC/commit/7e2eb932c9b47dc99bb56a9555b854b92b2a8a25))
- サポート済みスキーマを更新 ([0e768bf](https://github.com/yupix/MiPAC/commit/0e768bf7700c9d46352dbbe5f47dfc45960122b6))
- Channels/create の引数を最新に追従 ([cba1f30](https://github.com/yupix/MiPAC/commit/cba1f30b3a9c0b32014e38cdeed953d29d7ba18f))
- サポート状況を更新 ([dbd78c6](https://github.com/yupix/MiPAC/commit/dbd78c6d9b24a2cce161783bb75a14c9fb272adb))
- Ruffの設定を変更 ([d64fecc](https://github.com/yupix/MiPAC/commit/d64fecc39aa9b874310188ac3870763a5e41504f))
- Format ([1297def](https://github.com/yupix/MiPAC/commit/1297defc273dcab9402502e19e3e3cdcd38187f0))
- Followの型を正確に ([8e1cc0c](https://github.com/yupix/MiPAC/commit/8e1cc0ca33ecdc070a67d56598547587e30631f0))
- Add .onedev-buildspec.yml ([cb8ffa6](https://github.com/yupix/MiPAC/commit/cb8ffa62b5378dd0e8165ffed0146d9fd4072b22))
- 開発者向けの依存関係を追加 ([b3a1a1a](https://github.com/yupix/MiPAC/commit/b3a1a1ad22b72c2fc37e54b3bde08efd9528a76c))
- サポート状況を更新 ([a29deeb](https://github.com/yupix/MiPAC/commit/a29deebf2e3e95bb0ca570a94593c2d1c9b03d9b))
- Gitlabへのpushはforceで行うように ([1d8817e](https://github.com/yupix/MiPAC/commit/1d8817e9970066e9659c9812f43ece8a7462f503))
- Driveの型を変更 ([72052a2](https://github.com/yupix/MiPAC/commit/72052a2d7f719eb98bc0559969ad04121c53ca81))
- Update docstring ([4c69fc5](https://github.com/yupix/MiPAC/commit/4c69fc522027098045a080bd83709accf2ab7ead))
- Update support status ([443a93b](https://github.com/yupix/MiPAC/commit/443a93b122c27b91e4e902a8a4d79f022a9a90c2))
- 引数のデフォルト値を変更、docstringを更新 ([b1210e6](https://github.com/yupix/MiPAC/commit/b1210e63277f619b12f731d2549fbb4b51397b3e))
- Docstringを変更 ([e3a420a](https://github.com/yupix/MiPAC/commit/e3a420a8f21e687d6ece361be54d09f7abb2e6a6))
- サポート状況を更新 ([93028ab](https://github.com/yupix/MiPAC/commit/93028ab1a0c564a323c7a917c7d5c3df2d138f5d))
- Format ([49ad01d](https://github.com/yupix/MiPAC/commit/49ad01d497cd9b1f5328c53414e87447a23e063d))
- Format ([787813e](https://github.com/yupix/MiPAC/commit/787813ecbc3787f28a5f50772ac2d570a023448e))
- Update DocString ([04d4eef](https://github.com/yupix/MiPAC/commit/04d4eef0c1e97e91bb9ef122fcb5c12767e9988f))
- Update DocString ([afe4c8f](https://github.com/yupix/MiPAC/commit/afe4c8f84fe56c9d08406cc5ee28725ef94795e8))
- サポート状況を更新 ([c9c8e54](https://github.com/yupix/MiPAC/commit/c9c8e546a1caea5908cb0b7766d8f1543a0d5f04))
- Format ([3e535fe](https://github.com/yupix/MiPAC/commit/3e535fe0356994a9764d157784d73a508b1c8204))
- Endpointを更新 ([1dfd443](https://github.com/yupix/MiPAC/commit/1dfd443652922eaf2a6d41b5a3865cd18163aa73))
- 些細な変更 ([da1ebfe](https://github.com/yupix/MiPAC/commit/da1ebfe93eb823c715ad10e7c82a0ac551eeedaf))
- サポート状況を更新 ([8cd61c3](https://github.com/yupix/MiPAC/commit/8cd61c3ff777901d2fead7f7f4bfc0eff4be2b02))
- Add code_quality.yml ([b8792c5](https://github.com/yupix/MiPAC/commit/b8792c565ec900e9dcf53cdc6664465a07d19730))
- 些細な修正 ([42d1283](https://github.com/yupix/MiPAC/commit/42d128389edc43a9e84151155f810f1ab670b52e))
- 存在しないエンドポイント用のaction等を削除 ([33fca69](https://github.com/yupix/MiPAC/commit/33fca69953c9725c3463a9b1252ae5090e5ac9ea))
- Format ([973ad39](https://github.com/yupix/MiPAC/commit/973ad398c708b4ff893712468aca1788752c66b7))
- Format ([e8ce50d](https://github.com/yupix/MiPAC/commit/e8ce50d50cf620893be54838e60a5da59be813f3))
- 些細な修正 ([dc2cf6a](https://github.com/yupix/MiPAC/commit/dc2cf6acd26e8f3860adc6add3729f69d582d90f))
- Clip_idがキーワード引数になっていないのを修正 ([8860a1d](https://github.com/yupix/MiPAC/commit/8860a1d1b2904d7054f42398a3b3b7dc76d0b3c4))
- 些細な変更 ([f2ace31](https://github.com/yupix/MiPAC/commit/f2ace31c5c07f31ddb026831cac22c7a5e524ff2))
- Pyrightの設定を追記 ([e7bf18e](https://github.com/yupix/MiPAC/commit/e7bf18ead19cb3f750c6188e9ab0828d247ebb98))
- [**breaking**] BlockingUserモデルを削除 ([59f7867](https://github.com/yupix/MiPAC/commit/59f78676ed05e1ab709b92ee3659fc1df9a8e48c))
- コミット漏れ ([62d4037](https://github.com/yupix/MiPAC/commit/62d40376f86b2d1b4cd058c452a296614d929c6d))
- Annoucementの型を明確に ([2931e3d](https://github.com/yupix/MiPAC/commit/2931e3d8695ff8fb2fbac189a29e6c0b4b76f8fa))
- IUserのunionからMeDetailedを削除 ([7008dc7](https://github.com/yupix/MiPAC/commit/7008dc754741089515aa1cfafb6ae7c54fe9b81d))
- EmojiSimpleにlocal_onlyプロパティを追加 ([bca4dd6](https://github.com/yupix/MiPAC/commit/bca4dd6719bd68dcc8b207a0ecace29e04eabed4))
- IMutedUserの型を修正 ([c5109ba](https://github.com/yupix/MiPAC/commit/c5109ba72786387cf537304d3609355d77c70e7e))
- Pollの型を修正 ([a612cf8](https://github.com/yupix/MiPAC/commit/a612cf8472595172d99b23e8d9f9545194dcf99b))
- ModerationLogの型を更新 ([c62e81e](https://github.com/yupix/MiPAC/commit/c62e81e12427c2fe8186acc7e3bc41e1a62214d5))
- Format ([303c415](https://github.com/yupix/MiPAC/commit/303c41501bef937a660a232d7ee4aed0c437ab09))
- 使用していないimportを削除 ([00f13ce](https://github.com/yupix/MiPAC/commit/00f13ce294ca4bc54beb5a359e19b8029f5341e5))
- [**breaking**] AuthClientを削除 ([08a3629](https://github.com/yupix/MiPAC/commit/08a36290142f1f5aa68ad6bb520f220f8f830e07))
- 些細な変更 ([bfce899](https://github.com/yupix/MiPAC/commit/bfce899e36e68bc8159f66962281504ee0557e11))
- Credentials_required を削除 close #101 ([357bd2c](https://github.com/yupix/MiPAC/commit/357bd2c932e95541b06783b2d475a07d9b5b0afa))
- [**breaking**] Requestのauth引数のデフォルト値をTrueに変更 ([6e3dac1](https://github.com/yupix/MiPAC/commit/6e3dac1507e0fd35ace0eb069cd70b2cf1f84613))
- 未消化のTODOを消化 ([5b6f52b](https://github.com/yupix/MiPAC/commit/5b6f52b56b1d1278d132c175a6d067c2aaac4b97))

## [0.5.99] - 2023-12-03

### <!-- 0 -->🚀 Features

- チャットに関係するファイルを削除 ([e1bc5f9](https://github.com/yupix/MiPAC/commit/e1bc5f93ecfd8b546354872ba5a56e0044c6184e))
- 広告を最新のMisskeyに合わせて修正 ([425f843](https://github.com/yupix/MiPAC/commit/425f84370de73cbdbcad11bf66efaf20c56020e1))
- Metaを最新のMisskeyに合わせて修正 ([b53ebab](https://github.com/yupix/MiPAC/commit/b53ebab8df2602835a3587ad87139487b2aea6d8))
- Configからuse_version等のバージョンやforkに関する物を削除 ([6b0972a](https://github.com/yupix/MiPAC/commit/6b0972a4d6472bde49519e09a0932e3a42a5e066))
- ユーザーモデルを作り直した #96 ([5d81c3d](https://github.com/yupix/MiPAC/commit/5d81c3d0847d746014e3a5c583e9966504fec6f1))
- Get_meのモデルをより詳細に ([f8c2eef](https://github.com/yupix/MiPAC/commit/f8c2eef6977a86a88408104e6f90cd0b271113a1))
- Users/showで使える引数にuser_idsを追加 ([0b01308](https://github.com/yupix/MiPAC/commit/0b01308239b2319683efd256bb4b30642ecef91c))
- Users/notesで使える引数をv13に合わせて修正 ([3c4f917](https://github.com/yupix/MiPAC/commit/3c4f917640c6dab219e5ed7f88818fbdc0da40bc))
- Is_partial_userを追加 ([7b3ef24](https://github.com/yupix/MiPAC/commit/7b3ef243b111d7d685f33bd01b484c6e1cc3fa58))
- Create_user_modelでpartialも作れるように ([6ace5a9](https://github.com/yupix/MiPAC/commit/6ace5a94b31965b771b7702bd1654de48ba436ce))
- Class用のDeprecatedデコレータを作成 ([92ad730](https://github.com/yupix/MiPAC/commit/92ad730d150ded04e50d1da561f4972262e8a708))
- PartialRoleモデルを追加 ([60dd8eb](https://github.com/yupix/MiPAC/commit/60dd8eb606270a8ae473cb8298c43aa1f9d44b2e))
- HttpClientでwith構文をサポート ([e94f404](https://github.com/yupix/MiPAC/commit/e94f404f77248f63defb2a56454d0c42e7121a27))
- 例外 CredentialsErrorを追加 ([8a934ce](https://github.com/yupix/MiPAC/commit/8a934cee044dca69fabf8b6e8b2ac8d196cc4a9c))
- ReactionAcceptanceをサポート ([8141e03](https://github.com/yupix/MiPAC/commit/8141e039c60426caf8a7e532930d4a9390da8643))
- Get_all_children ジェネレータを追加 ([179da5e](https://github.com/yupix/MiPAC/commit/179da5e0f4f2c64e7cc94ecfdd74e9b6f08085a2))
- Fetch_childrenメソッドを追加 ([2a5442d](https://github.com/yupix/MiPAC/commit/2a5442d4220295a294ca44f4edaebedbb84d8fb3))
- NoteStateから プロパティ is_watching を削除 ([abc2ec1](https://github.com/yupix/MiPAC/commit/abc2ec1f9618850c57a3cd0c3474b72c42e28fad))
- Get_stateメソッドでcacheをサポート & fetch版を用意 ([b40199e](https://github.com/yupix/MiPAC/commit/b40199ea18222cc00405d6b104c4d31f660c7ec4))
- ReactionAcceptanceをサポート ([085743d](https://github.com/yupix/MiPAC/commit/085743dd6e4037919e0567e788dab655af284938))
- Get_all_children ジェネレータを追加 ([bd75c18](https://github.com/yupix/MiPAC/commit/bd75c18659974680845c46c63a38d0bc06af2b72))
- Fetch_childrenメソッドを追加 ([2e6629d](https://github.com/yupix/MiPAC/commit/2e6629da8e5b3317d5d2e879e65eddf4c4366fae))
- NoteStateから プロパティ is_watching を削除 ([43eaa45](https://github.com/yupix/MiPAC/commit/43eaa45add495b0c50d32ecce354cb5f97f8a9a3))
- Get_stateメソッドでcacheをサポート & fetch版を用意 ([2024fbd](https://github.com/yupix/MiPAC/commit/2024fbdba41b82ff3f73743707195d30271a86cc))
- [**breaking**] Get_reactionをget_reactionsに変更 ([835efe3](https://github.com/yupix/MiPAC/commit/835efe3b96e2af2a543877c1d7b741ff5d463910))
- Fetch_reactionsを追加 ([8bdf3be](https://github.com/yupix/MiPAC/commit/8bdf3be24b022ab18a50886979509d176248e737))
- Noteモデルを作り直した ([d179360](https://github.com/yupix/MiPAC/commit/d1793603ec0beb5f8473626c70fe3c0d546ab415))
- PollActionsをClientPollActionsに分割 ([9ba7729](https://github.com/yupix/MiPAC/commit/9ba77293d26c41ceda12a0ddfd08207636d5f4ef))
- Get_all_recommendationメソッドを追加 ([6d947f1](https://github.com/yupix/MiPAC/commit/6d947f15dbc2d49cb199aab7db825652f12f8b40))
- ClientPollManagerを追加 ([4779c1b](https://github.com/yupix/MiPAC/commit/4779c1bcb9a9f5d01e9da62961ce91ae05d69079))
- ClientManagerにClientNoteManagerの生成を追加 ([e848de0](https://github.com/yupix/MiPAC/commit/e848de0152e212c94fc1a4f15a4fd4d7a0077282))
- Get_renotesメソッドを実装 ([3ac407f](https://github.com/yupix/MiPAC/commit/3ac407f1df1dffb2f0af890f0292a3b4cb91ca72))
- Get_repliesをジェネレータからメソッドに ([b6e2c44](https://github.com/yupix/MiPAC/commit/b6e2c44dd00e55f11d109ef976dbaaee164603ff))
- Get_all_repliesジェネレータを追加 ([3fad319](https://github.com/yupix/MiPAC/commit/3fad319a0221aa1f949989449a956775f1a04037))
- Renoteメソッドを追加 ([11f6419](https://github.com/yupix/MiPAC/commit/11f64191584c7b33c328ac1a41c504fecdc2aa77))
- Get_mentionsメソッドを追加 ([f960742](https://github.com/yupix/MiPAC/commit/f960742d9edddc1de0ef4fd0cefa380df21e472d))
- Openapiの型を少し追加 ([9bd0ea3](https://github.com/yupix/MiPAC/commit/9bd0ea373edecb26045d77d7082d46d1ac80e4f6))
- Api.jsonの変更を検知するスクリプトを追加 ([d40585f](https://github.com/yupix/MiPAC/commit/d40585f4ca019aca9f72c5b41cbf18560a5ec08a))
- Username/* をサポート ([543030b](https://github.com/yupix/MiPAC/commit/543030b8b6025e4d78ecc6c88e2153dfc1e70c84))
- Adminではないinviteエンドポイント用のmanagerとactionを追加 ([b6a39ff](https://github.com/yupix/MiPAC/commit/b6a39ffe8890cbb1e3e04328c2a2df0ddb6c12f5))
- InviteCodeモデルにapiプロパティを追加 ([59f6d46](https://github.com/yupix/MiPAC/commit/59f6d4603a734c50365faf0c0c7a20fed5a1dce9))
- InviteLimitモデルを追加 ([e6b7405](https://github.com/yupix/MiPAC/commit/e6b7405d00aeec09ad303ee147b10475c6abcba6))
- Invite/listをサポート ([42526ee](https://github.com/yupix/MiPAC/commit/42526ee7989b1ddab5eb3dc44b1005ff422f60c9))
- Invite/limitをサポート ([54f97bb](https://github.com/yupix/MiPAC/commit/54f97bba62c69359492eab51890ea62fec60e9eb))
- DriveStatusモデルを追加 ([892a164](https://github.com/yupix/MiPAC/commit/892a1648cf75fc42e10ce4595340858f5bc86f98))
- Drive周りのモデルと型を最新の物に追従 ([1b9dc39](https://github.com/yupix/MiPAC/commit/1b9dc39edf474a70a780a50f19854d2b30a9dcd9))
- Missingクラスを追加 ([10c8c8d](https://github.com/yupix/MiPAC/commit/10c8c8d6982b89ddb7e284339ea396cf64ed14ec))
- Remove_dict_missing関数を追加 ([5e36908](https://github.com/yupix/MiPAC/commit/5e36908b17884c2044e0dcbee1f4a01b151f956c))
- Drive/files/* をサポート ([b91aaa1](https://github.com/yupix/MiPAC/commit/b91aaa19233ec685530c8f89999f6704ee6e576a))
- Drive/streamをサポート ([0a247c5](https://github.com/yupix/MiPAC/commit/0a247c5b2bd1424663dea2cf74b2d1d00ac50648))
- Drive/folders/* をサポート ([86cc8ed](https://github.com/yupix/MiPAC/commit/86cc8edb72d17cb90742cef3c2ab47b434d5a00b))
- Admin/drive/* をサポート ([d098b91](https://github.com/yupix/MiPAC/commit/d098b91eca4f0af3cb03cb4e623915760789df22))

### <!-- 1 -->🐛 Bug Fixes

- Emojiの追加に必須のdataが足りていない ([5e2e9ea](https://github.com/yupix/MiPAC/commit/5e2e9eaebb2567e1fb297c0fd6ab126aeb2476a3))
- Typo ([05c829a](https://github.com/yupix/MiPAC/commit/05c829a388b5c3b29e76c744e167428dda8d782a))
- ログインしているのにUserDetailedNotLoginedが返ってくる ([75e734e](https://github.com/yupix/MiPAC/commit/75e734ebfbe276620215d69035ce342040d8bce7))
- Mipac.utilを使っている箇所があった ([af0cf9b](https://github.com/yupix/MiPAC/commit/af0cf9b7c551bdf75af44f13ec37da7b639cd510))
- Roleにis_explorableプロパティが欠如している ([2cc5e20](https://github.com/yupix/MiPAC/commit/2cc5e20f355903d5790d1966f5392e8e8e1e030b))
- Credentials_requiredでインスタンスを渡し忘れてた ([6a8e508](https://github.com/yupix/MiPAC/commit/6a8e5083c35e3492f5261805d22db0110fc00745))
- Doc_genがwindowsだと\なせいで動かない ([843b19d](https://github.com/yupix/MiPAC/commit/843b19d28eb742f383eaaabdfae5fa083916a082))
- NoteManagerでNoteActionsを毎回生成しないように ([cc6b88b](https://github.com/yupix/MiPAC/commit/cc6b88b00709983883abfcc5f1bb48af5cb15233))
- Fetch_childrenメソッドでnote_idをインスタンスから参照していない ([5bc22d2](https://github.com/yupix/MiPAC/commit/5bc22d2872aeb8a2be0b724b46e8872a8d41d115))
- Get_reactionのreaction引数は必須ではない ([4442889](https://github.com/yupix/MiPAC/commit/4442889ec6a7c5f73e2f7353019562b2f2f5bf2e))
- NoteManagerでNoteActionsを毎回生成しないように ([f77afff](https://github.com/yupix/MiPAC/commit/f77afff31f47a7e34f9fbe4ad0d9d7b4d4737d20))
- Fetch_childrenメソッドでnote_idをインスタンスから参照していない ([2a248d6](https://github.com/yupix/MiPAC/commit/2a248d6950b3366989fe04aa42b58572dd338dbd))
- Get_reactionのreaction引数は必須ではない ([5cc2404](https://github.com/yupix/MiPAC/commit/5cc2404ce97f23572e7fed25cdacb8463bdbb15e))
- ReactionManagerでReactionActionsを毎回生成しないように ([42c1a0b](https://github.com/yupix/MiPAC/commit/42c1a0b21cd30bbcb26640364bd400a7bc9bc67a))
- Noteモデルにapiプロパティが無い ([4f610a7](https://github.com/yupix/MiPAC/commit/4f610a7a7b893360444338f12c9f78f96db5acd7))
- Inviteのcreated_byはdatetimeではなくPartialUser ([ce48f90](https://github.com/yupix/MiPAC/commit/ce48f90d02a70a5deb3bd4991912436ec6ab43e6))
- Pagination.is_finalがnext実行前に見ると必ずTrueになってしまう ([2d43ba7](https://github.com/yupix/MiPAC/commit/2d43ba734028cbd94d5ccc84d232caf22051db45))

### <!-- 2 -->🚜 Refactor

- Users/search のコードを修正 ([b6a2caf](https://github.com/yupix/MiPAC/commit/b6a2caf0158407b55a4cf1ee2d93be77106d52f1))
- PartialInviteCodeをInviteCodeに統合 ([5580a42](https://github.com/yupix/MiPAC/commit/5580a42ea34d17751eef8dcc32cd71d5d9bbbe24))
- オーバーライドすることで引数を正確に ([ef09b52](https://github.com/yupix/MiPAC/commit/ef09b52234882fcb91afde8724541937df649f84))

### <!-- 3 -->📚 Documentation

- Update README.md ([16f6ab3](https://github.com/yupix/MiPAC/commit/16f6ab3603a40590890f5a6d57933bcde39b6e46))
- デザインが崩れているのを修正 ([0531de4](https://github.com/yupix/MiPAC/commit/0531de4416da84113cf81393330fd998e43b7591))
- Classの後にattributableを配置するjsを追加 ([50fb89c](https://github.com/yupix/MiPAC/commit/50fb89cd72110d1fcfffb182f91579658256bc8b))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Login実行時にmetaを取得するのを廃止 ([6ec77a4](https://github.com/yupix/MiPAC/commit/6ec77a4113cd559f6bef79ab1e17ad9e56c5d88a))
- インポートの整理 ([a408f52](https://github.com/yupix/MiPAC/commit/a408f5291f52abee79256c910c201866a71d8b5e))
- Cnameがpushされると消えるのでそれの対策 ([9ca53dc](https://github.com/yupix/MiPAC/commit/9ca53dced82cdf5229644db4ec135569d795559b))
- Docstringを少し付けた ([d472837](https://github.com/yupix/MiPAC/commit/d47283779de2b4788281cb293a46a655bd4a8056))
- Import系コミット忘れてた ([a0da4c5](https://github.com/yupix/MiPAC/commit/a0da4c51ae219ef0dd1d81991c29f5a07a208ee6))
- Format ([3a9ad19](https://github.com/yupix/MiPAC/commit/3a9ad197038e2fbb112b4eb84ca1639cac214b8d))
- Endpointを更新 ([321814b](https://github.com/yupix/MiPAC/commit/321814ba10f4adace839db406029c2fb370fe472))
- Update .gitignore ([b75d06e](https://github.com/yupix/MiPAC/commit/b75d06e78450c6c984cfda9aa877e0f5e5534816))
- Format code ([e58690b](https://github.com/yupix/MiPAC/commit/e58690b219b4d7a66c0ebf0b19da11cdc3f821a0))
- /api/admin/invite は廃止されたので削除 ([c3a1c8f](https://github.com/yupix/MiPAC/commit/c3a1c8f899dfbe534edffcb5a754eddc3973d137))
- Docstringを追加 ([5026014](https://github.com/yupix/MiPAC/commit/5026014b09a42e2570e0b459f866d8dbaa137e5b))
- Silence周りのメソッドを削除 ([7364dcf](https://github.com/yupix/MiPAC/commit/7364dcfa716d02cb916adc4d7345044bc3733c46))
- Vacuumメソッドを削除 ([e402026](https://github.com/yupix/MiPAC/commit/e4020262404dda4908ce39f252bf452f2bc9835e))
- Blackをやめてruffに ([96ce06e](https://github.com/yupix/MiPAC/commit/96ce06edfc31690d63067ade4e4b2a5e65dafbc9))
- 非推奨になっていたmipac.utilモジュールを削除 ([f2ab820](https://github.com/yupix/MiPAC/commit/f2ab820e100ec5fac4ba9acec0b3e4ee5af3c9e8))
- UserRoleを非推奨に ([859513d](https://github.com/yupix/MiPAC/commit/859513d2882fc2fdbba54e4a3a9c4b0168df7b3c))
- Create_user_modelでpartialを除外できるように ([bdbaa52](https://github.com/yupix/MiPAC/commit/bdbaa5215ffe290b78ae20ea22931fe6918979b4))
- RoleはPartialRoleを継承するように ([96a126a](https://github.com/yupix/MiPAC/commit/96a126accdf6c585049b049bdb2827fe41f8d532))
- IPartialRoleに含まれる属性をIRoleから削除し、継承するように ([bf69165](https://github.com/yupix/MiPAC/commit/bf69165b3b94bf02d149e0776b57ddefd1559d71))
- UserRoleをPartialRoleに置き換え ([5087d1b](https://github.com/yupix/MiPAC/commit/5087d1b59a41b403699d0e51a3b07026fd576798))
- IUserRoleのDocStringにDeprecatedであることを記述 ([7709667](https://github.com/yupix/MiPAC/commit/7709667c8359e1a42fa6f9036855e2df7c6b0806))
- /api/roles/*系にdocstringを追加 ([1c6316e](https://github.com/yupix/MiPAC/commit/1c6316e098611a617b373f410b18d66a18089dfa))
- Flake8ではなくruffを使うように ([a4b62a7](https://github.com/yupix/MiPAC/commit/a4b62a715a74b65359480345fb50e04b826a1b64))
- V13には必要ないデータを削除、併せてendpoints.pyで使用しないように ([72e42da](https://github.com/yupix/MiPAC/commit/72e42da98dd2da1bf294b3b6d1bb439e4bc73cbf))
- データを2023.11.0-beta.10の物に更新 ([23c45cc](https://github.com/yupix/MiPAC/commit/23c45ccd97bac64dac3230f9aee981c33a3af40b))
- Endpoint周りの情報を更新 ([b56b9fc](https://github.com/yupix/MiPAC/commit/b56b9fcc6d28032bdd5289a5869569f6664f19a0))
- 使用していない定数を削除 ([5ad026d](https://github.com/yupix/MiPAC/commit/5ad026dca623fcc90678edf25887380c9658fb12))
- 使用していないimportを削除 ([0f35220](https://github.com/yupix/MiPAC/commit/0f35220c63add647adb870e4717a37d19ca4d46c))
- Credentials_requiredデコレータを追加 ([47a9769](https://github.com/yupix/MiPAC/commit/47a9769a4bdb116d9b6e05ebb491711aad044a0d))
- 使用してないimportの削除 ([1d6a79c](https://github.com/yupix/MiPAC/commit/1d6a79c1ca9e1fa8a3dd2459adfedb29d5220269))
- 最新のデータに更新 ([6adf277](https://github.com/yupix/MiPAC/commit/6adf2774cf165b1b3f5a9b6ada0816984b8cd71f))
- IReactionAcceptanceに抜けてる値を追加 ([d4a1048](https://github.com/yupix/MiPAC/commit/d4a10488bae7c34f126af07c23f4eba73b53c256))
- Format ([2f3618e](https://github.com/yupix/MiPAC/commit/2f3618edf904612b7b382be6a93f0e15d27eb3b8))
- Get_childrenを普通のメソッドに ([48b2ede](https://github.com/yupix/MiPAC/commit/48b2ede5cdf159c878fd7c18c6b674045abbf3c4))
- Cache decoratorでfunctools.wrapsを使うように ([74fc003](https://github.com/yupix/MiPAC/commit/74fc00355a9feadf96be49e85ab470903a29accb))
- Noteのdocstringを更新 ([9f9e178](https://github.com/yupix/MiPAC/commit/9f9e178e84aa8fc5a5990459f98e33fea23e2d3d))
- IReactionAcceptanceに抜けてる値を追加 ([230b40b](https://github.com/yupix/MiPAC/commit/230b40b5b6876cfe0329b116983545a658b9a148))
- Format ([78ad980](https://github.com/yupix/MiPAC/commit/78ad980a663b0c6d485aa7a013eba5339f7f30e4))
- Get_childrenを普通のメソッドに ([8c51ba2](https://github.com/yupix/MiPAC/commit/8c51ba27373896cea4deb0608e9182e908417653))
- Cache decoratorでfunctools.wrapsを使うように ([a6034f7](https://github.com/yupix/MiPAC/commit/a6034f7d9845076cc2c2e6644935af499fc496b0))
- Noteのdocstringを更新 ([99a3ace](https://github.com/yupix/MiPAC/commit/99a3acee4be6c26f5dae1dd5f11c73bb44f24aca))
- PartialNoteを削除 ([9ef547f](https://github.com/yupix/MiPAC/commit/9ef547febc1b231072c0e404752778b398583358))
- NoteManagerからcreate_client_note_managerを削除 ([2b0c9a1](https://github.com/yupix/MiPAC/commit/2b0c9a10ac7eb8bdfb8b87db53ea8369546964de))
- ClientNoteManagerのpollをClientPollManagerに変更 ([0f59ac4](https://github.com/yupix/MiPAC/commit/0f59ac4f563616fd6dede17a885b1e5b0d6f2d19))
- Importをcommitし忘れてた ([5f18237](https://github.com/yupix/MiPAC/commit/5f182378ae8f81bb6a1da1dd10d8cfedf4bf62ff))
- DocStringを追加 ([fece605](https://github.com/yupix/MiPAC/commit/fece60542b8abb7b8b90e9c02125cf012f59eff2))
- 引数の名前を変更 ([ab39041](https://github.com/yupix/MiPAC/commit/ab390413bfb891c33e12df6c38303b146b2dc729))
- Docstringを追加 ([04ce746](https://github.com/yupix/MiPAC/commit/04ce746027ef41ad17e75120d826047a7358d00a))
- Get_reactionsの引数を微調整 ([36017fd](https://github.com/yupix/MiPAC/commit/36017fdf68edd6656efcdb6b0de9b91a2e493ad8))
- Endpoints.jsonに保存しないように ([49132de](https://github.com/yupix/MiPAC/commit/49132defff081270f89c9097d7089dcddf80e787))
- サポート状況のリストを追加 ([33164b4](https://github.com/yupix/MiPAC/commit/33164b47c0bc3349a26ce410f1b7d8875c3597de))
- AbstractActionのコンストラクタの引数を調整 ([d9b6ce1](https://github.com/yupix/MiPAC/commit/d9b6ce18a79cdf612ff86cf8a64228513ac142c1))
- 一部のlintエラーを修正 ([eb98c3f](https://github.com/yupix/MiPAC/commit/eb98c3f6cec38113c89f8bffb09086b9bb0ad24c))
- Docstringを追加 ([28bf5de](https://github.com/yupix/MiPAC/commit/28bf5de18238bf34f613719d49d5c499ab118ec1))
- 不要になったファイルを削除 ([e1a6cd2](https://github.com/yupix/MiPAC/commit/e1a6cd2d3c362849e1c5b7b9535a84521465f378))
- サポート状況を更新 ([f30f0e5](https://github.com/yupix/MiPAC/commit/f30f0e5936d0dbfbe201f9b48b2183df79bbc153))
- Remove_dict_emptyで特定のkeyをignoreできるように ([c2cac8f](https://github.com/yupix/MiPAC/commit/c2cac8f6d51f0dec76d11462a02a3e50da0cce78))
- Mipac.utils.utilのMISSINGを使うように ([300c2e4](https://github.com/yupix/MiPAC/commit/300c2e435f65df582243f20259fba5083018754e))
- 古いdrive達をいったん避難 ([d55a49c](https://github.com/yupix/MiPAC/commit/d55a49c961143c47a7607dc6c68f19b4ff44dca9))
- サポート状況を更新 ([6e26406](https://github.com/yupix/MiPAC/commit/6e2640602ab46978d026b9955ec3a6be3c9b4e66))
- 型の名前を統一 ([af4bb82](https://github.com/yupix/MiPAC/commit/af4bb8207f97f47b295824d6c76643f2573edc8d))
- Importのcommit忘れ ([7075b13](https://github.com/yupix/MiPAC/commit/7075b13f7847a546d4cf43605b2d9684d1f9e436))
- 使用していないimportを削除 ([641db1d](https://github.com/yupix/MiPAC/commit/641db1d89a6937e85b00f11613cfdcc7f56e2397))
- Driveに関するモデルの引数を変更 ([1cf757f](https://github.com/yupix/MiPAC/commit/1cf757ff1d07c5f7cd659f50a80022277a8aefd8))
- 昔のdrive系を削除 ([c376350](https://github.com/yupix/MiPAC/commit/c3763504cb3437243ff40b006dc17ec73908e3b7))

## [0.5.1] - 2023-10-01

### <!-- 0 -->🚀 Features

- プロトコルが欠如してる場合のエラーを分かりやすく close #76 ([5e6c044](https://github.com/yupix/MiPAC/commit/5e6c04491fe044e6255770148c789d7b2efac392))
- ファイルを保存するための save メソッドを追加 Resolve #78 ([dcf20ab](https://github.com/yupix/MiPAC/commit/dcf20ab45402349f41c33b7943f3e39dce68357e))
- Async with 構文をサポート Resolve #79 ([0c0fd4e](https://github.com/yupix/MiPAC/commit/0c0fd4e3d9f7c4c9436a1b1a8e9a07b87406b72b))
- FilesプロパティーでFileモデルを返すように Resolve #80 ([0966944](https://github.com/yupix/MiPAC/commit/096694476bb671832572c9dee3fc49e3b5bcec0a))
- モデル同士の比較演算をサポート Resolve #81 ([259d41b](https://github.com/yupix/MiPAC/commit/259d41b6a841e16fcfb7a55e34f541b676d3b053))
- Reactionの許可範囲を共通の型に ([15b3b33](https://github.com/yupix/MiPAC/commit/15b3b33efd1324a8d51b6db85fdcdef727c31efb))
- Clipの型を追加 ([3c61a15](https://github.com/yupix/MiPAC/commit/3c61a15ffeb804979e9e19c8f869914d618a8582))
- Clipに関するものを追加 ([65fde31](https://github.com/yupix/MiPAC/commit/65fde31abb19e97e495e8cde92e06971333d93b0))
- /api/users/clipsをサポート ([c4fc1d5](https://github.com/yupix/MiPAC/commit/c4fc1d52f4c3353eb8a2181a4ce33d1a39e7cfdb))
- Channelのサポート チャンネルをサポートする Resolve #64 ([baadb13](https://github.com/yupix/MiPAC/commit/baadb1303dbb2bb61037430829666dc18fb2c2e2))
- Release v0.5.0 ([d8e03f4](https://github.com/yupix/MiPAC/commit/d8e03f43fbf779bf17f536f1de2600343a196420))
- Admin/invite/* をサポート ([8e95e8f](https://github.com/yupix/MiPAC/commit/8e95e8fa74252951be4aba8f84a6225b4319b9e2))
- Axblackを辞めてblackに ([f7b930f](https://github.com/yupix/MiPAC/commit/f7b930fbdde3423fffe95392e91ee1cec345fd23))
- README.mdを英語に、日本語は別途用意 ([f630410](https://github.com/yupix/MiPAC/commit/f630410f338bb48bf4a329c042dc97113a731c1c))
- Pagination_iterator関数を追加 ([edcd4b6](https://github.com/yupix/MiPAC/commit/edcd4b65a5bb9224689b7cfbeb471a4437ef3411))
- AbstractModelをModelに継承させるように ([2fe31ee](https://github.com/yupix/MiPAC/commit/2fe31ee894a6603d930d84914198502f7948e99d))
- Roles/show をサポート ([0ff3a0a](https://github.com/yupix/MiPAC/commit/0ff3a0a7f47bae0eef52fdde9ddc3a6d5d335eec))
- ユーザーのロール関係をサポート ([e982e0a](https://github.com/yupix/MiPAC/commit/e982e0a6005133a3c086d9b9b82ca807748dde5a))
- MeDetailedを追加 ([d2c18c4](https://github.com/yupix/MiPAC/commit/d2c18c4a00460dc95253bfe0aa15b75588986679))
- Configにアカウントのidを保存するように ([fcc852b](https://github.com/yupix/MiPAC/commit/fcc852baa23bd516f88799b1e6c46fc20641ab81))
- Admin/show-usersでMeDetailedも返せるように ([ab124b5](https://github.com/yupix/MiPAC/commit/ab124b53ae5c7c586cceb04643e70faaf3706cae))
- Role/*をサポート #87 ([afb3ea7](https://github.com/yupix/MiPAC/commit/afb3ea79885c08ef7150d15e0e98666d5c00682a))
- V13以上じゃない場合は例外を返すように ([94a5a09](https://github.com/yupix/MiPAC/commit/94a5a0979e84ef64c296ee4221bf11c580a11df8))
- ドキュメント周りを整備 ([1d8848b](https://github.com/yupix/MiPAC/commit/1d8848b4580f580e10f2bdef2080e3739ef2d131))

### <!-- 1 -->🐛 Bug Fixes

- ClientNoteActionにおいて note_idが無かった場合の例外処理を追加 ([51f53b9](https://github.com/yupix/MiPAC/commit/51f53b9d37521ab89dc0e9c583914ee7a55fe441))
- Lint error ([89535cb](https://github.com/yupix/MiPAC/commit/89535cbdbcc1032fb5cda70fb9e4f67ae1579b52))
- Paginationを使用している際にlistに値が1つも無いとIndexErrorになる ([ae44c2d](https://github.com/yupix/MiPAC/commit/ae44c2d68395c5fe482537adf0edec47482153fb))
- RoleUserの型が不適切 ([bd9fafb](https://github.com/yupix/MiPAC/commit/bd9fafbddf9d9fc66191667dfbf3835abd02747d))
- 使用していないimportを削除 ([0cd545d](https://github.com/yupix/MiPAC/commit/0cd545d9655d072f93d1d0a427e37dc66a9c3b2f))
- ドキュメントの生成時に指定するextraを間違えてる ([dafe722](https://github.com/yupix/MiPAC/commit/dafe722564d41d66fbb591e7c5a93a544b6b9ff9))

### <!-- 3 -->📚 Documentation

- CHANGELOG.mdでkeepchangelogを辞めた ([e3ba0b4](https://github.com/yupix/MiPAC/commit/e3ba0b45bcbdab55731793768d6747f1a5ddcd3b))
- Fileモデルにapiプロパティーが追加されたことを記載 ([de50cee](https://github.com/yupix/MiPAC/commit/de50cee1df2904a0c64816682e280550ec03ebfb))
- Migration方法を削除 ([4b0adde](https://github.com/yupix/MiPAC/commit/4b0adde5605e2fad5b7a1f027c4c9d5de35afa9c))
- Update CHANGELOG.md ([7edb970](https://github.com/yupix/MiPAC/commit/7edb970a213a8bc8ca9b455d01168bf4ff0cf739))
- Update README.md ([71b62ad](https://github.com/yupix/MiPAC/commit/71b62adb2f024f137330ea35aa19148618949fb4))
- Update CHANGELOG.md ([46963ff](https://github.com/yupix/MiPAC/commit/46963ff023807465820b6a935cf7ff34395dbc93))
- Update CHANGELOG.md ([8dc78b4](https://github.com/yupix/MiPAC/commit/8dc78b4215d2e7827a5b997c508c275a3f391678))
- Update CHANGELOG.md ([8696846](https://github.com/yupix/MiPAC/commit/869684602b7d64e2284fecca19a323105511fe8c))
- Update README.md ([10aba98](https://github.com/yupix/MiPAC/commit/10aba9867ebd89494cb8ae28db2b62f0f006b2b3))
- Update CHANGELOG.md ([ff11d9b](https://github.com/yupix/MiPAC/commit/ff11d9b8ae68ad9ed7e4e6da39da6c0156edcc60))
- Update README.md ([26a59f9](https://github.com/yupix/MiPAC/commit/26a59f95e8ac5cb8b083496b8b2767c551caef30))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Python3.12に上げる日程を記述 ([decc665](https://github.com/yupix/MiPAC/commit/decc6655f901f96c57b806bfcbd84dea2bfb8b22))
- Urlとtokenを使用してないのに変数に保存しているので削除 ([753c147](https://github.com/yupix/MiPAC/commit/753c147eb478bc8ddb803ae226bc3d498126d18b))
- NoteのVisibilityを共通の型に ([b998a0a](https://github.com/yupix/MiPAC/commit/b998a0a84a4638dcc0cb3139460b6a79435d930d))
- Code Format ([dc6737c](https://github.com/yupix/MiPAC/commit/dc6737c50e08d1de8a8aabaebf6084657bc369ec))
- Ruffだとなんかlineあたりの数が正しくカウントされなくてciが落ちるから廃止 ([349b21b](https://github.com/yupix/MiPAC/commit/349b21b35cd9b915503bb5c18406543de02860e8))
- Can cancel setup_logging when init client ([e30b0e4](https://github.com/yupix/MiPAC/commit/e30b0e4684535b19c96f4a7bacf46423cd842012))
- Codesee使わないので削除 ([2b34ca7](https://github.com/yupix/MiPAC/commit/2b34ca70261f218992fa918ad1dfe811fa70127c))
- 使用していないimportを削除 ([f861e45](https://github.com/yupix/MiPAC/commit/f861e45242309e0ffc0b483d87942f3932977cf2))
- Format ([e8e3e22](https://github.com/yupix/MiPAC/commit/e8e3e223e607a6d2c7ee957ee42e8ec4aedd7dd4))
- Ciのjob名を変更 ([a2837e2](https://github.com/yupix/MiPAC/commit/a2837e2fc693876595ddeda2c0eb90d136607a1f))
- V13でchatを使用しようとしたら例外を返すように Resolve #52 ([0fe2977](https://github.com/yupix/MiPAC/commit/0fe2977810f6d792b871757c4f4b6d59b4f7d56e))
- Api.json周りを更新 ([5ad3412](https://github.com/yupix/MiPAC/commit/5ad3412a08b54ac5922b375dd16ab4e3366de791))
- 使用していないMi.pyの頃のコードを削除 ([1106d94](https://github.com/yupix/MiPAC/commit/1106d948607de8270dae3f3ef367820c86c7a2c5))
- 日本語から英語に ([fecdb01](https://github.com/yupix/MiPAC/commit/fecdb019b2c542463c10028e9f2a13fe775547af))
- フォーマット ([d55183e](https://github.com/yupix/MiPAC/commit/d55183e530db4d12205e11ade39870fb8fb84d8d))
- Issueのテンプレートを追加 ([e735011](https://github.com/yupix/MiPAC/commit/e7350114ddfae1599667babeeffc10bcd19023ce))
- 些細な修正 ([93b9129](https://github.com/yupix/MiPAC/commit/93b91296d6c9e70e4038ffd4c57adab8dad83f5a))
- ドキュメント用のciを追加 ([e8e8fee](https://github.com/yupix/MiPAC/commit/e8e8fee680f896d45248560f098c13f7f7355054))
- Gettextを行うように ([d20f0d3](https://github.com/yupix/MiPAC/commit/d20f0d3ab7155ebfd819de42e0c0c6c2d063c76d))

## [0.4.99] - 2023-06-16

### <!-- 0 -->🚀 Features

- Endpoints更新時にエンドポイントが消えた場合でも型として残すように ([af81ac3](https://github.com/yupix/MiPAC/commit/af81ac3a0593597cb98fe1880e82964770550e4b))
- V13のapi.jsonを更新 ([3dcf384](https://github.com/yupix/MiPAC/commit/3dcf384043f5cd5190a2912d57010e496db44502))
- Endpoint周りを更新 ([47af713](https://github.com/yupix/MiPAC/commit/47af71387aa759d793f4c06842148dbfd626f2ba))
- チャンネルのフォローの概念を追加 #64 ([57c0cf5](https://github.com/yupix/MiPAC/commit/57c0cf5e92873a4b991cc3957cdc9226ccea1e05))
- Clientをインスタンス化する際にサーバーのバージョンを指定できるように ([70beddb](https://github.com/yupix/MiPAC/commit/70beddbf2cff4333e12dbc647d8a2a1a7df8df5b))
- Noteの型をよりよく ([e495ed9](https://github.com/yupix/MiPAC/commit/e495ed969ab1486ab4371b157005a742b82a684e))
- IChannelNoteクラスを追加 ([720c670](https://github.com/yupix/MiPAC/commit/720c67036b47ca2e5f60369a203d238dec699fdb))
- PartialNoteクラスを追加 ([1d280a0](https://github.com/yupix/MiPAC/commit/1d280a00c2528b32c544c2752fa6661c69b26917))
- NoteクラスでPartialNoteを継承するように ([c9faf0a](https://github.com/yupix/MiPAC/commit/c9faf0aac63ffdfe45152549b05e8b2bfb49ca4b))
- Channel周りを整備 #64 ([7b3efaa](https://github.com/yupix/MiPAC/commit/7b3efaa10daef254af3669d025344c47f6a6991c))
- FileやFolderモデルにapiプロパティを追加 ([f7eee76](https://github.com/yupix/MiPAC/commit/f7eee766b33fcf10f70aafa5cee0be5c484ffbbf))
- Bump version ([76c6b4f](https://github.com/yupix/MiPAC/commit/76c6b4f33dd9dc5e194b896e206371c1cc471fb8))
- ロールの作成時にis_explorableを使用できるように ([35130f5](https://github.com/yupix/MiPAC/commit/35130f5533cc366f377dd653bcc721e5a1ba5718))
- Endpoint一覧を更新 ([c1e0912](https://github.com/yupix/MiPAC/commit/c1e09129a67e4ece9c80ce683aff958388b54ecd))
- Update_metaにserver_rules引数を追加 ([2ef06fe](https://github.com/yupix/MiPAC/commit/2ef06fe85081ab9441bff1c0c0ed19465d9a5604))
- AdminEmojiActionsにset_license_bulkメソッドを追加 ([4184f56](https://github.com/yupix/MiPAC/commit/4184f56393f715911471dabf34e8dac20064ec79))
- Paginationをやるためのクラスを追加 ([5b76d45](https://github.com/yupix/MiPAC/commit/5b76d4536b71b305e89c83047158c68e10085ecf))
- Get_notesメソッドをジェネレーターに ([7e5aaff](https://github.com/yupix/MiPAC/commit/7e5aaff9e6aa30f261c065cc34207dec53c74767))
- Pagination化を進めた ([89c53f3](https://github.com/yupix/MiPAC/commit/89c53f3a4f9ce982dd42fbe77cc7feb4b21d0326))
- [**breaking**] 既存のallを用いた全取得をPaginationを用いたものに変更 ([7b9afa4](https://github.com/yupix/MiPAC/commit/7b9afa4b113f943d5590cc06a7ba6abe781c3060))
- Antennaの型とモデルを追加  #74 ([1e45726](https://github.com/yupix/MiPAC/commit/1e45726d576a740320b1f010226a341fd5d6516d))
- Antennaをサポート close #74 ([a3c0e79](https://github.com/yupix/MiPAC/commit/a3c0e79a7ad789c0be5d2df1204fc2d597264d25))
- Apiのエラーでmessageだけでなく、生のエラーも表示するように ([7375330](https://github.com/yupix/MiPAC/commit/737533029a061367134439982af659c3db097a6b))

### <!-- 1 -->🐛 Bug Fixes

- Channelの型を修正 #64 ([3d303dd](https://github.com/yupix/MiPAC/commit/3d303dd5354d7605ffe0ee926cf5591575088caf))
- デフォルト値が入ってない ([1c19685](https://github.com/yupix/MiPAC/commit/1c19685d00fd8cbe568cf1791bf4cfb42bbc0787))

### <!-- 3 -->📚 Documentation

- Update README.md ([e710cb6](https://github.com/yupix/MiPAC/commit/e710cb6c4ab254b74c269a482a85f747f69fa8f0))
- Update CHANGELOG.md ([015070a](https://github.com/yupix/MiPAC/commit/015070ae1cc68ccc5d755441dd21deaee8a4d4d5))
- Update CHANGELOG.md ([12d8cb9](https://github.com/yupix/MiPAC/commit/12d8cb94a2a13ce003a0d6644f1e4f84b44bea6a))
- Update CHANGELOG.md ([8b00614](https://github.com/yupix/MiPAC/commit/8b00614aa1f1b4a992d5bfeac4830218ba6a0747))
- Update CHANGELOG.md ([f558a95](https://github.com/yupix/MiPAC/commit/f558a95f04682dcb728471077d9b1880b8e2b67b))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Misskeyのバージョンを変数に ([cbe7737](https://github.com/yupix/MiPAC/commit/cbe7737e0e655250e21b8fd48ed4b9d603bfa574))
- Format ([d12159e](https://github.com/yupix/MiPAC/commit/d12159ee335b5230d345ae200512fc4a302b25a6))
- Importを整理 ([6c851e8](https://github.com/yupix/MiPAC/commit/6c851e86010ab09a6452249722515695afa0c195))
- Format ([0044ed4](https://github.com/yupix/MiPAC/commit/0044ed44c566c201b951e1a25bb420b014f525ed))
- 新しい実績をサポート ([7eb6f08](https://github.com/yupix/MiPAC/commit/7eb6f084f4a0570486d80e1d4576621cec31302b))
- NoteManagerに何故か存在する `get` メソッドを削除 ([50477ad](https://github.com/yupix/MiPAC/commit/50477ad5767bfda5acdd833b43d6b7dde82eb438))
- Format code ([0e646c5](https://github.com/yupix/MiPAC/commit/0e646c5164f6c365e0a4e3ec72472d7b3168f93b))
- Paginationにレスポンスを保持しないように ([f202891](https://github.com/yupix/MiPAC/commit/f202891009dd3240f68407cf7c58c7ad1b7c0a2a))
- Format ([c731975](https://github.com/yupix/MiPAC/commit/c731975413cf0a7cee3595d42b15b6c9847a8fa8))

## [0.4.1] - 2023-03-13

### <!-- 0 -->🚀 Features

- Support achievement ([69809e8](https://github.com/yupix/MiPAC/commit/69809e87761757717a9f118e4107bcf12654ce17))
- Cache decoratorで同じoverrideを簡単に出来るように #46 ([074a0ba](https://github.com/yupix/MiPAC/commit/074a0ba76891b4ba52988de56b8c6b731a1cff83))
- IIndexStatクラスを追加 #41 ([e023a0c](https://github.com/yupix/MiPAC/commit/e023a0c93f0b149341cb5528183a0aef29b56ca4))
- IndexStatモデルを追加 #41 ([21db087](https://github.com/yupix/MiPAC/commit/21db0878f586a612a19c8dbbc78bae9ea3b45cc5))
- Show-userをサポート ([3749650](https://github.com/yupix/MiPAC/commit/37496503d50680098b5a24ef0cec7c27c2e94b2f))
- Configにdistro属性を追加 ([4ceee32](https://github.com/yupix/MiPAC/commit/4ceee322c0bafa2567f52273961ccbb5161f7f32))
- Support /api/federation/* close #49 ([df1d122](https://github.com/yupix/MiPAC/commit/df1d122c4923930d11938393d099011550814452))
- 今後使用するデータを追加 ([c38d240](https://github.com/yupix/MiPAC/commit/c38d240c21ea3a4378752b79a1584cc9f40d08c0))
- Endpointsを自動で生成するように ([d2c9a8c](https://github.com/yupix/MiPAC/commit/d2c9a8cbf0b6d2284fda21ee2bef5d0e74bb8edb))
- Content field auto convert empty string to None ([72992bb](https://github.com/yupix/MiPAC/commit/72992bbc4f70d2d648fec869cc6ffbb46bcdb0ff))
- バージョンの自動検出機能を追加 close #54 ([a7560c3](https://github.com/yupix/MiPAC/commit/a7560c368a07903887f47cc63cfeca2cac66ed8c))
- ロールに関する型を追加 #53 ([a0f2591](https://github.com/yupix/MiPAC/commit/a0f259129a07a73fdcb37681ecb2a3fc570a42be))
- ロールに関するモデルを追加 #53 ([9a846d5](https://github.com/yupix/MiPAC/commit/9a846d5e2a221ed8c91eec24cdaa84c65d6e5530))
- Roleに関するmanagerやactionを追加 #53 ([a663b46](https://github.com/yupix/MiPAC/commit/a663b46184e7910c7247fad0237b3a70614def94))
- Roleの作成をサポート ([e934113](https://github.com/yupix/MiPAC/commit/e934113f26d59842c7ae9f0d2a40a6fbf24589a4))
- Roleの削除をサポート ([5d0d438](https://github.com/yupix/MiPAC/commit/5d0d4386be012f2bd089186c1306f312bb3c8fe9))
- Roles/listをサポート ([d4de776](https://github.com/yupix/MiPAC/commit/d4de776a058e7d708fd86c6f91a9e308ceb294c8))
- モデルからactionを呼べるように ([118e511](https://github.com/yupix/MiPAC/commit/118e51101b773dfdd3e38d625fa0bac649e0a78b))
- Roles/unassignをサポート ([79b14e3](https://github.com/yupix/MiPAC/commit/79b14e3b4fa93210b164bd5d1fd01f826a8a153f))
- Roles/update-default-policiesをサポート ([cd9c23e](https://github.com/yupix/MiPAC/commit/cd9c23e89ce503152e85071db51f79ac49ff26a1))
- IRoleUser型を追加 ([f55cccf](https://github.com/yupix/MiPAC/commit/f55cccf6b09cbea5d4020ddc2b662d1420780c3a))
- RoleUserモデルを追加 ([caa6cdf](https://github.com/yupix/MiPAC/commit/caa6cdfb52dcbef33a48301c078666589bc79afa))
- Roles/usersをサポート close #53 ([12adba1](https://github.com/yupix/MiPAC/commit/12adba1eafd3382132d9bb11390801c67848d28f))
- 実績の型を追加 ([a54eecf](https://github.com/yupix/MiPAC/commit/a54eecf4cfc9aa9d38dbc41c55cfc21b071aff70))
- Endpoints生成時に変更を加えても失われる可能性があるとコメントを付けるように ([0a0a7fe](https://github.com/yupix/MiPAC/commit/0a0a7fe38957b42e573585566763bfcb85c2c127))
- I/claim-achievementをサポート ([b5c66d2](https://github.com/yupix/MiPAC/commit/b5c66d2b406766c7659f37a10f24641829fbfb31))
- Configにfeaturesを追加 ([0a0f82f](https://github.com/yupix/MiPAC/commit/0a0f82f998e0957880565da8fd4274e49c5ee379))
- Chat系はv13を使用してる場合デフォルトで例外を返すように ([be8d3aa](https://github.com/yupix/MiPAC/commit/be8d3aa5809903270a9cb6ac8ea4546565962140))
- Managerやactionsを自動で作成するためのutilを追加 ([5bb6b70](https://github.com/yupix/MiPAC/commit/5bb6b70b3cee01ade8781f5d8a0fc4db6a8b3f97))
- Templateを元にmanagerやactionsを生成できるように ([c510194](https://github.com/yupix/MiPAC/commit/c5101945ec987cc410e9de3365c570b4b91cf001))
- IBlockingUser型を追加 #58 ([8be5135](https://github.com/yupix/MiPAC/commit/8be513548d309534caae6603308f434823576161))
- Endpointsを生成する際、ダブルクォートではなくシングルクォートを使うように ([6720c8d](https://github.com/yupix/MiPAC/commit/6720c8d12d12d0de8813123f226c7d0eaed75c85))
- BlockingUserモデルを追加 ([905d47b](https://github.com/yupix/MiPAC/commit/905d47ba45e62794d9050eb9d0396b2d00d77942))
- Blocking周りのメソッドなどを充実させた close #58 ([5cd4f05](https://github.com/yupix/MiPAC/commit/5cd4f059f21cb70ef2ff5faa345901a26b0eed0b))
- Noteに増えたreactionの新しい属性をサポート ([a145080](https://github.com/yupix/MiPAC/commit/a145080788517c630f3762d2374be654d5d1acf7))
- V13のapi.jsonを更新 ([8243cad](https://github.com/yupix/MiPAC/commit/8243cad16720ae75bda13cdd7bf54f288769583b))
- Emojiにlicenseを追加 ([14b515e](https://github.com/yupix/MiPAC/commit/14b515e2053c4cb47bff980d396abe2423e356c9))
- IAd型を追加 ([3cbf2f1](https://github.com/yupix/MiPAC/commit/3cbf2f15c55ca88849a179025ddfa3c9b847430c))
- 広告をサポート #62 ([0f7f96f](https://github.com/yupix/MiPAC/commit/0f7f96f3ba62221345b25dd2f6cf0d73278b5b09))
- 広告周りでv12より下のバージョンを使用してる場合は例外を返すように ([f16e2ee](https://github.com/yupix/MiPAC/commit/f16e2ee57419d445f6176b14c944fb4efd49b8bc))
- Config.limitsを追加 ([3740272](https://github.com/yupix/MiPAC/commit/374027232783c2f7518aa296073e4ea226269159))
- Configの引数をすべてキーワード引数に ([e9db4f9](https://github.com/yupix/MiPAC/commit/e9db4f93334d4d729392df6d09690624ae6111dd))
- トークンを使用しなくても使用できるように ([6079056](https://github.com/yupix/MiPAC/commit/6079056716df354ffdb043b84c589eea50d69cc0))
- ChannelLiteモデルを追加 ([c329862](https://github.com/yupix/MiPAC/commit/c3298628cd7f6ef0c0df3a539343bc39452b17f8))
- ChannelクラスはChannelLiteを継承するように ([84474a8](https://github.com/yupix/MiPAC/commit/84474a8c3f6e33b0dd70a862e49eff5164f43ff8))
- Visibilityの型を明記 ([34456e8](https://github.com/yupix/MiPAC/commit/34456e8aedbcdd976d3705e3f10afd69444a041f))
- Bump version ([f2b32f2](https://github.com/yupix/MiPAC/commit/f2b32f2c899f6153433d303d83d9b5b1041e6cd5))
- Mipac.utilをmipac.utils配下に分離 ([381ad6e](https://github.com/yupix/MiPAC/commit/381ad6ec9a40476d50d225fdec17c311d149a4a6))
- Mipac.utilsを使うように ([bd1610f](https://github.com/yupix/MiPAC/commit/bd1610f7bda564b71f605cf2f4d37e7a579f48ee))
- Lowerをkwargsから引数に close #57 ([bdae5c8](https://github.com/yupix/MiPAC/commit/bdae5c87288ac71fd94f38e2e67b7d258b9ce50f))
- Colorsクラスを追加 ([face859](https://github.com/yupix/MiPAC/commit/face85926bac97e2ceafcbe1e05864c5320e320d))
- [**breaking**] LiteUserからnameプロパティを削除 ([5686df3](https://github.com/yupix/MiPAC/commit/5686df313e14aa5768db75f173053343c3a8e53b))
- Client初期化時にsetup_loggingを実行するように ([7a6e4ba](https://github.com/yupix/MiPAC/commit/7a6e4ba2b8806a92cd1645401b8f5439914de77f))
- HTTPClient.request実行時にdebugログを出すように ([8029b67](https://github.com/yupix/MiPAC/commit/8029b67d84698ca30bf7b50b573bf968e3ffc412))
- Mipactlを用いた際に自動でmanager側にactionsをインポートするように ([be554de](https://github.com/yupix/MiPAC/commit/be554de2b41b92799944d2ec19cf1bb9fbec1340))
- CustomEmojiでhostが抜けてる ([45e5cce](https://github.com/yupix/MiPAC/commit/45e5cce30545f8524cac81eb3b54e02935660143))
- 最新のMisskeyのデータに更新 ([c543204](https://github.com/yupix/MiPAC/commit/c543204c995ae9d52048fc8c63f023c90d39a64b))
- Emojiエンドポイントをサポート ([a8b3d71](https://github.com/yupix/MiPAC/commit/a8b3d710136d67c978d5682d6ce6240602f6b659))

### <!-- 1 -->🐛 Bug Fixes

- Misskeyのバージョンによって動かない機能は例外を返すように ([928ca87](https://github.com/yupix/MiPAC/commit/928ca875b23b5c1d1ff612ac3d2a4e3054fbee42))
- Fetch_userでcacheを使わないように ([716b8bb](https://github.com/yupix/MiPAC/commit/716b8bbb51cd2d6023427e964299832322c98ad3))
- 評価の遅延をやってなかった ([1135f83](https://github.com/yupix/MiPAC/commit/1135f83251107a540a41f9dce61ca3d76e7a05d6))
- インデントがちょっと変 ([bd40462](https://github.com/yupix/MiPAC/commit/bd4046281612d51d61a67b71e3ecb24746d681e5))
- Content field no longer supports empty string ([91ab86f](https://github.com/yupix/MiPAC/commit/91ab86f439450fbcc48c1dc282415d2465dea5ed))
- Roles/listのエンドポイントが間違ってた ([b595e83](https://github.com/yupix/MiPAC/commit/b595e83332f0bb40eb6e65ce55dd7c15ab5cd19f))
- Labelerのパスが間違っている ([da87330](https://github.com/yupix/MiPAC/commit/da873302e99bf5b92ed1fd3e7de0345fa3640344))
- Templateの引数が少し間違っている ([e28eb2f](https://github.com/yupix/MiPAC/commit/e28eb2fe64cbd6b7e84107b5ab9e1740e647d896))
- Blackが動かない ([6d8bcd3](https://github.com/yupix/MiPAC/commit/6d8bcd3ed5ac1300cec73db73084b7f5b6ad420d))
- 型を修正 ([56587c6](https://github.com/yupix/MiPAC/commit/56587c61131936c253b276b74cd25950e06a8555))
- Replyのキーがrenoteになっている ([5fe895e](https://github.com/yupix/MiPAC/commit/5fe895e7644102750ca13e1134f0b7c31625c5f4))
- Datetimeのインポートを間違えてる ([4393240](https://github.com/yupix/MiPAC/commit/4393240f077bc91291a366e1adeaef98afc4ffa5))
- PartialCustomEmojiのインスタンス化方法が間違っている ([ab5bc4e](https://github.com/yupix/MiPAC/commit/ab5bc4e15567b554017f41e2d9f953616f229a61))

### <!-- 3 -->📚 Documentation

- Update README.md ([611f6ac](https://github.com/yupix/MiPAC/commit/611f6ac70f73baccd09e621087d1835e4c3b09db))
- Update CHANGELOG.md ([4332fc0](https://github.com/yupix/MiPAC/commit/4332fc0bcb84be173cbacf1c07d06c4157815f38))
- バッヂを追加 ([4cddb8f](https://github.com/yupix/MiPAC/commit/4cddb8fb572be35ec62f10e9849256bdbe7f0f36))
- Update CHANGELOG.md ([e2c1ce6](https://github.com/yupix/MiPAC/commit/e2c1ce68a423c028cdb0e61ea77f3582c220c5f3))
- Update CHANGELOG.md ([752188a](https://github.com/yupix/MiPAC/commit/752188ac718debe261d1730ec9cb157bb3e03c47))
- Pypiのダウンロード数を表示するように ([1704627](https://github.com/yupix/MiPAC/commit/17046277ef8aab1fb2bdb26116131533ef29a8c2))
- Update CHANGELOG.md ([969ce9e](https://github.com/yupix/MiPAC/commit/969ce9e919aeb3b7b526debad272241c3174bae2))
- Update CHANGELOG.md ([3c41fb1](https://github.com/yupix/MiPAC/commit/3c41fb1118ed9606dbdd80ac9835409813606e0c))
- Update CHANGELOG.md ([aedc160](https://github.com/yupix/MiPAC/commit/aedc160730e8abc28fcf0a52cbcdf06c3f890668))
- Update CHANGELOG.md ([a736302](https://github.com/yupix/MiPAC/commit/a73630205275a490872a2dc0e288f8e1c3692858))
- Update README.md ([245df59](https://github.com/yupix/MiPAC/commit/245df5932920126bbe2f36163cc718b9c7935583))
- Update CHANGELOG.md ([7bad5d8](https://github.com/yupix/MiPAC/commit/7bad5d81ad1c40cc69d3adf27b0faf184b7259b4))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Achievementsは13以降の機能の為13以外では動かないように ([519633d](https://github.com/yupix/MiPAC/commit/519633d7e8b6fc30f9c8bfca22783c62e141e1a2))
- Pullrequestで自動でラベルを付けるように ([951be5c](https://github.com/yupix/MiPAC/commit/951be5ca67f33392908c5d57c467832c5e59abbf))
- コミュニティー関係のものを追加 ([05e6b80](https://github.com/yupix/MiPAC/commit/05e6b80f02aec806bf5e356ca2ee5d19a3d5c12a))
- Issue templateを追加 ([5621df6](https://github.com/yupix/MiPAC/commit/5621df6de51ccffadd9bcf9eb3e46d9f2b8da8ca))
- コードのフォーマット ([3855f94](https://github.com/yupix/MiPAC/commit/3855f94ae4348f540c4a0a135335de0b5a2bc635))
- 同じこと書くのも大変なのでエラーの文を定数化 ([0ae6c7b](https://github.com/yupix/MiPAC/commit/0ae6c7b78e40b75b412fe87a1dbf60e99ca343e0))
- フォーマット ([46ce875](https://github.com/yupix/MiPAC/commit/46ce87539a3cdf208755cd849d5ffdcb8b033d3e))
- Aiohttpでバージョンを指定するように ([6d75852](https://github.com/yupix/MiPAC/commit/6d75852a4e5c1e09119256ced477c7cecc638419))
- Sphinx周り使わないので削除 ([8910122](https://github.com/yupix/MiPAC/commit/89101227100808f06eb8fe828e22153a1e2967c2))
- 使わなくなった設定ファイルなどを削除 ([53c1f88](https://github.com/yupix/MiPAC/commit/53c1f88189c0e2bf27b91a5838e66b17e16d9f0c))
- Format code ([2dc4983](https://github.com/yupix/MiPAC/commit/2dc49839a5cad993457365e87608e485b10e3b85))
- Setup.pyにutilsを追記 ([16f445b](https://github.com/yupix/MiPAC/commit/16f445bb15dbf7a64f4c0801ba198a779a709d19))
- Format ([bbc2ea0](https://github.com/yupix/MiPAC/commit/bbc2ea041ed33eed9349c6a11b6ab71330448eda))

## [0.4.0] - 2023-01-18

### <!-- 0 -->🚀 Features

- Configを大幅に変更 #MP-32 ([e07ef93](https://github.com/yupix/MiPAC/commit/e07ef9340417451ee26d6928c206506cf5939bb6))
- Emojisが含まれなくなったのでoptionに移動 #MP-34 ([358232d](https://github.com/yupix/MiPAC/commit/358232df9faf5784eeadef24f165d828e0489ced))
- ILiteUserにavatar_colorプロパティを追加 #MP-34 ([54d1abd](https://github.com/yupix/MiPAC/commit/54d1abdb85e713bd931067a96c78db3f316a32b0))
- Bump version ([2d6e4e0](https://github.com/yupix/MiPAC/commit/2d6e4e04b2453a86972ecd05ffefe215d82c4c45))

### <!-- 3 -->📚 Documentation

- Update README.md ([bda30fe](https://github.com/yupix/MiPAC/commit/bda30fe0de79ef5f8524d790175631354fc48fc4))
- Update CHANGELOG.md ([024bf88](https://github.com/yupix/MiPAC/commit/024bf880aec86923322894f3ef56c0dcf8c208f1))
- Update README.md ([9616a20](https://github.com/yupix/MiPAC/commit/9616a20c7892f7e873c80fa254ef3eb748163dbe))
- Update README.md ([a5ac8e6](https://github.com/yupix/MiPAC/commit/a5ac8e6528677495b8dfc99244e5246e34bd7265))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- コードのフォーマット ([5c51438](https://github.com/yupix/MiPAC/commit/5c514383bdf51a751c6bfe7e5ccf6eecaeb795b5))

## [0.3.99] - 2022-12-25

### <!-- 0 -->🚀 Features

- ディレクトリ名をabcからabstractに ([caaaa4e](https://github.com/yupix/MiPAC/commit/caaaa4e021446712a93699ae540079124e6568d1))
- Status_codeが204の場合Trueを返すように ([fe403a8](https://github.com/yupix/MiPAC/commit/fe403a82bc242cd613e2d1e1eef3b2aa2c2ef6e0))
- Add `get_state` method a `ClientNoteActions` ([cb3c27e](https://github.com/yupix/MiPAC/commit/cb3c27ea47587f141e5a378fe9aa459159b13a91))

### <!-- 1 -->🐛 Bug Fixes

- 削除したディレクトリをpackagesから削除 ([9b88d26](https://github.com/yupix/MiPAC/commit/9b88d26d3fe4e57e1b4c3b3691a067261f865390))
- 0などといった物まで `remove_dict_empty` で消えていた ([8167be3](https://github.com/yupix/MiPAC/commit/8167be332759f1e3cb50a74af909e1904d3f72b6))
- V11だとis_muted_threadが無い ([33b7188](https://github.com/yupix/MiPAC/commit/33b7188922c0e2c9fdc88e6a2a22536d07775636))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Update flake8 settings ([46aaf29](https://github.com/yupix/MiPAC/commit/46aaf29ac4ba8e7aa60a0d6466531158c45178f5))
- Update .flake8 ([4a36d13](https://github.com/yupix/MiPAC/commit/4a36d134dd0e559b8bc13c4bb6f0a3662f24fa97))
- Fix filename ([ac1c24a](https://github.com/yupix/MiPAC/commit/ac1c24a7604f85e0f410155eea050bd78a48da57))
- Mipac.actions.adminをpackagesに追記 ([3b4068b](https://github.com/yupix/MiPAC/commit/3b4068b8fff52b54ca1f8ed8483353c8d5c874bf))
- Ruffを使ったlintを追加 ([7fc3273](https://github.com/yupix/MiPAC/commit/7fc32737e928b8843af2d31a17993400fb19836d))

## [0.3.1] - 2022-12-24

### <!-- 0 -->🚀 Features

- Added class `NoteDeleted` ([b55ee05](https://github.com/yupix/MiPAC/commit/b55ee0560e55bdc6f84f68efc5f5937690bbb824))

### <!-- 3 -->📚 Documentation

- Update CHANGELOG.md ([5c67c21](https://github.com/yupix/MiPAC/commit/5c67c21c708800d5b96de6c0f54a113cfe0f08d3))

## [0.2.7] - 2022-12-22

### <!-- 1 -->🐛 Bug Fixes

- TypedDict type error ([c44cf13](https://github.com/yupix/MiPAC/commit/c44cf13f65985cfde4ba751ac9aeada569c663de))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Remove unused imports ([51f5628](https://github.com/yupix/MiPAC/commit/51f5628e9d7c1de5e56099ef266eebdcc4ac7cde))

## [0.2.6] - 2022-12-08

### <!-- 7 -->⚙️ Miscellaneous Tasks

- フォーマット ([d7cf189](https://github.com/yupix/MiPAC/commit/d7cf1891999a1b5fb29473e59ebba3653770762e))

## [0.2.4] - 2022-12-08

### <!-- 0 -->🚀 Features

- ClientNoteActionsを追加 ([eebe40c](https://github.com/yupix/MiPAC/commit/eebe40c2d53171dfc20f2e9918a8f2f9e57f4d80))
- Noteクラスで使用するactionをClientNoteActionsに ([1669aac](https://github.com/yupix/MiPAC/commit/1669aac90ac9f7525f4558af2146cbaefae05b49))
- Bump version ([66beedb](https://github.com/yupix/MiPAC/commit/66beedbf68b4f27f7d287f631da6d772738cc525))

### <!-- 1 -->🐛 Bug Fixes

- レスポンスがdictだった場合小文字に出来ずモデルが作れない ([e038f3b](https://github.com/yupix/MiPAC/commit/e038f3b92cd09b9a7e62f0e97811c9b955c7cac6))
- ノートを作成した際のモデルが正しく作成できない ([0eba2de](https://github.com/yupix/MiPAC/commit/0eba2de5984d25e3040778b563218c4d6e2b5924))

## [0.2.2] - 2022-11-27

### <!-- 0 -->🚀 Features

- Bump version ([3d84e9d](https://github.com/yupix/MiPAC/commit/3d84e9dfa5c214ce585e988d7654cc884d79434e))
- Propert用のdeprecatedを追加 ([eedd3a6](https://github.com/yupix/MiPAC/commit/eedd3a6b177cd43d3ff9338650f378c082f65238))
- LiteUserにnameを追加(非推奨) ([cff59b7](https://github.com/yupix/MiPAC/commit/cff59b7fda111d87c10a83732ca8ce24a9a31e87))
- Bump version ([3cfdbfc](https://github.com/yupix/MiPAC/commit/3cfdbfc6f09c6e64bbcd363c6aa4691eb0828cce))

### <!-- 1 -->🐛 Bug Fixes

- 使っているインポートがTYPE_CHECKINGに入ってた ([ab4b78a](https://github.com/yupix/MiPAC/commit/ab4b78a7130035fa4dd2df6ff5fc540e348228d6))
- LiteUserのhostを取得するとkeyErrorになる可能性がある ([32d3f68](https://github.com/yupix/MiPAC/commit/32d3f68e8bbac2d5480560bc4b4e59d3e7b39074))
- LiteUserの属性instanceでkeyErrorになる可能性がある ([11f52d7](https://github.com/yupix/MiPAC/commit/11f52d739d81c7e29f9af2e7982fe6dad2d9bcec))
- Get_mentionでusernameではなくnicknameを使っていた ([2d387ac](https://github.com/yupix/MiPAC/commit/2d387ac7aad08cc66d0e99ba341db0a2a440d060))

### <!-- 3 -->📚 Documentation

- Update CHANGELOG.md ([05ac3c6](https://github.com/yupix/MiPAC/commit/05ac3c638d06841b8ded69c709b530714590932d))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Deprecated周りを変更 ([177f234](https://github.com/yupix/MiPAC/commit/177f234d173832e88a8d676791fadc43e65a540b))
- 些細な変更 ([65cbd52](https://github.com/yupix/MiPAC/commit/65cbd52425de23046be66188d6c9c135eb6c1c58))
- Flake8のライブラリ変更に伴う修正 ([5d145ab](https://github.com/yupix/MiPAC/commit/5d145abcab9b5e8d34dba89f63863eca7a207412))

## [0.2.1] - 2022-11-24

### <!-- 0 -->🚀 Features

- ノートの一括取得に対応 #MP-20 Fixed ([cd52f71](https://github.com/yupix/MiPAC/commit/cd52f710c6901b2311df24615df26955c18c8636))
- Bump version ([27c3a9b](https://github.com/yupix/MiPAC/commit/27c3a9bc5f4552b1fd56221b3129720219613bf8))
- Python-versioneerを追加 ([c374fef](https://github.com/yupix/MiPAC/commit/c374fefc09b6f998621a3da6feb083fb9453e545))

### <!-- 1 -->🐛 Bug Fixes

- NotificationのReactionを別の名前に変更 #MP-16 Fixed ([fda2290](https://github.com/yupix/MiPAC/commit/fda2290b86cca4d9a951e9b32fe7f8b398dbab31))

### <!-- 3 -->📚 Documentation

- Update CHANGELOG.md ([847e54c](https://github.com/yupix/MiPAC/commit/847e54cc0bec5493d92295ae7d2c32f71c9bbc8a))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Websocket使用時のレスポンスクラスを変更 ([2f2b9e6](https://github.com/yupix/MiPAC/commit/2f2b9e6fa1f32308c61513de28788c4159e6e3dd))
- Debugログを削除 ([a592c77](https://github.com/yupix/MiPAC/commit/a592c77bae9e29993a8543a5cbf3807206c43448))
- Docstring を追加 ([8872004](https://github.com/yupix/MiPAC/commit/88720043289197cfd4d8b8f779049082a7e34cb7))
- IUserLite => ILiteUserに変える close #18 ([827adac](https://github.com/yupix/MiPAC/commit/827adac33c786d01b06da8b29c7a1e54a3b50b96))
- Userモデルのnameをnicknameに変える close #17 ([2a7a956](https://github.com/yupix/MiPAC/commit/2a7a9564e1f4ebb00b1164dfea75b8570e88c939))
- Type hintの追加 ([d8df46f](https://github.com/yupix/MiPAC/commit/d8df46f23ac42e36848ae90b0e24789d7690590f))
- クラス名の更新 ([c4d56f7](https://github.com/yupix/MiPAC/commit/c4d56f70d7d2737f0a1f12f0938b73a5a3009e62))
- デバッグログの消し忘れ ([cbe30cc](https://github.com/yupix/MiPAC/commit/cbe30cc011c93211b699d99bce8a9a5b7a23db08))
- フォーマット ([45a35ea](https://github.com/yupix/MiPAC/commit/45a35ea5dfbdce88abe96981c342786f52ea0723))
- Pyproject-flake8を廃止してflake8に #MP-21 Fixed ([7fc8fea](https://github.com/yupix/MiPAC/commit/7fc8fea65c1aca59dbb4882e23e3a3641025bf21))
- Flake8のルールを変更 ([bac1d7c](https://github.com/yupix/MiPAC/commit/bac1d7cf526f050df0c8945bf145fe9a32f1eeda))
- Limitが100以上だった場合例外を返すように ([a77cc5c](https://github.com/yupix/MiPAC/commit/a77cc5ca8aed8b818643b9df5e0f0cdf8d328713))
- Format ([82250c4](https://github.com/yupix/MiPAC/commit/82250c43a58aac40a9b06c53cf0575f4e5c5ef34))
- 不要なファイルを削除 ([aa5a2ae](https://github.com/yupix/MiPAC/commit/aa5a2aea857b3ebf2b7cddd76ec3d18b87ffbfac))
- Flake8のルールを変更 ([f8e1eae](https://github.com/yupix/MiPAC/commit/f8e1eae9a15fa73ca71c1a84730d464c83730382))

## [0.2.0] - 2022-11-02

### <!-- 0 -->🚀 Features

- Init ([376328f](https://github.com/yupix/MiPAC/commit/376328f26f4d2c9a962258b3fd16f90300334ff5))
- APIError の追加 ([fcf8a57](https://github.com/yupix/MiPAC/commit/fcf8a57d3270e8b9afa05555ed430d79f36b220b))
- APIのエラーを返すように issue: #1 ([ca37a45](https://github.com/yupix/MiPAC/commit/ca37a45c8c76bb08db6c0929e0b5de3ce0f2a3c6))
- 必須の引数がNoneの場合の対策を追加 issue #2 ([94e5376](https://github.com/yupix/MiPAC/commit/94e5376e9893d8105a147837ba96c04867b9572b))
- Blackの設定をしたので再フォーマット ([7f38b70](https://github.com/yupix/MiPAC/commit/7f38b70575585e4e52ffb4e02551208c0d64c93f))
- __all__の定義 issue #3 ([73b4e3b](https://github.com/yupix/MiPAC/commit/73b4e3b717cefbeaf869cec4ab9e21c4dff2b35c))
- __init__のモデルを定義 ([8f41d2a](https://github.com/yupix/MiPAC/commit/8f41d2a7d1f4f87a338ac9992cfa2b86e7c3e940))
- Get_meメソッドの実装 issue #4 ([a598111](https://github.com/yupix/MiPAC/commit/a5981119f6d5104bca8de4a744e48d1743037609))
- __all__の定義 issue #3 ([e59d0d4](https://github.com/yupix/MiPAC/commit/e59d0d433fa14d0856aab4b476bded0dc20c90ac))
- __init__の定義 ([759476d](https://github.com/yupix/MiPAC/commit/759476d0994248fd45a8b45f15f94d4d0703a047))
- Sessionを取得できるように ([133f0fb](https://github.com/yupix/MiPAC/commit/133f0fb920e4e13612eb2f8dbac2b4a886bdab32))
- Bump version ([518b7e2](https://github.com/yupix/MiPAC/commit/518b7e29392bb0543143528aa8de0cd6229f2ea9))
- AuthClientクラスを追加 - issue #7 ([4c7a20f](https://github.com/yupix/MiPAC/commit/4c7a20f718a9d2ed5cb7c37594371ee21412aea5))
- __all__を定義 issue #3 ([d6acfc8](https://github.com/yupix/MiPAC/commit/d6acfc8969bd1817dd1e38952ee2f5f7f5182a43))
- [**breaking**] Drive周りの大規模な修正 ([73ba01c](https://github.com/yupix/MiPAC/commit/73ba01c5381d95b293bacd93fa26db4a4d02ccc4))
- __all__を定義 issue #3 ([4c3ae13](https://github.com/yupix/MiPAC/commit/4c3ae13ba229f2d6e9e5c6099666c67a65b50dc2))
- Configクラスを追加 issue #6 ([0b253bb](https://github.com/yupix/MiPAC/commit/0b253bb373b81e2cfbe61b75b668bff67a64a085))
- Configを使うように issue #6 ([862cbbe](https://github.com/yupix/MiPAC/commit/862cbbe51d265826c9f2567b71b7357218296f1b))
- Configを使うように ([b14f5e8](https://github.com/yupix/MiPAC/commit/b14f5e87b75cf51358c37fc2bd5f393366fe1906))
- Pre-commitの設定を追加 ([1916103](https://github.com/yupix/MiPAC/commit/191610330c2e755ab5d548d52a7600d7b4043ee7))
- Bump version to 0.1.0 ([f2c3cff](https://github.com/yupix/MiPAC/commit/f2c3cffe8012dd3e7d64e2fbfb9df5daaf1154e9))
- Noteの型を修正 issue #11 ([d0e214c](https://github.com/yupix/MiPAC/commit/d0e214c4404d989454ff1b50656bb1cbac72b17b))
- RawReaction, RawRenoteの型を修正 issue #11 ([de1807e](https://github.com/yupix/MiPAC/commit/de1807ed97be09f422f2368c21b304a7683a6ad9))
- APIError発生時にhttpのstatus codeを返すように issue #12 ([14250cb](https://github.com/yupix/MiPAC/commit/14250cbd7ee0940b8224d484f2740a2bc237540f))
- Typingを用いないDict, Listの記法に変更 ([269ba75](https://github.com/yupix/MiPAC/commit/269ba75ccbf781ad4e2daf99ef064aa9dbf82204))
- RawChannel クラスを追加 ([265e26e](https://github.com/yupix/MiPAC/commit/265e26eaf9f5115646b72050656ee3c5cbbb9d29))
- Modelerクラスを追加 ([e1be082](https://github.com/yupix/MiPAC/commit/e1be082e19dcfe71eb5e03ec27d37811cc5029e7))
- 循環インポートを回避するためのmodelerを使ったモデルのインスタンス化に変更 ([5fba3c6](https://github.com/yupix/MiPAC/commit/5fba3c6bc3d6b80808cd28fe432ebff06ab6afa7))
- Close #9 ([99fca60](https://github.com/yupix/MiPAC/commit/99fca60873dd9336e860a2d606fdfcd14a380026))
- Endpointをまとめた変数を用意 ([640dd6b](https://github.com/yupix/MiPAC/commit/640dd6b1ecddd6b9f6a4a43bb0bd4514881af201))
- Request methodの型を正確に ([897433a](https://github.com/yupix/MiPAC/commit/897433ad1e5d9b96385602579d191ff80eee8d6f))
- IInstanceLiteクラスを追加 ([7768883](https://github.com/yupix/MiPAC/commit/77688834b79666d95d64467dacc14d7932006b3a))
- ICustomEmojiLite タイプを追加 ([f06340b](https://github.com/yupix/MiPAC/commit/f06340b2dd55a4caf727843690b285827ab44302))
- IUserLite タイプを追加 ([b306703](https://github.com/yupix/MiPAC/commit/b306703ca4e49994b680c28f4a2d2e1f1f8acffe))
- INote タイプを大幅に修正 ([26c8c5b](https://github.com/yupix/MiPAC/commit/26c8c5b421634c74415ec806cd135c3ddcb33577))
- InstanceLite モデルを追加 ([bd44e2d](https://github.com/yupix/MiPAC/commit/bd44e2db81d0d10f22f91a020385a0f889f344a4))
- UserLite モデルを追加 ([7342096](https://github.com/yupix/MiPAC/commit/734209663bc750d9dae21829c0cc7ad4bdae3949))
- Noteモデルを大幅に変更 ([4668b18](https://github.com/yupix/MiPAC/commit/4668b18227321bca3037356b9d85122c450fed7f))
- モデルの作成時に新しいRawクラスを使わないように ([4506daa](https://github.com/yupix/MiPAC/commit/4506daab477c3ca8c35ef27d9a771d4a800d4434))
- Liteディレクトリをpackagesに追記 ([5ab5891](https://github.com/yupix/MiPAC/commit/5ab58910f3b98fa62b22b9d871cccac7e15b746d))
- INoteReaction タイプを追加 #10 ([86ddc2f](https://github.com/yupix/MiPAC/commit/86ddc2f6844133d3bef2c4de1017bd8e95fbe72d))
- NoteReaction クラスを大幅に変更 ([4cf2349](https://github.com/yupix/MiPAC/commit/4cf23493ffef4efcafe41656fd9317e2a010c201))
- RawReaction, RawNote クラスを削除 #10 ([c3814c7](https://github.com/yupix/MiPAC/commit/c3814c78291d0eb55e262aeb63171cf2b4260a5c))
- 通知に関する型を定義 ([8835faa](https://github.com/yupix/MiPAC/commit/8835faa999ac2a2dc356989e93a3d8283d98eb90))
- Reaction型を新しく #10 ([aeb6e6d](https://github.com/yupix/MiPAC/commit/aeb6e6d0f9b2e863d2957d8689a6cfbe77f57675))
- RawRenote, Renoteクラスを削除 #10 ([2a198ce](https://github.com/yupix/MiPAC/commit/2a198ce933679e2a571093ec608ffcbbd57d3d17))
- `RawEmoji`, `Emoji` クラスを削除 #10 ([9e45f5c](https://github.com/yupix/MiPAC/commit/9e45f5c9eb20fdd3d66203e4320f58d41c4de932))
- IAds タイプを追加 ([d9f40c4](https://github.com/yupix/MiPAC/commit/d9f40c4222be936dea4ffb5415761c4eec56f109))
- インスタンスに関する型を追加 ([fd25a26](https://github.com/yupix/MiPAC/commit/fd25a26815d226dd417442c31188da3ca27816b5))
- LiteInstanceMeta クラスを追加 ([847d317](https://github.com/yupix/MiPAC/commit/847d3173950976c2d174e1cc33bfea2eded00883))
- InstanceMeta クラスを大幅に変更 ([374c695](https://github.com/yupix/MiPAC/commit/374c695e1ed2b0e7a0101ba48311f545b8ca5aa6))
- IRenoteクラスを削除 ([250de36](https://github.com/yupix/MiPAC/commit/250de3605ebf6ccf6091ffe477bf423ab8a711f8))
- Progress #10 ([f7ef493](https://github.com/yupix/MiPAC/commit/f7ef49329def418022886c98e153cb3b3611b727))
- 不要なインポートの削除 #10 ([bdf163a](https://github.com/yupix/MiPAC/commit/bdf163a6c52c10de9a49f225ec4cf31ef57caa0f))
- Progress #10 ([9607435](https://github.com/yupix/MiPAC/commit/96074357d71eb935b75865761d1bd3082580690a))
- チャットでRawModelを使わないように #10 ([f756c15](https://github.com/yupix/MiPAC/commit/f756c15c831e296c99659f5ce166ce78991b76bd))
- Channel周りでRawModel使わないように #10 ([bd0d5b5](https://github.com/yupix/MiPAC/commit/bd0d5b5d467d042abbef362e98b01d36e0cce824))
- `UserLite` -> `LiteUser` に変更 ([ce85ece](https://github.com/yupix/MiPAC/commit/ce85eceaf5a2fb1312923df2d9f39ac986adf5fd))
- Poll系でRawModelを廃止 #10 ([3e50c07](https://github.com/yupix/MiPAC/commit/3e50c07e064fa832cc6dda37da586b6631361500))
- Orjsonがあればorjsonを使うように ([0d345a1](https://github.com/yupix/MiPAC/commit/0d345a14e114a9f3ce38971d058f7871fd4a1b1a))
- フォローリクエストを取得できるように close #12 ([d142355](https://github.com/yupix/MiPAC/commit/d14235575554f755b53956024ece25fd4d6bfbd9))
- ドキュメントを作成する close #13 ([90ea7e8](https://github.com/yupix/MiPAC/commit/90ea7e86fb1556768a060658345489a6a49c0e35))
- キャッシュに関する関数を追加 ([ab97fdb](https://github.com/yupix/MiPAC/commit/ab97fdbdb1670f696205ae2b52239fa2c364abd3))
- Noteの取得をcacheするように #14 ([34ae2a3](https://github.com/yupix/MiPAC/commit/34ae2a33ba91553117e359a1795fdd4cb6be0879))
- Chatをmanagerとactionに分離 ([73c1fdc](https://github.com/yupix/MiPAC/commit/73c1fdc290d09fe919e477d16885d93f51edc69f))
- .editorconfigを追加 ([f276ff5](https://github.com/yupix/MiPAC/commit/f276ff5f3caa21d9acb7d1f0403865ae9d4d8d82))
- Chatモデルにactionを追加 ([30e5abb](https://github.com/yupix/MiPAC/commit/30e5abba263c6b7a599f69b6cc93f59a320a6e6a))
- Channelモデルにhas_unread_note属性を追加 ([d0096f9](https://github.com/yupix/MiPAC/commit/d0096f971e8dd2bc782957def352e30a750459f9))
- Bump version ([d2eb6d7](https://github.com/yupix/MiPAC/commit/d2eb6d796d16ca1b6d51f436dc33f26de7fe5c47))

### <!-- 1 -->🐛 Bug Fixes

- コメントアウトしてる関数をimportしてた ([3ed1417](https://github.com/yupix/MiPAC/commit/3ed1417b5cc50b41c591fb83dfbbda69a056b8a9))
- Typo ([dfd1001](https://github.com/yupix/MiPAC/commit/dfd100186745aa22f807a900381c23ae9e466bad))
- Chatの削除でmessage_idが必須になっていた ([3c454c2](https://github.com/yupix/MiPAC/commit/3c454c2d7419e68165562116d83a4e4a88c62cf0))
- 重複したキーを__all__に定義していた ([c3e6f45](https://github.com/yupix/MiPAC/commit/c3e6f45e57b4507117dcedc39cf53686faa9046f))
- そのファイルにないクラスを__all__に定義していた ([05fdf81](https://github.com/yupix/MiPAC/commit/05fdf81db9a3b6f6e37ceb2af8153f95e0ec0a17))
- Get_meメソッドで認証を使用していなかった ([b89e968](https://github.com/yupix/MiPAC/commit/b89e9682ba42a88b123c14a87ee19017ab653e94))
- モデルの修正 ([8cd38cb](https://github.com/yupix/MiPAC/commit/8cd38cba03edd811fdc69e1197237c56ae5ecf8a))
- 型が正しくない - issue #9 ([34456bc](https://github.com/yupix/MiPAC/commit/34456bc8a25a7629afc89d1d9d498e50e136c778))
- 重複した属性を削除 ([33d723a](https://github.com/yupix/MiPAC/commit/33d723a0ab8c2373aca69a60159a4bb6c19fac79))
- 取得方法が型にあってない ([0906477](https://github.com/yupix/MiPAC/commit/0906477566289553bd8c05c5bd6d8a03abff7043))
- 属性の型が正しくないのを修正 - issue #9 ([7dbf845](https://github.com/yupix/MiPAC/commit/7dbf8450f3827f77ceaaf96184aca35d95f896f0))
- Get_pagesでreturnしていなかった ([3082084](https://github.com/yupix/MiPAC/commit/30820844ef4b36c6fd3d10d17a2d2a9f339f1bd3))
- Folderクラスにclientを渡していない ([7426f82](https://github.com/yupix/MiPAC/commit/7426f82dc7a87daac61fe5ae90a0032cb5c8049c))
- Typo ([9802909](https://github.com/yupix/MiPAC/commit/9802909d394a4d24251435ba867866990e257ec1))
- Fileが添付できない ([894c0b3](https://github.com/yupix/MiPAC/commit/894c0b39d7b464f340d1b112614c6652711cac6d))
- 実行時に型を解決できない ([eadd7c3](https://github.com/yupix/MiPAC/commit/eadd7c3a0cef1f97c19c9184f33cda16517e8510))
- Close yupix/mipa#6 ([f27ec06](https://github.com/yupix/MiPAC/commit/f27ec067470df586cfa515b8a2e4aa7c048a2a2f))
- エンドポイントが間違っている ([b41bc0b](https://github.com/yupix/MiPAC/commit/b41bc0bbc6ab24a36c45ac90a834c6a85fd88a1a))
- APIが動かなくなる ([b12f92d](https://github.com/yupix/MiPAC/commit/b12f92de0e0c91ab8ede53438625b4a051667f8f))
- 未解決の参照 ([58eeb64](https://github.com/yupix/MiPAC/commit/58eeb64863d9a2d331b8ed55c2c886bb7602bf31))
- Typo ([5cfe5ea](https://github.com/yupix/MiPAC/commit/5cfe5ea865aad8d2ae427f186c0c5606ab70316f))
- Selfのインポートが出来ないので別の方法に変更 ([1a9d4db](https://github.com/yupix/MiPAC/commit/1a9d4db75eea601761354b0c1d3704319bb04ebc))
- ファイル名が間違ってる ([6ab4716](https://github.com/yupix/MiPAC/commit/6ab4716bbf2dd60eb8d7f8b12ef883d8b0437ed1))

### <!-- 2 -->🚜 Refactor

- ユーザー周りのモデルを改善 ([971911f](https://github.com/yupix/MiPAC/commit/971911f90455f9b5b690fa155ecc5c28a813aae9))

### <!-- 3 -->📚 Documentation

- Update README.md ([6d955ff](https://github.com/yupix/MiPAC/commit/6d955ff1391681525b2b687ab3ceb88d9517bbf1))
- Update README.md ([0eb4edf](https://github.com/yupix/MiPAC/commit/0eb4edf0ae32f9affbff412a409b86512d1ef6de))
- Update README.md ([2a36480](https://github.com/yupix/MiPAC/commit/2a3648037f586ab4db70d4c527f37092fac9cc57))
- Update CHANGELOG.md ([dae3fda](https://github.com/yupix/MiPAC/commit/dae3fdaaf3674deedf139a88778917d4883df025))
- Update README.md ([75387b9](https://github.com/yupix/MiPAC/commit/75387b9bccec0c40284b661a9e074b98ebecd6fc))
- Update README.md ([7e4a23f](https://github.com/yupix/MiPAC/commit/7e4a23fb6be1480751900302bffead728c6d310c))
- Update CHANGELOG.md ([60e85f4](https://github.com/yupix/MiPAC/commit/60e85f4dd04973d368f639d35e26aacf17e6679c))
- Update CHANGELOG.md ([06998a8](https://github.com/yupix/MiPAC/commit/06998a84c5b5d8ff3bdea44196d4ccf640a47361))
- Update CHANGELOG.md ([e452d53](https://github.com/yupix/MiPAC/commit/e452d53b99283f7deea69174c4683b2114e9652b))
- Update CHANGELOG.md ([b6a5e3e](https://github.com/yupix/MiPAC/commit/b6a5e3ecbf3f790523b71801a43ef9cdfd7f4397))
- Update CHANGELOG.md ([97d3b73](https://github.com/yupix/MiPAC/commit/97d3b73f87c17b515a385e305fb50cb89da5eec7))
- Update CHANGELOG.md ([567c86a](https://github.com/yupix/MiPAC/commit/567c86af86829e17a512c1656fff8835e9d30012))
- Specialthanksを削除 ([7d0d6e3](https://github.com/yupix/MiPAC/commit/7d0d6e3e7847c8c77f9824b20c2e4b8868549a75))

### <!-- 7 -->⚙️ Miscellaneous Tasks

- Add LICENSE ([61afad4](https://github.com/yupix/MiPAC/commit/61afad4c85b203329d9ed336f36be0fb2a1ac0d0))
- Axblackを使用してフォーマット ([8eb34b3](https://github.com/yupix/MiPAC/commit/8eb34b321a9d9dcf9044f8508fc163c28ded23d3))
- ノートの投稿範囲をDocStringに記述 ([e06712b](https://github.com/yupix/MiPAC/commit/e06712b5637cacb8e7e65bdaf4f56e0f1d15df2a))
- Requestの戻り地をanyに ([4e778dd](https://github.com/yupix/MiPAC/commit/4e778dd35c9dff4adf643ee08410a82c7da40c20))
- 型の修正と細かな不具合の修正 ([d24a887](https://github.com/yupix/MiPAC/commit/d24a88735871fee5f602c602f9acae4b514b1ff6))
- Isortでフォーマット ([d086726](https://github.com/yupix/MiPAC/commit/d086726cdbd90e20f731651560a639693116f2ad))
- Update setup.py ([fb23c67](https://github.com/yupix/MiPAC/commit/fb23c6798edc6bcf9d8521866bef121dae70ced3))
- Update .gitignore ([304f241](https://github.com/yupix/MiPAC/commit/304f24163a5d80ba87693e8a2019a57a5ab80b12))
- 重複した属性を削除 ([55a4da3](https://github.com/yupix/MiPAC/commit/55a4da30fcb14810d3714bf87560843047b3750d))
- Add .onedev-buildspec.yml ([fbf4999](https://github.com/yupix/MiPAC/commit/fbf49996a39be89deadd536d59d09a95a573b9e2))
- Edit .onedev-buildspec.yml ([eb085fd](https://github.com/yupix/MiPAC/commit/eb085fd584d1ab3647475921814caaf8e24c59dd))
- Image名を間違えてた ([2208dea](https://github.com/yupix/MiPAC/commit/2208deabcc9134780a891c41e93b559c2c5a8791))
- Edit .onedev-buildspec.yml ([9626c72](https://github.com/yupix/MiPAC/commit/9626c72812c1ec3e8eaf09b3e4f5b958419f2f16))
- コードのフォーマット ([5a12854](https://github.com/yupix/MiPAC/commit/5a12854abcc1eb88d1b9702a36043051af56b1e4))
- 些細な変更 ([bea4cc4](https://github.com/yupix/MiPAC/commit/bea4cc4c23e642dfb20fdab25e81fa0de6075d9f))
- 属性名の変更 ([0d40ec9](https://github.com/yupix/MiPAC/commit/0d40ec9d1e9b5a57ab2f72ae34f188bf1bfc4e01))
- 循環importの原因となるコードを修正 ([c223989](https://github.com/yupix/MiPAC/commit/c223989aa4b170b4ebf499e4515573b9bd36ec13))
- 名前の変更 ([32e7773](https://github.com/yupix/MiPAC/commit/32e7773e8271a592b88b146f8a0a8066949704ff))
- Add MANIFEST.in ([060e755](https://github.com/yupix/MiPAC/commit/060e7554fe5c5d2a27f88044c741cdcb2633c7b3))
- Importの修正 ([010f91b](https://github.com/yupix/MiPAC/commit/010f91b3fa5e926cc411f2e98f007835b9ecd966))
- 開発環境の整備 ([1e3260d](https://github.com/yupix/MiPAC/commit/1e3260d27b826d2b975a10bb64129b50294a0dac))
- コメントアウトの削除・修正 ([a554421](https://github.com/yupix/MiPAC/commit/a5544210cbc29c0c2d224b1b60b8284a4cbe6b2b))
- 機能の修正 ([fbad268](https://github.com/yupix/MiPAC/commit/fbad2680223417fd489b82bcb4291a6186a2c741))
- フォーマットの修正 ([7e5b5ed](https://github.com/yupix/MiPAC/commit/7e5b5ed03d230212d2d9064d040abe3681efaa73))
- 終わってるTODOを削除 ([b7bac42](https://github.com/yupix/MiPAC/commit/b7bac42dc66346e2f1ae97c491c86a498c2c5f45))
- 些細な修正 ([db56dc8](https://github.com/yupix/MiPAC/commit/db56dc8ec0061d2991bdcd4011baf68d677775af))
- Folderクラスでclientを受け取るように ([8516497](https://github.com/yupix/MiPAC/commit/851649779d6484e7185ae4ffec8b3555747eacb3))
- Mypyだと一部の構文が理解できないのでciで使わないように ([40b9afc](https://github.com/yupix/MiPAC/commit/40b9afc14b66c0e199a3122e945ffb1b438fc58c))
- Check_authの中身を更に関数に分けた ([6ac0519](https://github.com/yupix/MiPAC/commit/6ac0519798f606ed47d95dcfb7b1847bdc1a1cf9))
- コードのフォーマット ([42c83c9](https://github.com/yupix/MiPAC/commit/42c83c94e22d71410c93622ee3db7135cf0f218a))
- 開発環境に必要なライブラリを追記 ([a96d643](https://github.com/yupix/MiPAC/commit/a96d643250713da56f9f2d7cdb7cd4458a34e3bc))
- Update issue templates ([77e6130](https://github.com/yupix/MiPAC/commit/77e613002aa6e47bc78edcec43012e2d20c8e711))
- 些細な変更 ([e34ef07](https://github.com/yupix/MiPAC/commit/e34ef070fd68878c33c469929048c09b4bd18032))
- フォーマット ([fdb8fc8](https://github.com/yupix/MiPAC/commit/fdb8fc8543df82c10a5607a73c063b1d8b4ffa2e))
- 型などの些細な修正 ([612f8c5](https://github.com/yupix/MiPAC/commit/612f8c573f05ab61aca499a32dfb37edc10c6dce))
- Update .gitignore ([902db49](https://github.com/yupix/MiPAC/commit/902db49eddd8e32cf3d710efe08f20e2f930d283))
- Importの整理 ([8984b86](https://github.com/yupix/MiPAC/commit/8984b864ac690c774202b6b2f2948598ba12066a))
- IReactionRequired, IReactionタイプを削除 ([ecaf96a](https://github.com/yupix/MiPAC/commit/ecaf96acb6c743efdd75b26403ad0bb5edc57633))
- フォーマット ([ccb8c3b](https://github.com/yupix/MiPAC/commit/ccb8c3b553cc667fbd0e35e5151ed35a076b344b))
- TypedDictをつけ忘れてる ([834e80a](https://github.com/yupix/MiPAC/commit/834e80a357c34313d90e8113943a18d1993f2ad5))
- Requestメソッドにreplace_list引数を追加 ([73062bc](https://github.com/yupix/MiPAC/commit/73062bc26f4fc4758ea22e447c3d5e354aad6314))
- クラス名の変更に伴う修正 ([770f15e](https://github.com/yupix/MiPAC/commit/770f15e4548f6b6860b40888f029583aa562d20e))
- 新しい型を用いるように ([9723af5](https://github.com/yupix/MiPAC/commit/9723af5fec59d3c5bdbde32e9c6d9d3e9124d233))
- フォーマット ([d504d64](https://github.com/yupix/MiPAC/commit/d504d64ed11d3859052a6e63676fc0901cf1b0ac))
- 些細な変更 ([5deaa16](https://github.com/yupix/MiPAC/commit/5deaa16ba2a6ff2c27cec45c6978b851975b285a))
- コードのフォーマット ([fab6166](https://github.com/yupix/MiPAC/commit/fab6166153e3ad89b02ec694a4a03ed9b702fb19))
- Extrasにspeedを追加 ([8d89bc7](https://github.com/yupix/MiPAC/commit/8d89bc7482830397009780bc5fa8a5148f8632a0))
- 型の修正 ([f1fc584](https://github.com/yupix/MiPAC/commit/f1fc584d8ccd150f0947a45edbcd711b52f805f8))
- ドキュメント用のrequirements.txtを追加 ([042a9ab](https://github.com/yupix/MiPAC/commit/042a9ab72e1336fb2ab1bd2781dbf6b93a3a7f65))
- Readthedocsの設定を追加 ([0485075](https://github.com/yupix/MiPAC/commit/0485075b287153c0ae74e80dd57c5fab3bc36dbb))
- 依存関係にmipacのものを追加 ([0b8eddd](https://github.com/yupix/MiPAC/commit/0b8eddd46189865989689d8da89f702aa6b4ac32))
- [**breaking**] Client.actionをClient.apiに変更 ([2187876](https://github.com/yupix/MiPAC/commit/2187876aec07031db79d7bb75280df9b260343f8))
- フォーマット ([fc56cbc](https://github.com/yupix/MiPAC/commit/fc56cbcd331c4b9ae78473046228d437d845c1ef))
- 不要なimportを削除 ([3d9ffd6](https://github.com/yupix/MiPAC/commit/3d9ffd6d4f9cd340f5515c08931215c74be342df))
- .gitattributesを追加 ([43262f5](https://github.com/yupix/MiPAC/commit/43262f58e197e7da56be29e23dc63e0ef393fbbd))
- 改行コードをlfに ([3dddcf6](https://github.com/yupix/MiPAC/commit/3dddcf69a639dc89a1da41f1877ba2aec9ff5c34))
- Importの修正 ([bf0558c](https://github.com/yupix/MiPAC/commit/bf0558cfbf90bcef4ab5c6ded13d907671384ea4))
- キャッシュでgroupを指定しない場合はdefaultに入れるように ([2657c25](https://github.com/yupix/MiPAC/commit/2657c25745831619cee9c748e8b6c394407f753e))
- 型周りの修正 ([9f9bdb2](https://github.com/yupix/MiPAC/commit/9f9bdb2f5f0fc71de6cf26763201a023df6e62a1))
- Flaek8を使ったテストを行うように ([fb4843e](https://github.com/yupix/MiPAC/commit/fb4843e57a9f4e8393860b73ff79cd4e8a7b9c1f))
- 使用していないimportを削除 ([94d4715](https://github.com/yupix/MiPAC/commit/94d4715d149a44a3d207c9cb3e6d932b17374a5b))
- Aiocacheを廃止 ([9f49870](https://github.com/yupix/MiPAC/commit/9f4987081e56c242298a03ae2da9975cef1c2541))
- 型の修正 ([0693078](https://github.com/yupix/MiPAC/commit/069307811c79c43de7fe3d689b8d3e44495e8608))
- リリース時にpypiにアップロードするように ([f711d7e](https://github.com/yupix/MiPAC/commit/f711d7e75a57daf29c88aa72b0d75ea4b7c2ab23))

[0.8.0]: https://github.com/yupix/MiPAC/compare/0.7.4..0.8.0
[0.7.4]: https://github.com/yupix/MiPAC/compare/0.7.3..0.7.4
[0.7.3]: https://github.com/yupix/MiPAC/compare/0.7.2..0.7.3
[0.7.2]: https://github.com/yupix/MiPAC/compare/0.7.1..0.7.2
[0.7.1]: https://github.com/yupix/MiPAC/compare/0.7.0..0.7.1
[0.7.0]: https://github.com/yupix/MiPAC/compare/0.6.3..0.7.0
[0.6.3]: https://github.com/yupix/MiPAC/compare/0.6.2..0.6.3
[0.6.2]: https://github.com/yupix/MiPAC/compare/0.6.1..0.6.2
[0.6.1]: https://github.com/yupix/MiPAC/compare/0.6.0..0.6.1
[0.6.0]: https://github.com/yupix/MiPAC/compare/0.5.99..0.6.0
[0.5.99]: https://github.com/yupix/MiPAC/compare/0.5.1..0.5.99
[0.5.1]: https://github.com/yupix/MiPAC/compare/0.4.99..0.5.1
[0.4.99]: https://github.com/yupix/MiPAC/compare/0.4.2..0.4.99
[0.4.1]: https://github.com/yupix/MiPAC/compare/0.4.0..0.4.1
[0.4.0]: https://github.com/yupix/MiPAC/compare/0.3.99..0.4.0
[0.3.99]: https://github.com/yupix/MiPAC/compare/0.3.1..0.3.99
[0.3.1]: https://github.com/yupix/MiPAC/compare/0.3.0..0.3.1
[0.2.7]: https://github.com/yupix/MiPAC/compare/0.2.6..0.2.7
[0.2.6]: https://github.com/yupix/MiPAC/compare/0.2.5..0.2.6
[0.2.4]: https://github.com/yupix/MiPAC/compare/0.2.2..0.2.4
[0.2.2]: https://github.com/yupix/MiPAC/compare/0.2.1..0.2.2
[0.2.1]: https://github.com/yupix/MiPAC/compare/v0.2.0..0.2.1

<!-- generated by git-cliff -->
