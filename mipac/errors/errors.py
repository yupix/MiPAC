from .base import APIError


class AccessDeniedError(APIError):
    """Access denied."""


class AlreadyAddedError(APIError):
    """That user has already been added to that list."""


class AlreadyBlockingError(APIError):
    """You are already blocking that user."""


class AlreadyClippedError(APIError):
    """The note has already been clipped."""


class AlreadyEndedError(APIError):
    """That game has already ended."""


class AlreadyExpiredError(APIError):
    """The poll is already expired."""


class AlreadyFavoritedError(APIError):
    """You have not favorited the list."""


class AlreadyFollowingError(APIError):
    """You are already following that user."""


class AlreadyLikedError(APIError):
    """The flash has already been liked."""


class AlreadyMovedError(APIError):
    """Account was already moved to another account."""


class AlreadyMutingError(APIError):
    """You are already muting that user."""


class AlreadyPinnedError(APIError):
    """That note has already been pinned."""


class AlreadyPromotedError(APIError):
    """The note has already promoted."""


class AlreadyReactedError(APIError):
    """You are already reacting to that note."""


class AlreadyVotedError(APIError):
    """You have already voted."""


class AuthenticationFailedError(APIError):
    """Authentication failed. Please ensure your token is correct."""


class AvatarNotAnImageError(APIError):
    """The file specified as an avatar is not an image."""


class BannerNotAnImageError(APIError):
    """The file specified as a banner is not an image."""


class BirthdayDateFormatInvalidError(APIError):
    """Birthday date format is invalid."""


class BlockedError(APIError):
    """You are blocked by that user."""


class BlockeeIsYourselfError(APIError):
    """Blockee is yourself."""


class BlockingError(APIError):
    """You are blocking that user."""


class BothWithRepliesAndWithFilesError(APIError):
    """Specifying both withReplies and withFiles is not supported"""


class CannotCreateAlreadyExpiredPollError(APIError):
    """Poll is already expired."""


class CannotRenoteDueToVisibilityError(APIError):
    """You can not Renote due to target visibility."""


class CannotRenoteOutsideOfChannelError(APIError):
    """Cannot renote outside of channel."""


class CannotRenoteToAPureRenoteError(APIError):
    """You can not Renote a pure Renote."""


class CannotReplyToAnInvisibleNoteError(APIError):
    """You cannot reply to an invisible Note."""


class CannotReplyToAPureRenoteError(APIError):
    """You can not reply to a pure Renote."""


class CannotReplyToSpecifiedVisibilityNoteWithExtendedVisibilityError(APIError):
    """You cannot reply to a specified visibility note with extended visibility."""


class CannotReportTheAdminError(APIError):
    """Cannot report the admin."""


class CannotReportYourselfError(APIError):
    """Cannot report yourself."""


class CanNotDeleteInviteCodeError(APIError):
    """You can't delete this invite code."""


class ContainsProhibitedWordsError(APIError):
    """Cannot post because it contains prohibited words."""


class ContainsTooManyMentionsError(APIError):
    """Cannot post because it exceeds the allowed number of mentions."""


class CredentialRequiredError(APIError):
    """Credential required."""


class DestinationAccountForbidsError(APIError):
    """Destination account doesn't have proper 'Known As' alias, or has already moved."""


class DuplicateNameError(APIError):
    """Duplicate name."""


class EmptyFileError(APIError):
    """That file is empty."""


class ExceededLimitOfCreateInviteCodeError(APIError):
    """You have exceeded the limit for creating an invitation code."""


class ExtResourceHashDidntMatchError(APIError):
    """Hash did not match."""


class ExtResourceReturnedInvalidSchemaError(APIError):
    """External resource returned invalid schema."""


class FailedToResolveRemoteUserError(APIError):
    """Failed to resolve remote user."""


class FolloweeIsYourselfError(APIError):
    """Followee is yourself."""


class FollowerIsYourselfError(APIError):
    """Follower is yourself."""


class FollowRequestNotFoundError(APIError):
    """Follow request not found."""


class ForbiddenError(APIError):
    """Forbidden."""


class ForbiddenToSetYourselfError(APIError):
    """You can't set yourself as your own alias."""


class GtlDisabledError(APIError):
    """Global timeline has been disabled."""


class HasChildFilesOrFoldersError(APIError):
    """This folder has child files or folders."""


class InappropriateError(APIError):
    """Cannot upload the file because it has been determined that it possibly contains inappropriate content."""


class IncorrectPasswordError(APIError):
    """Incorrect password."""


class InternalErrorError(APIError):
    """Internal error occurred. Please contact us if the error persists."""


class InvalidChoiceError(APIError):
    """Choice ID is invalid."""


class InvalidDateTimeError(APIError):
    """Invalid date-time format"""


class InvalidFileNameError(APIError):
    """Invalid file name."""


class InvalidParamError(APIError):
    """Invalid param."""


class InvalidRegexpError(APIError):
    """Invalid Regular Expression."""


class InvalidSeedError(APIError):
    """Provided seed is invalid."""


class InvalidUrlError(APIError):
    """Invalid URL"""


class IsRemoteUserError(APIError):
    """Currently unavailable to display reactions of remote users. See https://github.com/misskey-dev/misskey/issues/12964"""


