from __future__ import annotations

import os
import uuid

import pytest
from dotenv import load_dotenv

from yandex_disk import YandexDiskClient


load_dotenv()


@pytest.fixture(scope="session")
def disk_client() -> YandexDiskClient:
    """
    Create an API client from YANDEX_DISK_TOKEN.

    Integration tests are skipped when the token is not configured, so the
    project can still be collected locally without exposing credentials.
    """
    token = os.getenv("YANDEX_DISK_TOKEN", "").strip()

    if not token:
        pytest.skip(
            "YANDEX_DISK_TOKEN is not configured. "
            "Copy .env.example to .env and add a token for a separate test account."
        )

    client = YandexDiskClient(token)
    yield client
    client.close()


@pytest.fixture
def unique_path() -> str:
    return f"qa_autotest_{uuid.uuid4().hex[:12]}"


def cleanup_resource(client: YandexDiskClient, path: str) -> None:
    """
    Best-effort cleanup.

    404 is acceptable because the resource may already be absent.
    """
    response = client.delete_resource(path, permanently=True)
    assert response.status_code in (202, 204, 404), (
        f"Cleanup failed for {path!r}: "
        f"{response.status_code} {response.text}"
    )


@pytest.fixture
def created_folder(disk_client: YandexDiskClient, unique_path: str):
    response = disk_client.create_folder(unique_path)
    assert response.status_code == 201, (
        f"Could not create test folder: "
        f"{response.status_code} {response.text}"
    )

    yield unique_path

    cleanup_resource(disk_client, unique_path)
