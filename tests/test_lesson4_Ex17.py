# import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import allure


@allure.epic("Home work")
@allure.feature("lesson4_Ex17")
class TestUserEditExample17(BaseCase):
    def setup(self):

# Регистрируем нового пользователя, ему будем изменять данные. Это пользователь1.
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data['email']
        # self.first_name1 = register_data['firstName']
        password1 = register_data['password']
        self.user_id1 = self.get_json_value(response1, "id")

# Логинимся под пользователем1, запрашиваем его данные для дальнейших проверок.
        self.login_data1 = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=self.login_data1)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "user_id")

        self.auth_sid1 = self.get_cookie(response3, "auth_sid")
        self.token1 = self.get_header(response3, "x-csrf-token")

    @allure.story("1. Попытаемся изменить данные пользователя, будучи неавторизованными")
    def test_1(self):
# 1. Попытаемся изменить данные пользователя, будучи неавторизованными

# Меняем данные пользователю1 из-под неавторизованного
        new_name = "Changed_Name"
        new_lastname = "Changed_LastName"

        response2 = MyRequests.put(
            f"/user/{self.user_id1}",
            data={"firstName": new_name, "lastName": new_lastname}
        )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, f"Auth token not supplied")

# Логинимся под пользователем1, запрашиваем его данные, чтобы проверить, точно ли они не изменились.
        response4 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1}
        )
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name_is_not_changed(
            response4,
            "firstName",
            new_name,
            "This is bad. An unauthorized user can edit 'firstName'"
        )
        Assertions.assert_json_value_by_name_is_not_changed(
            response4,
            "lastName",
            new_lastname,
            "This is bad. An unauthorized user can edit 'lastName'"
        )

    @allure.story("2. Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем")
    def test_2(self):
# 2. Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем

# Логинимся под вторым пользователем, получаем его куки и токен. Это пользователь2. Под ним будем менять данные пользователя1
        login_data2 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response5 = MyRequests.post("/user/login", data=login_data2)

        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "user_id")

        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

#  Из-под пользователя2 меняем данные пользователя1.
        new_name = "Changed_Name"
        new_lastname = "Changed_LastName"
        response6 = MyRequests.put(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
            data={"firstName": new_name, "lastName": new_lastname}
        )
        Assertions.assert_code_status(response6, 400)

# Проверяем, что данные пользователя1 не изменены
        response7 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1}
        )

        Assertions.assert_json_value_by_name_is_not_changed(
            response7,
            "firstName",
            new_name,
            "This is bad. An unauthorized user can edit"
        )
        Assertions.assert_json_value_by_name_is_not_changed(
            response7,
            "lastName",
            new_lastname,
            "This is bad. An unauthorized user can edit 'lastName'"
        )

    @allure.story("3. Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @")
    def test_3(self):
# 3. Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @

        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_email = f"{base_part}{random_part}{domain}"

        response8 = MyRequests.put(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response8, 400)
        Assertions.assert_response_content(response8, f"Invalid email format")

        response9 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1},
        )
        Assertions.assert_code_status(response9, 200)
        Assertions.assert_json_value_by_name_is_not_changed(
            response9,
            "email",
            new_email,
            "This is bad. Email is changed by incorrect email'"
        )

    @allure.story("4. Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ")
    def test_4(self):
# 4. Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
        short_name = "j"
        response10 = MyRequests.put(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1},
            data={"firstName": short_name}
        )
        Assertions.assert_code_status(response10, 400)
        Assertions.assert_json_value_by_name(
            response10,
            "error",
            f"Too short value for field firstName",
            "User is created with short 'firstName'"
        )

        response11 = MyRequests.get(
            f"/user/{self.user_id1}",
            headers={"x-csrf-token": self.token1},
            cookies={"auth_sid": self.auth_sid1},
        )
        Assertions.assert_code_status(response11, 200)
        Assertions.assert_json_value_by_name_is_not_changed(
            response11,
            "firstName",
            short_name,
            "Confirmed. User is created with short 'firstName'.This is bad."
        )
