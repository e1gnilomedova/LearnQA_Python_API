import requests

class TestCookie:
    def test_cookies(self):
        payload = {"login": "secret_login","password":"secret_pass"}
        response = requests.post("https://playground.learnqa.ru/api/homework_cookie", data=payload)
        # print(response.headers)
        assert "Set-Cookie" in response.headers, "There is no cookies in the response"

        #Запуталась, как вынести ключ куки 'HomeWork' и значение ключа куки'hw_value'в переменные, пусть они равны "a" и "b" соответственно.
        # assert len(a) > 0, "Ключ куки пустой"
        # assert len(b) > 0, "Значение ключа куки пустое"

        print(dict(response.cookies))


