import requests

class TestHeaders:
    def test_headers(self):
        payload = {"login": "secret_login","password":"secret_pass"}
        response = requests.post("https://playground.learnqa.ru/api/homework_header", data=payload)
        headers = response.headers
        # print(response.headers)
        # По какому признаку тесту объяснить, что в этом задании нужно работать именно с этим header, чтобы не указывать ключ заголовка ?
        # Сейчас этот header я сама определила из print(response.headers), как подозрительный:)
        assert "x-secret-homework-header" in response.headers, "There is no 'x-secret-homework-header' in the response"

        # Помогите, пожалуйста, с синтаксисом в 14 и 15 строках. Планировала проверять количество символов в значении ключа заголовка.
        # key = ["x-secret-homework-header"]
        # assert len(key) > 0, "Значение ключа заголовка ответа пустое"
        print(response.headers["x-secret-homework-header"])