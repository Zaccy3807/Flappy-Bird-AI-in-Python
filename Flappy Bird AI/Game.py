#The visual space/Game, DO NOT change this code.
import random
import pygame
import sys
import Bird_Brain
import Evolutionary_algorithm

Neuron = Bird_Brain.Neuron
NeuralNetwork = Bird_Brain.NeuralNetwork
Evolution = Evolutionary_algorithm.Evolution

pop_num = 0
#Create the first Network
nodes = [Neuron([], [], 0) for i in range(5)]
network = NeuralNetwork(nodes)
network.create_all()

genetic_al = Evolution([], 10, 101)

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('.....')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.5
bird_movement = 0
score = 0
passed_pipes = []

# Game objects
bird_size = 40
bird_x = 100
bird_y = screen_height // 2 - bird_size // 2

pipe_width = 60
pipe_gap = 150
pipe_height = random.randint(100, 400)
pipe_x = screen_width
pipe_y = random.randint(100, 400)

clock = pygame.time.Clock()

#Core game functions
def reset_game():
    global bird_movement, score, bird_y, pipe_x, pipe_height, pipe_y, passed_pipes
    bird_movement = 0
    score = 1
    bird_y = screen_height // 2 - bird_size // 2
    pipe_x = screen_width
    pipe_height = random.randint(100, 400)
    pipe_y = random.randint(100, 400)
    passed_pipes = []

def score_function(pipe_x, bird_x):
    if pipe_x <= bird_x < pipe_x + 3:
        return 1
    else:
        return 0

response = 0
running = True
while running:
    if response == 1:
        bird_movement = 0
        bird_movement -= 9

    # Draw background
    screen.fill(BLACK)

    # Bird movement
    bird_movement += gravity
    bird_y += bird_movement

    # Draw bird
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
    pygame.draw.rect(screen, WHITE, bird_rect)

    # Pipe movement
    pipe_x -= 3
    if pipe_x <= -pipe_width:
        pipe_x = screen_width
        pipe_height = random.randint(100, 400)
        pipe_y = random.randint(100, 400)
        passed_pipes.append(False)

    # Draw pipes
    upper_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    lower_pipe_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)
    pygame.draw.rect(screen, WHITE, upper_pipe_rect)
    pygame.draw.rect(screen, WHITE, lower_pipe_rect)

    # Calculate distances for AI inputs [Following variables(Y), y_velocity, distance to pillar(X)]
    distance_to_top_pillar = pipe_y + pipe_height - (bird_y + bird_size)
    distance_to_bottom_pillar = bird_y - (pipe_y + pipe_height + pipe_gap)

    # Collision detection
    if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect) or bird_y < 0 or bird_y > screen_height - bird_size:
        pop_num += 1
        genetic_al.mutate(network.nodes)
        reset_game()

    response = network.fly([distance_to_top_pillar, distance_to_bottom_pillar, (bird_x - pipe_x), bird_movement])

    score_text = f"Fitness: {int(score)}"
    pop_text = f'Population #: {int(pop_num)}'
    font = pygame.font.Font(None, 36)
    score_surface = font.render(score_text, True, WHITE)
    number_surface = font.render(pop_text, True, WHITE)
    score_rect = score_surface.get_rect(center=(screen_width // 2, 40))
    number_rect = number_surface.get_rect(center=(screen_width // 2, 80))
    screen.blit(score_surface, score_rect)
    screen.blit(number_surface, number_rect)

    score += 0.01666666666

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # Update display
    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()