from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import allure

@allure.epic("Examples from videos")
@allure.feature("Registration cases")
class TestUserRegister(BaseCase):

    @allure.story("This test successfully create user with new generate correct email")
    @allure.description("This test successfully create user with new generate correct email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        # print(response.content)
        # print(response.status_code)

    @allure.story("This test try create user with existing email")
    @allure.description("This test try create user with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == \
               f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"