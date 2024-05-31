from mipac.types.app import IApp


class App:
    def __init__(self, raw_app: IApp) -> None:
        self.__raw_app: IApp = raw_app

    @property
    def id(self) -> str:
        """The id of the app"""
        return self.__raw_app["id"]

    @property
    def name(self) -> str:
        """The name of the app"""
        return self.__raw_app["name"]

    @property
    def callback_url(self) -> str | None:
        """The callback url of the app"""
        return self.__raw_app["callback_url"]

    @property
    def permission(self) -> list[str]:
        """The permissions the app has"""
        return self.__raw_app["permission"]

    @property
    def secret(self) -> str:
        """The secret of the app"""
        return self.__raw_app["secret"]

    @property
    def is_authorized(self) -> bool:
        """If the app is authorized or not"""
        return self.__raw_app["is_authorized"]
