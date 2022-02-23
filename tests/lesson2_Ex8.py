import requests
from lib.assertions import Assertions
import time

class TestToken:

    def test_get_token(self):
#1) создавал задачу
        response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

        # print(f" response: {response.status_code}")
        # print(f" response: {response.text}")

        Assertions.assert_code_status(response, 200)

        Assertions.assert_json_has_key(response, "token")
        response_dict = response.json()
        token = response_dict["token"]

        # print(f" значение токена равно '{token}'")

        Assertions.assert_json_has_key(response, "seconds")
        t = response_dict["seconds"]

# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
        payload = {"token": token}
        response1 = requests.post("https://playground.learnqa.ru/ajax/api/longtime_job", data=payload)

        # print(f" response1: {response1.status_code}")
        # print(f" response1: {response1.text}")

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "status")

        response_dict1 = response1.json()
        status = response_dict1["status"]


        if status == f"Job is NOT ready":
                # 3) ждал нужное количество секунд с помощью функции time.sleep()
                time.sleep(t)

                # 4) делал бы один запрос c token ПОСЛЕ того, как задача готова,
                # убеждался в правильности поля status и наличии поля result
                response2 = requests.post("https://playground.learnqa.ru/ajax/api/longtime_job", data=payload)

                # print(f" response2: {response2.status_code}")
                # print(f" response2: {response2.text}")

                Assertions.assert_code_status(response2, 200)

                new_name = "Job is ready"
                Assertions.assert_json_value_by_name(
                        response2,
                        "status",
                        new_name,
                        "Задача не готова, нужно разбираться"
                )
                Assertions.assert_json_has_key(response2, "result")
                response_dict2 = response2.json()
                result2 = response_dict2["result"]
                print(f"Значение результата равно '{result2}'")

        else:
                print(f"Статус равен '{status}'")
                Assertions.assert_json_has_key(response1, "result")
                result = response_dict1["result"]
                print(f"Значение результата равно '{result}'")