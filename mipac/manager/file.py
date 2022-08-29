from typing import Optional


class MiFile:
    __slots__ = (
        'path',
        'file_id',
        'name',
        'folder_id',
        'comment',
        'is_sensitive',
        'force',
    )

    def __init__(
        self,
        path: Optional[str] = None,
        file_id: Optional[str] = None,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
        comment: Optional[str] = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        """
        Parameters
        ----------
        path : Optional[str], default=None
            path to a local file
        file_id : Optional[str], default=None
            ID of the file that exists on the drive
        name Optional[str], default=None
            file name
        folder_id : Optional[str], default=None
            Folder ID
        comment : Optional[str], default=None
            Comments on files
        is_sensitive : Optional[str], default=None
            Whether this item is sensitive
        force : bool, default=False
            Whether to force overwriting even if it already exists on the drive
        """
        self.path = path
        self.file_id = file_id
        self.name = name
        self.folder_id = folder_id
        self.comment = comment
        self.is_sensitive = is_sensitive
        self.force = force
