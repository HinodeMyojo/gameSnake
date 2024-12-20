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

CELL_SIZE = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
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

def get_food():
    food = response.json()['food']

def get_game_state():
    """Получить состояние карты."""
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()

def draw_map(screen, state):
    screen.fill(COLOR_BG)
    for food in state.get('food', []):
        x, y, z = food['c']
        pygame.draw.rect(screen, COLOR_FOOD, (x * CELL_SIZE, y * CELL_SIZE, z * CELL_SIZE))

    for snake in state.get('snakes', []):
        for segment in snake['geometry']:
            x, y, z = segment
            pygame.draw.rect(screen, COLOR_SNAKE, (x * CELL_SIZE, y * CELL_SIZE, z * CELL_SIZE))

    for fence in state.get('fences', []):
        x, y, я = fence
        pygame.draw.rect(screen, COLOR_FENCES, (x * CELL_SIZE, y * CELL_SIZE, z * CELL_SIZE,))

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
                                         abs(snake_head[1] - f['c'][1]))

        target_c = target['c']

        direction = [
                (1 if target_c[0] > snake_head[0] else -1) if target_c[0] != snake_head[0] else 0,
                (1 if target_c[1] > snake_head[1] else -1) if target_c[1] != snake_head[1] else 0,
                (1 if target_c[2] > snake_head[2] else -1) if target_c[2] != snake_head[2] else 0
            ]                                              

        move(snake['id'], direction)
    

        draw_map(screen, state)

        clock.tick(FPS)

    pygame.quit()
    # init()

if __name__ == "__main__":
    main()
