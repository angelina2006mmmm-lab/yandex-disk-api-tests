import allure

from tests.conftest import cleanup_resource


@allure.feature("Yandex Disk REST API")
@allure.story("POST")
def test_copy_folder(disk_client, created_folder, unique_path):
    destination = f"{unique_path}_copy"

    try:
        with allure.step("Copy an existing folder"):
            response = disk_client.copy_resource(
                created_folder,
                destination,
                overwrite=False,
            )

        with allure.step("Check accepted or completed copy request"):
            assert response.status_code in (201, 202), response.text

        with allure.step("Verify copied folder if the operation completed synchronously"):
            if response.status_code == 201:
                get_response = disk_client.get_resource(destination)
                assert get_response.status_code == 200, get_response.text
                assert get_response.json()["type"] == "dir"
    finally:
        cleanup_resource(disk_client, destination)
