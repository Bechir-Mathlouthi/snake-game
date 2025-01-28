import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class FoodType(Enum):
    NORMAL = 1
    SPECIAL = 2

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Advanced Snake Game")
        self.clock = pygame.time.Clock()
        self.obstacles = []
        self.special_food = None  # Initialize special_food before reset_game
        self.special_food_timer = 0
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.obstacles = self.generate_obstacles()
        self.food = self.spawn_food()
        self.special_food = None
        self.special_food_timer = 0
        self.score = 0
        self.game_over = False

    def generate_obstacles(self) -> List[Tuple[int, int]]:
        obstacles = []
        for _ in range(5):
            while True:
                pos = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
                if pos not in self.snake and pos not in obstacles:
                    if hasattr(self, 'food') and pos == self.food:
                        continue
                    if self.special_food and pos == self.special_food:
                        continue
                    obstacles.append(pos)
                    break
        return obstacles

    def spawn_food(self, food_type: FoodType = FoodType.NORMAL) -> Tuple[int, int]:
        while True:
            pos = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if pos not in self.snake and pos not in self.obstacles:
                if food_type == FoodType.NORMAL and self.special_food and pos == self.special_food:
                    continue
                return pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def update(self):
        if self.game_over:
            return

        # Move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = ((head_x + dx) % GRID_COUNT, (head_y + dy) % GRID_COUNT)

        # Check collision with self or obstacles
        if new_head in self.snake[1:] or new_head in self.obstacles:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            if random.random() < 0.2 and not self.special_food:
                self.special_food = self.spawn_food(FoodType.SPECIAL)
                self.special_food_timer = 50
        elif new_head == self.special_food:
            self.score += 5
            self.special_food = None
            self.special_food_timer = 0
        else:
            self.snake.pop()

        # Update special food timer
        if self.special_food:
            self.special_food_timer -= 1
            if self.special_food_timer <= 0:
                self.special_food = None

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = GREEN if i == 0 else WHITE
            pygame.draw.rect(self.screen, color, 
                           (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))

        # Draw food
        pygame.draw.rect(self.screen, RED,
                        (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, 
                         GRID_SIZE-1, GRID_SIZE-1))

        # Draw special food
        if self.special_food:
            pygame.draw.rect(self.screen, GOLD,
                           (self.special_food[0] * GRID_SIZE, 
                            self.special_food[1] * GRID_SIZE,
                            GRID_SIZE-1, GRID_SIZE-1))

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, BLUE,
                           (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE,
                            GRID_SIZE-1, GRID_SIZE-1))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()