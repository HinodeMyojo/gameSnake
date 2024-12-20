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

# CELL_SIZE = 3
# SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 1000
# FPS = 10

# # Цвета
# COLOR_BG = (30, 30, 30)
# COLOR_SNAKE = (0, 255, 0)
# COLOR_FOOD = (255, 165, 0)
# COLOR_FENCES = (255, 0, 0)

# def init():

#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
    
#     snake0 = response.json()['snakes'][0]
#     snake1 = response.json()['snakes'][1]
#     snake2 = response.json()['snakes'][2]

#     print(snake0)
#     print(snake1)
#     print(snake2)

# def draw_cube(position, size, color):
#     glColor3fv(color)
#     glPushMatrix()
#     glTranslatef(position[0], position[1], position[2])
#     glutSolidCube(size)
#     glPopMatrix()

# def draw_snake(state):
#     for snake in state.get('snakes', []):
#         for segment in snake['geometry']:
#             draw_cube(segment, CELL_SIZE, COLOR_SNAKE)

# Функция для рисования карты
def draw_map(state):
    for food in state.get('food', []):
        draw_cube(food['c'], CELL_SIZE, COLOR_FOOD)

    for fence in state.get('fences', []):
        draw_cube(fence, CELL_SIZE, COLOR_FENCES)

    for enemies in state.get('enemies', []):
        for segment in enemies['geometry']:
            draw_cube(segment, CELL_SIZE, (1, 1, 1))

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
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main():
    running = True

    state = get_game_state()

    active_snakes = [snake for snake in state['snakes'] if snake['geometry']]
    
    print (active_snakes)
    
    for snake in active_snakes:
        snake_head = snake['geometry'][0]
        food = state['food']



        if food:
            
            target = min(food, key=lambda f: abs(snake_head[0] - f['c'][0]) +
                                            abs(snake_head[1] - f['c'][1]) + abs(snake_head[2] - f['c'][2]))

            target_c = target['c']

            fences = state['fences']

            enemies = state['enemies']
            enemies_fences = []

            
            direction = get_direction(snake_head, target_c)

        
            move(snake['id'], direction)

if __name__ == "__main__":
    main()
