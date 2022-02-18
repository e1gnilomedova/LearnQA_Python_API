import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest

class TestUserRegister(BaseCase):

    def setup(self):
        self.url = "https://playground.learnqa.ru/api/user/"

# ДЗ 15.1
    def test_create_user_email_incorrect(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email_incorrect = f"{base_part}{random_part}{domain}"
        data = {
             'password': '123',
             'username': 'learnqa',
             'firstName': 'learnqa',
             'lastName': 'learnqa',
             'email': email_incorrect
         }
        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"Invalid email format")

# ДЗ 15.2
    base_part = "learnqa"
    domain = "example.com"
    random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    email = f"{base_part}{random_part}@{domain}"
    arg_names = 'password, username, firstName, lastName, email'
    arg_values = [
        (
            None,
            "learnqa",
            "learnqa",
            "learnqa",
            email
        ),
        (
            "123",
            None,
            "learnqa",
            "learnqa",
            email
        ),
        (
            "123",
            "learnqa",
            None,
            "learnqa",
            email
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            None,
            email
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            "learnqa",
            None
        )
    ]
    @pytest.mark.parametrize(arg_names, arg_values)
    def test_create_user_without_required_parameters(self, password, username, firstName, lastName, email):
        data = {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email
        }
        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)

        decode_content = response.content.decode("utf-8")
        decode_content_parts = decode_content.split(": ")
        assert decode_content_parts[0] == 'The following required params are missed', \
            f"Response.content is incorrected for this test"
        # print(response.content)


# ДЗ 15.3
    def test_create_user_short_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
             'password': '123',
             'username': 'learnqa',
             'firstName': 'h',
             'lastName': 'learnqa',
             'email': email
         }
        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"The value of 'firstName' field is too short")


# ДЗ 15.4
    def test_create_user_long_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
             'password': '123',
             'username': 'learnqa',
             'firstName': 'ИмяРавное260СимволамОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмяОченьДлиннноеИмя',
             'lastName': 'learnqa',
             'email': email
         }
        response = requests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"The value of 'firstName' field is too long")