import allure


@allure.feature("Yandex Disk REST API")
@allure.story("DELETE")
def test_delete_folder(disk_client, created_folder):
    with allure.step("Delete the test folder permanently"):
        response = disk_client.delete_resource(
            created_folder,
            permanently=True,
        )

    with allure.step("Check accepted or completed deletion"):
        assert response.status_code in (202, 204), response.text

    with allure.step("Verify the resource is no longer available"):
        get_response = disk_client.get_resource(created_folder)
        assert get_response.status_code == 404, get_response.text
