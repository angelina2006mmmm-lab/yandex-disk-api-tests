import allure


@allure.feature("Yandex Disk REST API")
@allure.story("GET")
def test_get_disk_info(disk_client):
    with allure.step("Request disk information"):
        response = disk_client.get_disk_info()

    with allure.step("Check HTTP status and basic response fields"):
        assert response.status_code == 200, response.text
        body = response.json()
        assert "total_space" in body
        assert "used_space" in body
        assert isinstance(body["total_space"], int)
        assert isinstance(body["used_space"], int)


@allure.feature("Yandex Disk REST API")
@allure.story("GET")
def test_get_existing_folder(disk_client, created_folder):
    with allure.step("Request metadata for an existing folder"):
        response = disk_client.get_resource(created_folder)

    with allure.step("Check returned folder metadata"):
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["name"] == created_folder
        assert body["type"] == "dir"


@allure.feature("Yandex Disk REST API")
@allure.story("GET negative")
def test_get_missing_resource_returns_404(disk_client, unique_path):
    response = disk_client.get_resource(f"{unique_path}_missing")

    assert response.status_code == 404, response.text
    body = response.json()
    assert "error" in body
