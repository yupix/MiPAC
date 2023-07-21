from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generic, Literal, TypeVar

from mipac.models.drive import File
from mipac.models.lite.user import LiteUser
from mipac.types.note import INoteVisibility, IPartialNote
from mipac.utils.format import str_to_datetime

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.note import ClientNoteManager


T = TypeVar('T', bound=IPartialNote)


class PartialNote(Generic[T]):
    def __init__(self, note_data: T, client: ClientManager) -> None:
        self._note: T = note_data
        self._client: ClientManager = client

    @property
    def created_at(self) -> datetime:
        return str_to_datetime(self._note['created_at'])

    @property
    def cw(self) -> str | None:
        return self._note.get('cw')

    @property
    def file_ids(self) -> list[str]:
        return self._note['file_ids']

    @property
    def files(self) -> list[File]:
        return [File(file, client=self._client) for file in self._note['files']]

    @property
    def id(self) -> str:
        """
        ノートのID

        Returns
        -------
        str
            ユーザーのID
        """
        return self._note['id']

    @property
    def reaction_acceptance(self) -> Literal['likeOnly', 'likeOnlyForRemote'] | None:
        """リアクションを受け入れ

        Returns
        -------
        Literal['likeOnly', 'likeOnlyForRemote'] | None
        """
        return self._note.get('reaction_acceptance')

    @property
    def reaction_emojis(self) -> dict[str, str] | None:
        """リアクション一覧です

        Returns
        -------
        dict[str, str] | None
            リアクション名がキー、値はリアクション画像のリンクです
        """
        return self._note.get('reaction_emojis')

    @property
    def renote_id(self) -> str | None:
        return self._note['renote_id']

    @property
    def renote_count(self) -> int:
        return self._note['renote_count']

    @property
    def reactions(self) -> dict[str, int]:
        return self._note['reactions']

    @property
    def replies_count(self) -> int:
        return self._note['replies_count']

    @property
    def reply_id(self) -> str | None:
        return self._note['reply_id']

    @property
    def tags(self) -> list[str]:
        return self._note.get('tags', [])

    @property
    def content(self) -> str | None:
        return self._note.get('text')

    @property
    def author(self) -> LiteUser:
        return LiteUser(self._note['user'], client=self._client)

    @property
    def user_id(self) -> str:
        return self._note['user_id']

    @property
    def visibility(self,) -> INoteVisibility:
        return self._note['visibility']

    @property
    def api(self) -> ClientNoteManager:
        """
        ノートに対するアクション

        Returns
        -------
        NoteActions
        """
        return self._client.note.create_client_note_manager(self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialNote) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
