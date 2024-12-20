import requests

import json


# Ваш токен

token = '452cc499-268d-4d8f-9948-fcaa0aba839d'

# URL сервера

server_url = 'https://games-test.datsteam.dev/play/snake3d'


# API-метод

api = '/player/move'

url = f"{server_url}{api}"


# Данные для отправки

data = {

    'snakes': []

}


# Заголовки запроса

headers = {

    'X-Auth-Token': token,

    'Content-Type': 'application/json'

}


# Выполнение POST-запроса

response = requests.post(url, headers=headers, json=data)


# Сохранение ответа в файл

with open('example_response.json', 'w') as file:

    file.write(response.text)