# import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def setup(self):
#Регистрируем нового пользователя1.
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email1 = register_data['email']
        # self.first_name1 = register_data['firstName']
        password1 = register_data['password']
        self.user_id1 = self.get_json_value(response, "id")


        login_data1 = {
            'email': email1,
            'password': password1
        }
        response1 = MyRequests.post("/user/login", data=login_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "user_id")

        self.auth_sid1 = self.get_cookie(response1, "auth_sid")
        self.token1 = self.get_header(response1, "x-csrf-token")

#Существующий пользователь. Это будет пользователь2.
        login_data2 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequests.post("/user/login", data=login_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "user_id")

        self.auth_sid2 = self.get_cookie(response2, "auth_sid")
        self.token2 = self.get_header(response2, "x-csrf-token")
        self.user_id2 = self.get_json_value(response2, "user_id")

    def test_1(self):
#1. Первый - на попытку удалить пользователя по ID 2.
        response3 = MyRequests.delete(
            f"/user/{self.user_id2}",
            headers={"x-csrf-token": self.token2},
            cookies={"auth_sid": self.auth_sid2}
        )

# Убедиться, что система не даст вам удалить этого пользователя.
        Assertions.assert_code_status(response3, 400)

        response4 = MyRequests.get(
            f"/user/{self.user_id2}",
            headers={"x-csrf-token": self.token2},
            cookies={"auth_sid": self.auth_sid2}
        )

        Assertions.assert_code_status(response4, 200)
        id = int(self.get_json_value(response4, "id"))
        assert id == self.user_id2, "Пользователь удалился, хотя не должен был"


    def test_2(self):
#2. Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID
# и убедиться, что пользователь действительно удален.

        response5 = MyRequests.delete(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1}
        )
        Assertions.assert_code_status(response5, 200)

        response6 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1}
        )
        Assertions.assert_code_status(response6, 404)
        Assertions.assert_response_content(response6, f"User not found")

    def test_3(self):
#3. Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
        response7 = MyRequests.delete(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token2},
            cookies={"auth_sid": self.auth_sid2}
        )

        Assertions.assert_code_status(response7, 400)

        response8 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1}
        )
        Assertions.assert_code_status(response8, 200)
        Assertions.assert_json_has_key(response8, "id")
        Assertions.assert_json_value_by_name(
            response8,
            "id",
            self.user_id1,
            "Id пользователя изменился"
        )