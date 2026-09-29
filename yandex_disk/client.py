from __future__ import annotations

from typing import Any

import requests


class YandexDiskClient:
    """Small HTTP client for Yandex Disk REST API."""

    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, token: str, timeout: float = 15.0) -> None:
        if not token:
            raise ValueError("OAuth token must not be empty")

        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"OAuth {token}",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str = "",
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = f"{self.BASE_URL}{endpoint}"
        return self.session.request(
            method=method,
            url=url,
            params=params,
            timeout=self.timeout,
        )

    # GET
    def get_disk_info(self) -> requests.Response:
        return self._request("GET")

    def get_resource(self, path: str) -> requests.Response:
        return self._request(
            "GET",
            "/resources",
            params={"path": path},
        )

    # PUT
    def create_folder(self, path: str) -> requests.Response:
        return self._request(
            "PUT",
            "/resources",
            params={"path": path},
        )

    # POST
    def copy_resource(
        self,
        source_path: str,
        destination_path: str,
        *,
        overwrite: bool = False,
    ) -> requests.Response:
        return self._request(
            "POST",
            "/resources/copy",
            params={
                "from": source_path,
                "path": destination_path,
                "overwrite": str(overwrite).lower(),
            },
        )

    # DELETE
    def delete_resource(
        self,
        path: str,
        *,
        permanently: bool = True,
    ) -> requests.Response:
        return self._request(
            "DELETE",
            "/resources",
            params={
                "path": path,
                "permanently": str(permanently).lower(),
            },
        )

    def close(self) -> None:
        self.session.close()
