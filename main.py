import pygame
import requests
import json
import time

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

CELL_SIZE = 5
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
FPS = 10

# Цвета
COLOR_BG = (30, 30, 30)
COLOR_SNAKE = (0, 255, 0)
COLOR_FOOD = (255, 165, 0)
COLOR_FENCES = (255, 0, 0)

def init():

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    snake0 = response.json()['snakes'][0]
    snake1 = response.json()['snakes'][1]
    snake2 = response.json()['snakes'][2]

    print(snake0)
    print(snake1)
    print(snake2)

# def get_food(state):
#     food = response.json()['food']

def get_game_state():
    """Получить состояние карты."""
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()

def draw_map(screen, state):
    screen.fill(COLOR_BG)
    
    for food in state.get('food', []):
        x, y, _ = food['c']
        pygame.draw.rect(screen, COLOR_FOOD, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for snake in state.get('snakes', []):
        for segment in snake['geometry']:
            x, y, _ = segment
            pygame.draw.rect(screen, COLOR_SNAKE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for fence in state.get('fences', []):
        x, y, _ = fence
        pygame.draw.rect(screen, COLOR_FENCES, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for enemies in state.get('enemies', []):
        for segment in enemies['geometry']:
            x, y, _ = segment
            pygame.draw.rect(screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змея")
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = get_game_state()
        
        print(state)

        snake = state['snakes'][0]
        snake_head = snake['geometry'][0]
        food = state['food']

        if food:
            target = min(food, key=lambda f: abs(snake_head[0] - f['c'][0]) +
                                            abs(snake_head[1] - f['c'][1]) + abs(snake_head[2] - f['c'][2]))

            target_c = target['c']

            direction = get_direction(snake_head, target_c)                                         

            move(snake['id'], direction)
        

            draw_map(screen, state)

            clock.tick(FPS)

    pygame.quit()
    # init()

if __name__ == "__main__":
    main()
