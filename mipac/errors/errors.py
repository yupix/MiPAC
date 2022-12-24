from .base import APIError


class AccessDeniedError(APIError):
    """ アクセス権限がありません。 """


class AlreadyAddedError(APIError):
    """  """


class AlreadyBlockingError(APIError):
    """ すでにブロックしています。 """


class AlreadyClippedError(APIError):
    """  """


class AlreadyExpiredError(APIError):
    """  """


class AlreadyFavoritedError(APIError):
    """ 既にお気に入り登録されています。 """


class AlreadyFollowingError(APIError):
    """ すでにフォローしています。 """


class AlreadyInvitedError(APIError):
    """  """


class AlreadyLikedError(APIError):
    """ すでにいいねをつけています。 """


class AlreadyMutingError(APIError):
    """ すでにそのユーザーをミュートしています。 """


class AlreadyPinnedError(APIError):
    """ 指定されたノートは既にピン留めされています。 """


class AlreadyPromotedError(APIError):
    """  """


class AlreadyReactedError(APIError):
    """ 既にリアクションしています。 """


class AlreadyVotedError(APIError):
    """  """


class AvatarNotAnImageError(APIError):
    """ アバター画像に、画像ではないファイルが指定されました。 """


class BannerNotAnImageError(APIError):
    """ バナー画像に、画像ではないファイルが指定されました。 """


class BlockedError(APIError):
    """ ユーザーにブロックされています。 """


class BlockeeIsYourselfError(APIError):
    """ 自分のブロックを解除しようとしました。 """


class BlockingError(APIError):
    """ ユーザーをブロックしています。 """


class CannotCreateAlreadyExpiredPollError(APIError):
    """ アンケートの期限の指定が誤っています。 """


class CannotRenoteToAPureRenoteError(APIError):
    """ 単純なRenoteを再度Renoteすることはできません。 """


class CannotReplyToAPureRenoteError(APIError):
    """ 単純なRenoteに返信することはできません。 """


class CannotReportTheAdminError(APIError):
    """ 管理者を通報しようとしました。 """


class CannotReportYourselfError(APIError):
    """ 自身を通報しようとしました。 """


class ContentRequiredError(APIError):
    """  """


class CredentialRequiredError(APIError):
    """ クレデンシャル必須のエンドポイントにクレデンシャル無しでリクエストされました。 """


class FailedToResolveRemoteUserError(APIError):
    """ リモートユーザーの検索に失敗しました。 """


class FolloweeIsYourselfError(APIError):
    """ 自分のフォローを解除しようとしました。 """


class FollowerIsYourselfError(APIError):
    """ 自分をフォロワー解除しようとしました。 """


class FollowRequestNotFoundError(APIError):
    """ フォローリクエストがありません。 """


class ForbiddenError(APIError):
    """  """


class GroupAccessDeniedError(APIError):
    """  """


class GtlDisabledError(APIError):
    """ グローバルタイムラインが無効になっています。 """


class HasChildFilesOrFoldersError(APIError):
    """ フォルダーが空ではありません。 """


class InappropriateError(APIError):
    """ 不適切なコンテンツを含んでいる可能性があると判定されました。 """


class InternalErrorError(APIError):
    """ サーバー内部で問題が発生しました。引き続き問題が発生する場合は管理者にお問い合わせください。 """


class InvalidChoiceError(APIError):
    """  """


class InvalidFileNameError(APIError):
    """ ファイル名が不正です。 """


class InvalidParamError(APIError):
    """ リクエストパラメータに誤りがあります。 """


class InvalidRegexpError(APIError):
    """ 正規表現が不正です。 """


class InvalidUrlError(APIError):
    """  """


class IsOwnerError(APIError):
    """  """


class LtlDisabledError(APIError):
    """ ローカルタイムラインが無効になっています。 """


class MoSuchFileError(APIError):
    """  """


class MuteeIsYourselfError(APIError):
    """ 自分に対してミュートを解除しようとしました。 """


class NameAlreadyExistsError(APIError):
    """ 同じURLにページがすでに存在します。 """


