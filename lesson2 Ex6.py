import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
last = response.history[-1]
last_url = last.url
print(f"Конечный url: {last_url}")

all_url = response.history
print(all_url)
sum = len(all_url)
print(f"Количество редиректов: {sum}")