from http.cookiejar import CookieJar
from http.cookies import SimpleCookie
from typing import Optional, TypeVar

from httpx import Cookies as _Cookies

from kuronet.utils.types import CookieTypes

from pydantic import BaseModel

IntStr = TypeVar("IntStr", int, str)

__all__ = (
    "Cookies",
    "CookiesModel",
)


class Cookies(_Cookies):
    """A wrapper around `httpx.Cookies` that provides additional functionality."""

    jar: CookieJar

    def __init__(self, cookies: Optional[CookieTypes] = None):  # skipcq: PYL-W0231
        self.jar = CookieJar()
        if cookies is None or isinstance(cookies, dict):
            if isinstance(cookies, dict):
                for key, value in cookies.items():
                    if isinstance(value, str):
                        self.set(key, value)
                    else:
                        self.set(key, str(value))
        elif isinstance(cookies, list):
            for key, value in cookies:
                self.set(key, value)
        elif isinstance(cookies, Cookies):
            for cookie in cookies.jar:
                self.jar.set_cookie(cookie)
        elif isinstance(cookies, str):
            cookie = SimpleCookie(cookies)
            for key, value in cookie.items():
                self.set(key, value.value)
        else:
            self.jar = cookies  # type: ignore

    COOKIE_USER_ID_NAMES = ["account_id"]

    @property
    def account_id(self) -> Optional[int]:
        """Return the user account ID if present in the cookies.

        If one of the user ID cookies exists in the cookies, return its integer value.
        Otherwise, return `None`.

        Returns:
            Optional[int]: The user account ID, or `None` if it is not present in the cookies.
        """
        for name in self.COOKIE_USER_ID_NAMES:
            user_id = self.get(name)
            if user_id:
                return int(user_id)
        return None

    @property
    def user_token(self) -> Optional[str]:
        """Return the user token if present in the cookies.

        Returns:
            Optional[str]: The user token, or `None` if it is not present in the cookies.
        """
        return self.get("user_token")

    @property
    def platform(self) -> Optional[str]:
        """Return the platform if present in the cookies.

        Returns:
            Optional[str]: The platform, or `None` if it is not present in the cookies.
        """
        return self.get("platform")

    def get(
        self,
        name: str,
        default: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get a cookie by name. May optionally include domain and path
        in order to specify exactly which cookie to retrieve.
        """
        value = None
        for cookie in self.jar:
            if (
                cookie.name == name
                and domain is None
                or cookie.domain == domain
                and path is None
                or cookie.path == path
                and cookie.value
            ):
                value = cookie.value
        if value is None:
            return default
        return value


class CookiesModel(BaseModel, frozen=False):
    """A model that represents the cookies used by the client."""

    account_id: Optional[IntStr] = None
    user_token: Optional[str] = None

    def to_dict(self):
        """Return the cookies as a dictionary."""
        return self.dict(exclude_defaults=True)

    def to_json(self):
        """Return the cookies as a JSON string."""
        return self.json(exclude_defaults=True)

    @property
    def user_id(self) -> Optional[int]:
        if self.account_id:
            return self.account_id
        return None

    def set_uid(self, user_id: int):
        """Set the user ID for the cookies."""
        if self.account_id is None and self.user_token:
            self.account_id = user_id
