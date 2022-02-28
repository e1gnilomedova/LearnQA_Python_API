# import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime
import allure
TEST_CASE_LINK = 'https://jira.test.ru/browse/TESTCASE-1'

@allure.epic("Home work")
@allure.feature("lesson4_Ex16")
class TestUserRegister(BaseCase):

#Создаем нового юзера, чтобы получить его id
    @allure.story("Получение данных первого юзера с авторизацией из-под чужого")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase(TEST_CASE_LINK, 'Link TESTCASE in Jira')
    def test_get_user_details_of_another_user(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id_from_register_user = self.get_json_value(response, "id")


#Авторизовываемся вторым пользователем, чтобы получить его куки и токен
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

#Отправляем id первого юзера и куки, токен от второго
        response2 = MyRequests.get(
            f"/user/{user_id_from_register_user}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_has_key(response2, "username")
        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, expected_fields)
        Assertions.assert_code_status(response2, 401)