class IAmAiError(APIError):
    """You sent a request to Ai-chan, Misskey's showgirl, instead of the server."""


class LtlDisabledError(APIError):
    """Local timeline has been disabled."""


class MuteeIsYourselfError(APIError):
    """Mutee is yourself."""


class NameAlreadyExistsError(APIError):
    """Specified name already exists."""


class NotAssignedError(APIError):
    """Not assigned."""


class NotBlockingError(APIError):
    """You are not blocking that user."""


class NotFavoritedError(APIError):
    """You have not marked that note a favorite."""


class NotFollowingError(APIError):
    """The other use is not following you."""


class NotLikedError(APIError):
    """You have not liked that flash."""


class NotMutingError(APIError):
    """You are not muting that user."""


class NotReactedError(APIError):
    """You are not reacting to that note."""


class NotRootForbiddenError(APIError):
    """The root can't migrate."""


class NoFollowRequestError(APIError):
    """No follow request."""


class NoFreeSpaceError(APIError):
    """Cannot upload the file because you have no free space of drive."""


class NoPollError(APIError):
    """The note does not attach a poll."""


class NoSecurityKeyError(APIError):
    """No security key."""


class NoSuchAdError(APIError):
    """No such ad."""


class NoSuchAnnouncementError(APIError):
    """No such announcement."""


class NoSuchAntennaError(APIError):
    """No such antenna."""


class NoSuchAppError(APIError):
    """No such app."""


class NoSuchAvatarError(APIError):
    """No such avatar file."""


class NoSuchBannerError(APIError):
    """No such banner file."""


class NoSuchChannelError(APIError):
    """No such channel."""


class NoSuchClipError(APIError):
    """No such clip."""


class NoSuchEmojiError(APIError):
    """No such emoji."""


class NoSuchFileError(APIError):
    """No such file."""


class NoSuchFlashError(APIError):
    """No such flash."""


class NoSuchFolderError(APIError):
    """No such folder."""


class NoSuchGameError(APIError):
    """No such game."""


class NoSuchHashtagError(APIError):
    """No such hashtag."""


class NoSuchInviteCodeError(APIError):
    """No such invite code."""


class NoSuchKeyError(APIError):
    """No such key."""


class NoSuchListError(APIError):
    """No such list."""


class NoSuchNoteError(APIError):
    """No such note."""


class NoSuchObjectError(APIError):
    """No such object."""


class NoSuchPageError(APIError):
    """No such page."""


class NoSuchParentFolderError(APIError):
    """No such parent folder."""


class NoSuchPostError(APIError):
    """No such post."""


class NoSuchRegistrationError(APIError):
    """No such registration."""


class NoSuchRenoteTargetError(APIError):
    """No such renote target."""


class NoSuchReplyTargetError(APIError):
    """No such reply target."""


class NoSuchRoleError(APIError):
    """No such role."""


class NoSuchSessionError(APIError):
    """No such session."""


class NoSuchUserError(APIError):
    """No such user."""


class NoSuchUserListError(APIError):
    """No such user list."""


class NoSuchWebhookError(APIError):
    """No such webhook."""


class PendingSessionError(APIError):
    """This session is not completed yet."""


class PinLimitExceededError(APIError):
    """You can not pin notes any more."""


class RateLimitExceededError(APIError):
    """Rate limit exceeded. Please try again later."""


class ReactionsNotPublicError(APIError):
    """Reactions of the user is not public."""


class RecursiveNestingError(APIError):
    """It can not be structured like nesting folders recursively."""


class RemoteUserNotAllowedError(APIError):
    """Not allowed to load the remote user's list"""


class RestrictedByRoleError(APIError):
    """This feature is restricted by your role."""


class SameNameEmojiExistsError(APIError):
    """Emoji that have same name already exists."""


class StlDisabledError(APIError):
    """Hybrid timeline has been disabled."""


class TargetIsYourselfError(APIError):
    """Target user is yourself."""


class TooBigFileError(APIError):
    """That file is too big."""


class TooManyAntennasError(APIError):
    """You cannot create antenna any more."""


class TooManyClipsError(APIError):
    """You cannot create clip any more."""


class TooManyClipNotesError(APIError):
    """You cannot add notes to the clip any more."""


class TooManyMutedWordsError(APIError):
    """Too many muted words."""


class TooManyUserlistsError(APIError):
    """You cannot create user list any more."""


class TooManyUsersError(APIError):
    """You can not push users any more."""


class TooManyWebhooksError(APIError):
    """You cannot create webhook any more."""


class TwoFactorNotEnabledError(APIError):
    """2fa not enabled."""


class UnavailableError(APIError):
    """Translate of notes unavailable."""


class UnexpectedFileTypeError(APIError):
    """We need csv file."""


class UriNullError(APIError):
    """Local User ActivityPup URI is null."""


class UserIsDeletedError(APIError):
    """User is deleted."""


class UserNotFoundError(APIError):
    """User not found."""


class YourFlashError(APIError):
    """You cannot like your flash."""


class YourPageError(APIError):
    """You cannot like your page."""


class YourPostError(APIError):
    """You cannot like your post."""


class YouHaveBeenBlockedError(APIError):
    """You cannot push this user because you have been blocked by this user."""
