"""
=======================
        WARNING
=======================
 This file is automatically generated by compiler/endpoints.py.
 If this file is modified and then auto-generated, the changes will be lost.
"""

from typing import Literal

ENDPOINTS = Literal[
    "/api/admin/meta",
    "/api/admin/abuse-user-reports",
    "/api/admin/accounts/create",
    "/api/admin/accounts/delete",
    "/api/admin/accounts/find-by-email",
    "/api/admin/ad/create",
    "/api/admin/ad/delete",
    "/api/admin/ad/list",
    "/api/admin/ad/update",
    "/api/admin/announcements/create",
    "/api/admin/announcements/delete",
    "/api/admin/announcements/list",
    "/api/admin/announcements/update",
    "/api/admin/avatar-decorations/create",
    "/api/admin/avatar-decorations/delete",
    "/api/admin/avatar-decorations/list",
    "/api/admin/avatar-decorations/update",
    "/api/admin/delete-all-files-of-a-user",
    "/api/admin/unset-user-avatar",
    "/api/admin/unset-user-banner",
    "/api/admin/drive/clean-remote-files",
    "/api/admin/drive/cleanup",
    "/api/admin/drive/files",
    "/api/admin/drive/show-file",
    "/api/admin/emoji/add-aliases-bulk",
    "/api/admin/emoji/add",
    "/api/admin/emoji/copy",
    "/api/admin/emoji/delete-bulk",
    "/api/admin/emoji/delete",
    "/api/admin/emoji/list-remote",
    "/api/admin/emoji/list",
    "/api/admin/emoji/remove-aliases-bulk",
    "/api/admin/emoji/set-aliases-bulk",
    "/api/admin/emoji/set-category-bulk",
    "/api/admin/emoji/set-license-bulk",
    "/api/admin/emoji/update",
    "/api/admin/federation/delete-all-files",
    "/api/admin/federation/refresh-remote-instance-metadata",
    "/api/admin/federation/remove-all-following",
    "/api/admin/federation/update-instance",
    "/api/admin/get-index-stats",
    "/api/admin/get-table-stats",
    "/api/admin/get-user-ips",
    "/api/admin/invite/create",
    "/api/admin/invite/list",
    "/api/admin/promo/create",
    "/api/admin/queue/clear",
    "/api/admin/queue/deliver-delayed",
    "/api/admin/queue/inbox-delayed",
    "/api/admin/queue/promote",
    "/api/admin/queue/stats",
    "/api/admin/relays/add",
    "/api/admin/relays/list",
    "/api/admin/relays/remove",
    "/api/admin/reset-password",
    "/api/admin/resolve-abuse-user-report",
    "/api/admin/send-email",
    "/api/admin/server-info",
    "/api/admin/show-moderation-logs",
    "/api/admin/show-user",
    "/api/admin/show-users",
    "/api/admin/suspend-user",
    "/api/admin/unsuspend-user",
    "/api/admin/update-meta",
    "/api/admin/delete-account",
    "/api/admin/update-user-note",
    "/api/admin/roles/create",
    "/api/admin/roles/delete",
    "/api/admin/roles/list",
    "/api/admin/roles/show",
    "/api/admin/roles/update",
    "/api/admin/roles/assign",
    "/api/admin/roles/unassign",
    "/api/admin/roles/update-default-policies",
    "/api/admin/roles/users",
    "/api/announcements",
    "/api/antennas/create",
    "/api/antennas/delete",
    "/api/antennas/list",
    "/api/antennas/notes",
    "/api/antennas/show",
    "/api/antennas/update",
    "/api/ap/get",
    "/api/ap/show",
    "/api/app/create",
    "/api/app/show",
    "/api/auth/session/generate",
    "/api/auth/session/show",
    "/api/auth/session/userkey",
    "/api/blocking/create",
    "/api/blocking/delete",
    "/api/blocking/list",
    "/api/channels/create",
    "/api/channels/featured",
    "/api/channels/follow",
    "/api/channels/followed",
    "/api/channels/owned",
    "/api/channels/show",
    "/api/channels/timeline",
    "/api/channels/unfollow",
    "/api/channels/update",
    "/api/channels/favorite",
    "/api/channels/unfavorite",
    "/api/channels/my-favorites",
    "/api/channels/search",
    "/api/charts/active-users",
    "/api/charts/ap-request",
    "/api/charts/drive",
    "/api/charts/federation",
    "/api/charts/instance",
    "/api/charts/notes",
    "/api/charts/user/drive",
    "/api/charts/user/following",
    "/api/charts/user/notes",
    "/api/charts/user/pv",
    "/api/charts/user/reactions",
    "/api/charts/users",
    "/api/clips/add-note",
    "/api/clips/remove-note",
    "/api/clips/create",
    "/api/clips/delete",
    "/api/clips/list",
    "/api/clips/notes",
    "/api/clips/show",
    "/api/clips/update",
    "/api/clips/favorite",
    "/api/clips/unfavorite",
    "/api/clips/my-favorites",
    "/api/drive",
    "/api/drive/files",
    "/api/drive/files/attached-notes",
    "/api/drive/files/check-existence",
    "/api/drive/files/create",
    "/api/drive/files/delete",
    "/api/drive/files/find-by-hash",
    "/api/drive/files/find",
    "/api/drive/files/show",
    "/api/drive/files/update",
    "/api/drive/files/upload-from-url",
    "/api/drive/folders",
    "/api/drive/folders/create",
    "/api/drive/folders/delete",
    "/api/drive/folders/find",
    "/api/drive/folders/show",
    "/api/drive/folders/update",
    "/api/drive/stream",
    "/api/email-address/available",
    "/api/endpoint",
    "/api/endpoints",
    "/api/federation/followers",
    "/api/federation/following",
    "/api/federation/instances",
    "/api/federation/show-instance",
    "/api/federation/update-remote-user",
    "/api/federation/users",
    "/api/federation/stats",
    "/api/following/create",
    "/api/following/delete",
    "/api/following/update",
    "/api/following/update-all",
    "/api/following/invalidate",
    "/api/following/requests/accept",
    "/api/following/requests/cancel",
    "/api/following/requests/list",
    "/api/following/requests/reject",
    "/api/gallery/featured",
    "/api/gallery/popular",
    "/api/gallery/posts",
    "/api/gallery/posts/create",
    "/api/gallery/posts/delete",
    "/api/gallery/posts/like",
    "/api/gallery/posts/show",
    "/api/gallery/posts/unlike",
    "/api/gallery/posts/update",
    "/api/get-online-users-count",
    "/api/get-avatar-decorations",
    "/api/hashtags/list",
    "/api/hashtags/search",
    "/api/hashtags/show",
    "/api/hashtags/trend",
    "/api/hashtags/users",
    "/api/i",
    "/api/i/claim-achievement",
    "/api/i/favorites",
    "/api/i/gallery/likes",
    "/api/i/gallery/posts",
    "/api/i/notifications",
    "/api/i/notifications-grouped",
    "/api/i/page-likes",
    "/api/i/pages",
    "/api/i/pin",
    "/api/i/read-all-unread-notes",
    "/api/i/read-announcement",
    "/api/i/registry/get-all",
    "/api/i/registry/get-detail",
    "/api/i/registry/get",
    "/api/i/registry/keys-with-type",
    "/api/i/registry/keys",
    "/api/i/registry/remove",
    "/api/i/registry/set",
    "/api/i/unpin",
    "/api/i/update",
    "/api/i/webhooks/create",
    "/api/i/webhooks/list",
    "/api/i/webhooks/show",
    "/api/i/webhooks/update",
    "/api/i/webhooks/delete",
    "/api/invite/create",
    "/api/invite/delete",
    "/api/invite/list",
    "/api/invite/limit",
    "/api/meta",
    "/api/emojis",
    "/api/emoji",
    "/api/mute/create",
    "/api/mute/delete",
    "/api/mute/list",
    "/api/renote-mute/create",
    "/api/renote-mute/delete",
    "/api/renote-mute/list",
    "/api/my/apps",
    "/api/notes",
    "/api/notes/children",
    "/api/notes/clips",
    "/api/notes/conversation",
    "/api/notes/create",
    "/api/notes/delete",
    "/api/notes/favorites/create",
    "/api/notes/favorites/delete",
    "/api/notes/featured",
    "/api/notes/global-timeline",
    "/api/notes/hybrid-timeline",
    "/api/notes/local-timeline",
    "/api/notes/mentions",
    "/api/notes/polls/recommendation",
    "/api/notes/polls/vote",
    "/api/notes/reactions",
    "/api/notes/reactions/create",
    "/api/notes/reactions/delete",
    "/api/notes/renotes",
    "/api/notes/replies",
    "/api/notes/search-by-tag",
    "/api/notes/search",
    "/api/notes/show",
    "/api/notes/state",
    "/api/notes/thread-muting/create",
    "/api/notes/thread-muting/delete",
    "/api/notes/timeline",
    "/api/notes/translate",
    "/api/notes/unrenote",
    "/api/notes/user-list-timeline",
    "/api/notifications/create",
    "/api/notifications/mark-all-as-read",
    "/api/notifications/test-notification",
    "/api/pages/create",
    "/api/pages/delete",
    "/api/pages/featured",
    "/api/pages/like",
    "/api/pages/show",
    "/api/pages/unlike",
    "/api/pages/update",
    "/api/flash/create",
    "/api/flash/delete",
    "/api/flash/featured",
    "/api/flash/like",
    "/api/flash/show",
    "/api/flash/unlike",
    "/api/flash/update",
    "/api/flash/my",
    "/api/flash/my-likes",
    "/api/ping",
    "/api/pinned-users",
    "/api/promo/read",
    "/api/roles/list",
    "/api/roles/show",
    "/api/roles/users",
    "/api/roles/notes",
    "/api/request-reset-password",
    "/api/reset-db",
    "/api/reset-password",
    "/api/server-info",
    "/api/stats",
    "/api/sw/show-registration",
    "/api/sw/update-registration",
    "/api/sw/register",
    "/api/sw/unregister",
    "/api/test",
    "/api/username/available",
    "/api/users",
    "/api/users/clips",
    "/api/users/followers",
    "/api/users/following",
    "/api/users/gallery/posts",
    "/api/users/get-frequently-replied-users",
    "/api/users/featured-notes",
    "/api/users/lists/create",
    "/api/users/lists/delete",
    "/api/users/lists/list",
    "/api/users/lists/pull",
    "/api/users/lists/push",
    "/api/users/lists/show",
    "/api/users/lists/favorite",
    "/api/users/lists/unfavorite",
    "/api/users/lists/update",
    "/api/users/lists/create-from-public",
    "/api/users/lists/update-membership",
    "/api/users/lists/get-memberships",
    "/api/users/notes",
    "/api/users/pages",
    "/api/users/flashs",
    "/api/users/reactions",
    "/api/users/recommendation",
    "/api/users/relation",
    "/api/users/report-abuse",
    "/api/users/search-by-username-and-host",
    "/api/users/search",
    "/api/users/show",
    "/api/users/achievements",
    "/api/users/update-memo",
    "/api/fetch-rss",
    "/api/fetch-external-resources",
    "/api/retention",
]
