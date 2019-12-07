import pygame
from collections import namedtuple
import time
import random

Direction = namedtuple('Direction', 'x y')
SIDE_LENGTH = 15
START_X = 510
START_Y = 330 
DIRECTIONS = {
    'up': Direction(0, -SIDE_LENGTH),
    'down': Direction(0, SIDE_LENGTH),
    'left': Direction(-SIDE_LENGTH, 0),
    'right': Direction(SIDE_LENGTH, 0)
}
START_DIR = DIRECTIONS['up']
START_SNAKE_LENGTH = 6 
BACKGROUND_COLOR = (255, 255, 255)
SNAKE_COLOR = (176,176,176)
FRUIT_COLOR = (255, 0, 0)


class Section:
    def __init__(self, rect, curr_dir):
        self.rect = rect
        self.curr_dir = curr_dir

class Snake:
    def __init__(self, snake_length, surface):
        self.body = []
        self.surface = surface
        self.sections = set()
        self.init_snake(snake_length)
        self.head = self.body[0]
        self.tail = self.body[len(self.body) - 1]

    def get_new_rect_location(self, x, y):
        return (x, y, SIDE_LENGTH, SIDE_LENGTH) # left, top, width, height
    
    def draw_square(self, rect_loc):
        return pygame.draw.rect(self.surface, SNAKE_COLOR, rect_loc)

    def init_snake(self, snake_length):
        body_part = Section(
            rect=self.draw_square(self.get_new_rect_location(START_X, START_Y)),
            curr_dir=START_DIR,
        )
        self.body.append(body_part)
        self.sections.add((body_part.rect.x, body_part.rect.y))
        for i in range(0, snake_length - 1):
            body_part = Section(
                rect=body_part.rect.move(START_DIR.x * -1, START_DIR.y * -1),
                curr_dir=START_DIR
            )
            self.sections.add((body_part.rect.x, body_part.rect.y))
            self.body.append(body_part)

    def eat_fruit(self, new_dir=None):
        tail_x = self.tail.rect.x
        tail_y = self.tail.rect.y
        curr_dir = self.tail.curr_dir
        rect_loc = self.get_new_rect_location(tail_x, tail_y)
        body_part = Section(rect=self.draw_square(rect_loc), curr_dir=curr_dir)
        self.move(new_dir)
        self.body.append(body_part)
        self.sections.add((body_part.rect.x, body_part.rect.y))
        self.tail = body_part

    def move(self, new_dir=None):
        if new_dir:
            new_head = self.head.rect.move(new_dir.x, new_dir.y)
        else:
            new_head = self.head.rect.move(self.curr_dir.x, self.curr_dir.y)
        body_part = Section(
            rect=new_head,
            curr_dir=new_dir if new_dir else self.head.curr_dir
        )
        self.body.insert(0, body_part) 
        self.sections.add((body_part.rect.x, body_part.rect.y))
        self.head = body_part 
        self.sections.remove((self.tail.rect.x, self.tail.rect.y))
        self.body.pop()
        self.tail = self.body[len(self.body) - 1]

    @property
    def curr_dir(self):
        return self.head.curr_dir

    @property
    def x(self):
        return self.head.rect.x

    @property
    def y(self):
        return self.head.rect.y


class SnakeGame:
    def __init__(self): 
        pygame.init()
        self.screen_width = 1080
        self.screen_height = 720
        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.snake = Snake(START_SNAKE_LENGTH, self.surface)
        pygame.display.set_caption("Snake game")
        self.curr_dir = self.snake.curr_dir
        self.direction_changed = False
        self.create_fruit()
        self.actions = {
            pygame.K_LEFT: {'func': self.change_direction, 'args': [DIRECTIONS['left']]},
            pygame.K_RIGHT: {'func': self.change_direction, 'args': [DIRECTIONS['right']]},
            pygame.K_UP: {'func': self.change_direction, 'args': [DIRECTIONS['up']]},
            pygame.K_DOWN: {'func': self.change_direction, 'args': [DIRECTIONS['down']]},

        }

    def change_direction(self, new_direction):
        if self.direction_change_valid(new_direction):
            self.direction_changed = True
            self.curr_dir = new_direction

    def valid_movement(self):
        if any([
            (self.snake.x + self.curr_dir.x) < 0,
            (self.snake.x + 2 * self.curr_dir.x) > self.screen_width,
            (self.snake.y + self.curr_dir.y) < 0,
            (self.snake.y + 2 * self.curr_dir.y) > self.screen_height,
            (self.snake.x + self.curr_dir.x, self.snake.y + self.curr_dir.y) in self.snake.sections
        ]):
            return False
        return True

    def direction_change_valid(self, new_direction):
        if self.direction_changed:
            return False
        if self.curr_dir == new_direction:
            return False
        if any([
            self.curr_dir.x * -1 == new_direction.x,
            self.curr_dir.y * -1 == new_direction.y
        ]):
            return False
        return True

    def create_fruit(self):
        self.fruit_x = rand_x = random.randrange(0, self.screen_width, 15)
        self.fruit_y = rand_y = random.randrange(0, self.screen_height, 15)

    def update(self):
        self.surface.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.surface, FRUIT_COLOR, (self.fruit_x, self.fruit_y, SIDE_LENGTH, SIDE_LENGTH))
        for section in self.snake.body:
            pygame.draw.rect(self.surface, SNAKE_COLOR, section.rect)

        pygame.display.update()

    def run(self):
        while 1:
            pygame.time.delay(70)
            self.direction_changed = False
            if self.snake.x == self.fruit_x and self.snake.y == self.fruit_y:
                self.snake.eat_fruit()
                self.create_fruit()
            elif self.valid_movement():
                self.snake.move(self.curr_dir)
            else:
                time.sleep(.5)
                self.__init__()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key in self.actions:
                    action, args = self.actions[event.key].values()
                    action(*args)
                               
            self.update()


if __name__ == '__main__':
    s = SnakeGame()
    s.run()
