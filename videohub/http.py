import asyncio
from typing import Optional

import httpx

from .constants import API_BASE, SDK_NAME, SDK_VERSION
from .exceptions import APIRequestError
from .utils.validators import RequestValidator


class HTTPClient:


    def __init__(self, config):
        self.config = config
        self.validator = RequestValidator(config)

        self._client: Optional[httpx.AsyncClient] = None
        self._loop = None

    def _get_client(self):

        current_loop = asyncio.get_running_loop()

        if self._client is None or self._loop != current_loop:

            limits = httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            )

            self._client = httpx.AsyncClient(
                base_url=API_BASE,
                timeout=self.config.timeout,
                limits=limits
            )

            self._loop = current_loop

        return self._client
    

    def _build_headers(self, auth_required: bool, is_json: bool = True):

        headers = {
            "User-Agent": f"{SDK_NAME}/{SDK_VERSION}",
            "X-SDK-Version": SDK_VERSION,
        }

        if is_json:
            headers["Content-Type"] = "application/json"

        if auth_required:
            headers.update(
                self.validator.build_headers()
            )

        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ):

        retries = 3
        response = None

        client = self._get_client()

        for attempt in range(retries):

            try:

                response = await client.request(
                    method,
                    endpoint,
                    **kwargs
                )

                if response.status_code < 500:
                    break

            except httpx.RequestError as e:

                if attempt == retries - 1:
                    raise APIRequestError(
                        f"Network error: {str(e)}"
                    )

                await asyncio.sleep(
                    2 ** attempt * 0.2
                )

        if response is None:
            raise APIRequestError(
                "No response from server"
            )

        if response.status_code >= 400:

            try:

                error = response.json()

                message = (
                    error.get("error")
                    or error.get("message")
                    or str(error)
                )

                raise APIRequestError(message)

            except Exception:

                raise APIRequestError(
                    response.text
                )

        try:
            return response.json()

        except Exception:
            return response.text

    async def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        auth_required: bool = True,
        headers=None,
        files=None,
        data=None
    ):

        if files or data:

            request_headers = self._build_headers(
                auth_required,
                is_json=False
            )

            if headers:
                request_headers.update(headers)

            return await self._request(
                "POST",
                endpoint,
                files=files,
                data=data,
                headers=request_headers
            )

        request_headers = self._build_headers(
            auth_required,
            is_json=True
        )

        if headers:
            request_headers.update(headers)

        return await self._request(
            "POST",
            endpoint,
            json=payload,
            headers=request_headers
        )

    async def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        auth_required: bool = True,
        raw: bool = False
    ):

        headers = self._build_headers(
            auth_required
        )

        response = await self._request(
            "GET",
            endpoint,
            params=params,
            headers=headers
        )

        if raw:
            return response

        return response

    async def upload(
        self,
        endpoint: str,
        files,
        data=None,
        headers=None,
        auth_required: bool = False
    ):

        request_headers = {
            "User-Agent": f"{SDK_NAME}/{SDK_VERSION}",
            "X-SDK-Version": SDK_VERSION,
        }

        if auth_required:
            request_headers.update(
                self.validator.build_headers()
            )

        if headers:
            request_headers.update(headers)

        request_headers.pop(
            "Content-Type",
            None
        )

        client = self._get_client()

        response = await client.post(
            endpoint,
            files=files,
            data=data,
            headers=request_headers,
            timeout=None
        )

        if response.status_code >= 400:

            try:

                err = response.json()

                raise APIRequestError(
                    err.get(
                        "error",
                        str(err)
                    )
                )

            except Exception:

                raise APIRequestError(
                    response.text
                )

        return response.json()

    async def close(self):

        if self._client:

            await self._client.aclose()

            self._client = None
            self._loop = None

