import requests
import pytest

class Test1234:

    http_methods = [
        ("GET"),
        ("POST"),
        ("PUT"),
        ("DELETE")
    ]

    def setup(self):
        self.url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

    def test_123(self):
#1 Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
        http_types = ['GET', 'POST', 'PUT', 'DELETE']
        for http_type in http_types:
            response = requests.request(http_type, self.url)
            print(response)
            print(response.status_code)
            print(response.text)
            print()
        print('конец задания 1')
        print()

#2 Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
        response = requests.request('HEAD', self.url)
        print(response)
        print(response.status_code)
        print(response.text)

        print('конец задания 2')
        print()


#3 Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
        method = {"method": "GET"}
        response = requests.get(self.url, params=method)
        print(response)
        print(response.status_code)
        print(response.text)
        print()

        method = {"method": "POST"}
        response = requests.post(self.url, data=method)
        print(response)
        print(response.status_code)
        print(response.text)
        print()

        method = {"method": "PUT"}
        response = requests.put(self.url, data=method)
        print(response)
        print(response.status_code)
        print(response.text)
        print()

        method = {"method": "DELETE"}
        response = requests.delete(self.url, data=method)
        print(response)
        print(response.status_code)
        print(response.text)
        print('конец задания 3')

#4 С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для всех типов запроса.
# Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.


    @pytest.mark.parametrize('request_http_method', http_methods)
    @pytest.mark.parametrize('param_http_method', http_methods)
    def test_4(self, request_http_method, param_http_method):

        if request_http_method == "GET":
            params = {"method": param_http_method}
            response = requests.get(self.url, params=params)
        else:
            data = {"method": param_http_method}
            response = requests.request(request_http_method, self.url, data=data)


        if request_http_method != param_http_method and (response.status_code == 200 or "success" in response.json()):
            print(f"Условие1: Тип запроса '{request_http_method}' НЕ равен значению method '{param_http_method}', "
                  f"но сервер считает, что это так.")

        if request_http_method == param_http_method and (response.status_code != 200 or response.text == f"Wrong method provided"):
            print(f" Условие2: Тип запроса '{request_http_method}' равен значению method '{param_http_method}',"
                  f"но сервер считает, что это не так.")
        assert True