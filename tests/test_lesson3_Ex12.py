# import requests
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
import allure

@allure.epic("Home work")
@allure.feature("lesson3_Ex12")
class TestHeaders(BaseCase):
    @allure.story("Найти определенный header в ответе, заассертить")
    def test_headers(self):
        payload = {"login": "secret_login", "password": "secret_pass"}
        response = MyRequests.post("/homework_header", data=payload)
        headers = self.get_header(response, "x-secret-homework-header")
        print('x-secret-homework-header')
        print(headers)