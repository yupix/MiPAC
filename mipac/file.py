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
        path: str | None = None,
        file_id: str | None = None,
        name: str | None = None,
        folder_id: str | None = None,
        comment: str | None = None,
        is_sensitive: bool = False,
        force: bool = False,
    ):
        """
        Parameters
        ----------
        path : str | None, default=None
            path to a local file
        file_id : str | None, default=None
            ID of the file that exists on the drive
        name str | None, default=None
            file name
        folder_id : str | None, default=None
            Folder ID
        comment : str | None, default=None
            Comments on files
        is_sensitive : str | None, default=None
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
