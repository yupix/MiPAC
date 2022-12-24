class Config:
    def __init__(
        self, is_ayuskey: bool = False, is_official: bool = False
    ) -> None:
        self.is_ayuskey: bool = is_ayuskey
        self.is_official: bool = is_official
