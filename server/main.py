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

# snakes = [{id, directions}, {id, directions} ...]
def prepare_data(snakes):
    # Преобразуем массив snakes в нужный формат
    data = {
        "snakes": [
            {
                "id": snake["id"],
                "direction": snake["directions"] 
            }
            for snake in snakes
        ]
    }
    return data


def move(snakes):

    data = prepare_data(snakes)

    print(data)
    response = requests.post(f"{server_url}/player/move", headers=headers, json=data)
    return response.json()

def move_test(snake, direction):
    last_position = snake[0]
    snake[0][0] += direction[0]
    snake[0][1] += direction[1]
    snake[0][2] += direction[2]

    for snake_item in snake[1:]:
        tmp = snake_item
        snake_item[0] = last_position[0]
        snake_item[1] = last_position[1]
        snake_item[2] = last_position[2]
        last_position = tmp

def get_direction(head, target):
    if head[0] != target[0]: 
        return [1, 0, 0] if head[0] < target[0] else [-1, 0, 0]

    if head[1] != target[1]:
        return [0, 1, 0] if head[1] < target[1] else [0, -1, 0]

    if head[2] != target[2]: 
        return [0, 0, 1] if head[2] < target[2] else [0, 0, -1]

def get_game_state():
    """Получить состояние карты."""
    response = requests.post(url, headers=headers, json=data)
    # f = open("example_response copy.json", "r")
    # response = f.read()
    # return json.loads(response)
    return response.json()

def main():

    while True:

        state = get_game_state()

        active_snakes = [snake for snake in state['snakes']]

        moveList = []

        for snake in active_snakes:

            if not snake['geometry']:
                print("snake dead")
                continue

            snake_head = snake['geometry'][0]

            food = state['food']

            if not food:
                print("No food")
                continue
            
            target = min(food, key=lambda f: abs(snake_head[0] - f['c'][0]) +
                                            abs(snake_head[1] - f['c'][1]) + abs(snake_head[2] - f['c'][2]))

            target_c = target['c']

            fences = []
            for fence in state['fences']:
                fences.append((fence[0], fence[1], fence[2]))

            for enemy in state['enemies']:
                for enemy_body in enemy['geometry']:
                    fences.append((enemy_body[0], enemy_body[1], enemy_body[2]))
            
            for ourBody in snake['geometry'][1:]:
                fences.append((ourBody[0], ourBody[1], ourBody[2]))
            direction = ph.find_path((snake_head[0], snake_head[1], snake_head[2]), (target_c[0], target_c[1], target_c[2]), fences)

            moveList.append({"id": snake['id'], "directions": direction})

            
            print(snake['geometry'])
        
        move(moveList)

        print("tick remains: " + str(state['tickRemainMs']))
        print("#####################")
        time.sleep(state['tickRemainMs'] / 1000)


if __name__ == "__main__":
    main()
