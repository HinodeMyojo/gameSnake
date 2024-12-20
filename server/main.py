import requests
import json
import time
import pathfinder as ph
token = '452cc499-268d-4d8f-9948-fcaa0aba839d'
server_url = 'https://games-test.datsteam.dev/play/snake3d'

api = '/player/move'

url = f"{server_url}{api}"

data = {
    'snakes': [
        
    ]
}

# Заголовки запроса
headers = {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
}

def move(snake_id, direction):
    data = {
        "snakes": [
            {
                "id": snake_id,
                "direction": direction
            }
        ]
    }
    response = requests.post(f"{server_url}/player/move", headers=headers, json=data)
    return response.json()

def get_direction(head, target):
    if head[0] != target[0]: 
        return [1, 0, 0] if head[0] < target[0] else [-1, 0, 0]

    if head[1] != target[1]:
        return [0, 1, 0] if head[1] < target[1] else [0, -1, 0]

    if head[2] != target[2]: 
        return [0, 0, 1] if head[2] < target[2] else [0, 0, -1]

def get_game_state():
    """Получить состояние карты."""
    #response = requests.post(url, headers=headers, json=data)
    f = open("example_response copy.json", "r")
    response = f.read()
    return json.loads(response)

def main():

    while True:

        state = get_game_state()

        active_snakes = [snake for snake in state['snakes'] if snake['geometry']]
        
        for snake in active_snakes:
            snake_head = snake['geometry'][0]
            food = state['food']

            if food:
                
                target = min(food, key=lambda f: abs(snake_head[0] - f['c'][0]) +
                                                abs(snake_head[1] - f['c'][1]) + abs(snake_head[2] - f['c'][2]))

                target_c = target['c']

                fences = []
                for fence in state['fences']:
                    fences.append((fence[0], fence[1], fence[2]))

                direction = ph.find_path((snake_head[0], snake_head[1], snake_head[2]), (target_c[0], target_c[1], target_c[2]), fences)
                enemies = state['enemies']
                enemies_fences = []

                move(snake['id'], direction)

        time.sleep(1)

if __name__ == "__main__":
    main()