class NotBlockingError(APIError):
    """ ブロックしていないユーザーです。 """


class NotFavoritedError(APIError):
    """ お気に入り登録されていません。 """


class NotFollowingError(APIError):
    """ ユーザーにフォローされていません。 """


class NotLikedError(APIError):
    """ いいねをつけていないページです。 """


class NotMutingError(APIError):
    """ 対象となるユーザーをそもそもミュートしていません。 """


class NotReactedError(APIError):
    """ リアクションしていません。 """


class NoFollowRequestError(APIError):
    """ ユーザーからのフォローリクエストがありません。 """


class NoFreeSpaceError(APIError):
    """ ドライブに空き容量がありません。 """


class NoPollError(APIError):
    """  """


class NoSuchAdError(APIError):
    """  """


class NoSuchAnnouncementError(APIError):
    """ お知らせが存在しません。 """


class NoSuchAntennaError(APIError):
    """  """


class NoSuchAppError(APIError):
    """ アプリが存在しません。 """


class NoSuchAvatarError(APIError):
    """ アバター画像のファイルが存在しません。 """


class NoSuchBannerError(APIError):
    """ バナー画像のファイルが存在しません。 """


class NoSuchChannelError(APIError):
    """ 指定されたチャンネルが存在しないか、アクセスが許可されていません。 """


class NoSuchClipError(APIError):
    """  """


class NoSuchEmojiError(APIError):
    """  """


class NoSuchFileError(APIError):
    """ ファイルが存在しません。 """


class NoSuchFolderError(APIError):
    """ フォルダーが存在しません。 """


class NoSuchGroupError(APIError):
    """  """


class NoSuchGroupMemberError(APIError):
    """  """


class NoSuchHashtagError(APIError):
    """ ハッシュタグが存在しません。 """


class NoSuchInvitationError(APIError):
    """  """


class NoSuchListError(APIError):
    """  """


class NoSuchMessageError(APIError):
    """  """


class NoSuchNoteError(APIError):
    """ 指定されたノートが存在しないか、アクセスが許可されていません。 """


class NoSuchNotificationError(APIError):
    """ 通知が存在しません。 """


class NoSuchObjectError(APIError):
    """  """


class NoSuchPageError(APIError):
    """ ページが存在しません。 """


class NoSuchParentFolderError(APIError):
    """ 親フォルダーが存在しません。 """


class NoSuchPostError(APIError):
    """  """


class NoSuchRenoteTargetError(APIError):
    """ Renoteに指定されたノートが存在しないか、アクセスが許可されていません。 """


class NoSuchReplyTargetError(APIError):
    """ 返信先に指定されたノートが存在しないか、アクセスが許可されていません。 """


class NoSuchSessionError(APIError):
    """ セッションが存在しません。 """


class NoSuchUserError(APIError):
    """ ユーザーが存在しません。 """


class NoSuchUserGroupError(APIError):
    """  """


class NoSuchUserListError(APIError):
    """  """


class NoSuchWebhookError(APIError):
    """ Webhookが存在しません。 """


class PendingSessionError(APIError):
    """  """


class PermissionDeniedError(APIError):
    """ 与えられたクレデンシャルには必要なパーミッションがありません。 """


class PinLimitExceededError(APIError):
    """ これ以上ピン留めできません。 """


class RateLimitExceededError(APIError):
    """ レートリミットによる制限のため一時的に利用できません。 """


class ReactionsNotPublicError(APIError):
    """ リアクションが公開されていません。 """


class RecipientIsYourselfError(APIError):
    """  """


class StlDisabledError(APIError):
    """ ソーシャルタイムラインが無効になっています。 """


class YourAccountSuspendedError(APIError):
    """ アカウントが凍結されているため利用できません。 """


class YourPageError(APIError):
    """ 自身のページにいいねをつけようとしました。 """


class YourPostError(APIError):
    """  """


class YouAreOwnerError(APIError):
    """  """


class YouHaveBeenBlockedError(APIError):
    """ ブロックされているユーザーのノートにリアクションは行えません。 """
