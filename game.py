import pygame

pygame.init()

screen_width, screen_height = 1080, 720
surface = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake game")

SIDE_LENGTH = 15
START_POS = 225

rect = pygame.draw.rect(surface, (0, 0, 255), (START_POS, START_POS, SIDE_LENGTH, SIDE_LENGTH))

DIRECTIONS = {
    'up': (0, -SIDE_LENGTH),
    'down': (0, SIDE_LENGTH),
    'left': (-SIDE_LENGTH, 0),
    'right': (SIDE_LENGTH, 0)
}
curr_dir = DIRECTIONS['up']

class Section:


class Snake:
    def __init__(self):
        self.body = []
        self.add_section()
        self.add_section()
        self.add_section()
    
    def add_section(self):
         

def is_opposite(curr_direction, new_direction):
    for i, val in enumerate(curr_direction):
        if curr_direction[i] * -1 == new_direction[i]:
            return True 
    return False 
def direction_change_valid(curr_direction, new_direction, direction_changed):
    if direction_changed:
        return False
    if curr_direction == new_direction:
        return False
    if is_opposite(curr_direction, new_direction):
        return False
    return True

run = True 
while run:
    pygame.time.delay(0)
    direction_changed = False
    rect.move_ip(curr_dir[0], curr_dir[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction_change_valid(curr_dir, DIRECTIONS['left'], direction_changed):
                direction_changed = True
                curr_dir = DIRECTIONS['left']
            if event.key == pygame.K_RIGHT and direction_change_valid(curr_dir, DIRECTIONS['right'], direction_changed):
                direction_changed = True
                curr_dir = DIRECTIONS['right']
            if event.key == pygame.K_DOWN and direction_change_valid(curr_dir, DIRECTIONS['down'], direction_changed):
                direction_changed = True
                curr_dir = DIRECTIONS['down']
            if event.key == pygame.K_UP and direction_change_valid(curr_dir, DIRECTIONS['up'], direction_changed):
                direction_changed = True
                curr_dir = DIRECTIONS['up']

    surface.fill((255, 255, 255))
    pygame.draw.rect(surface, (176,176,176), rect)

    #pygame.display.blit(rect)
    pygame.display.update()

pygame.quit()
