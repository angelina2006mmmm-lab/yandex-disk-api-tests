import allure

from tests.conftest import cleanup_resource


@allure.feature("Yandex Disk REST API")
@allure.story("PUT")
def test_create_folder(disk_client, unique_path):
    try:
        with allure.step("Create a new folder"):
            response = disk_client.create_folder(unique_path)

        with allure.step("Check successful creation"):
            assert response.status_code == 201, response.text

        with allure.step("Verify the folder is available through GET"):
            get_response = disk_client.get_resource(unique_path)
            assert get_response.status_code == 200, get_response.text
            assert get_response.json()["type"] == "dir"
    finally:
        cleanup_resource(disk_client, unique_path)


@allure.feature("Yandex Disk REST API")
@allure.story("PUT negative")
def test_create_existing_folder_returns_409(disk_client, created_folder):
    response = disk_client.create_folder(created_folder)

    assert response.status_code == 409, response.text
    body = response.json()
    assert "error" in body
