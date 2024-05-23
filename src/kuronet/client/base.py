import logging
from types import TracebackType
from typing import AsyncContextManager, Type, Optional, Any, Union

from httpx import AsyncClient, TimeoutException, Response, HTTPError, Timeout

from kuronet.client.cookies import Cookies
from kuronet.client.headers import Headers
from kuronet.errors import (
    TimedOut,
    NetworkError,
    BadRequest,
    raise_for_ret_code,
    NotSupported,
)
from kuronet.utils.enums import Region, Game
from kuronet.utils.types import (
    RT,
    HeaderTypes,
    CookieTypes,
    RequestData,
    QueryParamTypes,
    TimeoutTypes,
    URLTypes,
)

_LOGGER = logging.getLogger("KuroNet.BaseClient")

__all__ = ("BaseClient",)


class BaseClient(AsyncContextManager["BaseClient"]):
    """
    This is the base class for simnet clients. It provides common methods and properties for simnet clients.

    Args:
        cookies (Optional[str, CookieTypes], optional): The cookies used for the client.
        headers (Optional[HeaderTypes], optional): The headers used for the client.
        account_id (Optional[int], optional): The account id used for the client.
        player_id (Optional[int], optional): The player id used for the client.
        region (Region, optional): The region used for the client.
        lang (str, optional): The language used for the client.
        timeout (Optional[TimeoutTypes], optional): Timeout configuration for the client.

    Attributes:
        headers (HeaderTypes): The headers used for the client.
        account_id (Optional[int]): The account id used for the client.
        player_id (Optional[int]): The player id used for the client.
        region (Region): The region used for the client.
        lang (str): The language used for the client.
        game (Optional[Game]): The game used for the client.

    """

    game: Optional[Game] = None

    def __init__(
        self,
        cookies: Optional[Union[str, CookieTypes]] = None,
        headers: Optional[HeaderTypes] = None,
        user_token: Optional[str] = None,
        account_id: Optional[int] = None,
        player_id: Optional[int] = None,
        region: Region = Region.OVERSEAS,
        lang: str = "en-us",
        timeout: Optional[TimeoutTypes] = None,
    ) -> None:
        """Initialize the client with the given parameters."""
        if timeout is None:
            timeout = Timeout(
                connect=5.0,
                read=5.0,
                write=5.0,
                pool=1.0,
            )
        cookies = Cookies(cookies)
        self.headers = Headers(headers)
        self.player_id = player_id
        self.account_id = account_id or cookies.account_id
        self.user_token = user_token or cookies.user_token
        self.client = AsyncClient(cookies=cookies, timeout=timeout)
        self.region = region
        self.lang = lang

    @property
    def cookies(self) -> Cookies:
        """Get the cookies used for the client."""
        return Cookies(self.client.cookies.jar)

    @cookies.setter
    def cookies(self, cookies: CookieTypes) -> None:
        self.client.cookies = cookies

    @property
    def device_name(self) -> str:
        """Get the device name used for the client."""
        return "KuroNet Build 114514"

    @property
    def app_version(self) -> str:
        """Get the app version used for the client."""
        if self.region == Region.CHINESE:
            return "2.2.0"
        if self.region == Region.OVERSEAS:
            return "1.5.0"
        return "null"

    @property
    def user_agent(self) -> str:
        """Get the user agent used for the client."""
        if self.region == Region.CHINESE:
            return (
                f"Mozilla/5.0 (Linux; {self.device_name}) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36"
            )
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Safari/537.36"
        )

    async def __aenter__(self: RT) -> RT:
        """Enter the async context manager and initialize the client."""
        try:
            await self.initialize()
            return self
        except Exception as exc:
            await self.shutdown()
            raise exc

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit the async context manager and shutdown the client."""
        await self.shutdown()

    async def shutdown(self):
        """Shutdown the client."""
        if self.client.is_closed:
            _LOGGER.info("This Client is already shut down. Returning.")
            return

        await self.client.aclose()

    async def initialize(self):
        """Initialize the client."""

    def get_lab_api_header(
        self,
        headers: HeaderTypes,
        lang: Optional[str] = None,
    ):
        """Get the lab API header for API requests.

        Args:
            headers (HeaderTypes): The header to use.
            lang (Optional[str], optional): The language to use for overseas regions. Defaults to None.
        Returns:
            Headers: The lab API header with added fields.
        """
        headers = Headers(headers)
        headers["user-agent"] = self.user_agent
        if self.region == Region.OVERSEAS:
            if lang:
                headers["lang"] = lang
        if self.user_token:
            headers["token"] = self.user_token
        headers["devCode"] = "D006C4D753D3D0049DF4339D3562C11A6676CDDB"
        headers["source"] = "android"
        headers["version"] = self.app_version
        headers["versionCode"] = self.app_version.replace(".", "") + "0"
        headers["osVersion"] = "Android"
        headers["distinct_id"] = "ac442a9e-0085-4fd3-8a31-583275dfdc35"
        headers["countryCode"] = "CN"
        return headers

    async def request(
        self,
        method: str,
        url: URLTypes,
        data: Optional[RequestData] = None,
        json: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ) -> Response:
        """Make an HTTP request and return the response.

        This method makes an HTTP request with the specified HTTP method, URL, request parameters, headers,
        and JSON payload. It catches common HTTP errors and raises a `NetworkError` or `TimedOut` exception
        if the request times out.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            data (Optional[RequestData]): The request data to include in the body of the request.
            json (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Response: A `Response` object representing the HTTP response.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.

        """
        try:
            return await self.client.request(
                method,
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
            )
        except TimeoutException as exc:
            raise TimedOut from exc
        except HTTPError as exc:
            raise NetworkError from exc

    async def request_api(
        self,
        method: str,
        url: URLTypes,
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
    ):
        """Make an API request and return the data.

        This method makes an API request using the `request()` method
        and returns the data from the response if it is successful.
        If the response contains an error, it raises a `BadRequest` exception.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            data (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Any: The data returned by the API.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        response = await self.request(
            method,
            url,
            data=data,
            params=params,
            headers=headers,
        )
        if not response.is_error:
            data = response.json()
            ret_code = data.get("code", 0)
            if ret_code != 200:
                raise_for_ret_code(data)
            return data["data"]
        if response.status_code == 404:
            raise NotSupported("API not supported or has been removed.")
        raise BadRequest(status_code=response.status_code, message=response.text)

    async def request_lab(
        self,
        url: URLTypes,
        method: Optional[str] = None,
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        headers: Optional[HeaderTypes] = None,
        lang: Optional[str] = None,
    ):
        """Make a request to the lab API and return the data.

        This method makes a request to the lab API using the `request_api()` method
        and returns the data from the response if it is successful.
        It also adds headers for the lab API and handles the case where the method is not specified.

        Args:
            url (URLTypes): The URL to send the request to.
            method (Optional[str]): The HTTP method to use for the request (e.g., "GET", "POST").
            data (Optional[Any]): The JSON payload to include in the body of the request.
            params (Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (Optional[HeaderTypes]): The headers to include in the request.
            lang (Optional[str]): The language of the request (e.g., "en", "zh").

        Returns:
            Any: The data returned by the lab API.

        """
        if method is None:
            method = "POST" if data else "GET"
        headers = self.get_lab_api_header(headers, lang=lang)
        return await self.request_api(
            method=method, url=url, data=data, params=params, headers=headers
        )
