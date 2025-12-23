from sys import path
path.append(".")

import pygame
# type: ignore
# pylint: disable=all
from python.player import *
from python.constants import *

#window setup
pygame.init()
WIN = pygame.display.set_mode((WORLD_CONSTANTS.WIDTH, WORLD_CONSTANTS.HEIGHT))
pygame.display.set_caption("game")
BG = pygame.image.load("assets/game background.jpeg")

player_manager = PlayerManager()

#platform (x, y, length and width)
LEVELS = {
    1: [
        (100, 750, 200, 20),
        (400, 500, 200, 20),
        (700, 400, 150, 20),
    ],
    2: [
        (50, 650, 150, 20),
        (300, 550, 100, 20),
        (500, 450, 150, 20),
        (750, 350, 100, 20),
    ],
    3: [
        (150, 600, 100, 20),
        (350, 500, 100, 20),
        (550, 400, 100, 20),
        (200, 300, 200, 20),
        (600, 200, 150, 20),
    ]
}
#makes players and draws them. ghost player is drawn differently than when active
def draw(platforms): 
    WIN.blit(BG, (0,0))
    for platform in platforms:
        pygame.draw.rect(WIN, WORLD_CONSTANTS.PLATFORM_COLOR, platform)
    player_manager.draw_players(WIN)
    pygame.display.update()

#home screen 
def draw_home_screen():
    WIN.fill((20, 20, 40))
    title_font = pygame.font.SysFont("georgia", 55, bold=True)
    instruction_font = pygame.font.SysFont("georgia", 30)
    title_text = title_font.render("GHOST SWITCH PLATFORMER", True, "white")
    title_rect = title_text.get_rect(center=(WORLD_CONSTANTS.WIDTH//2, WORLD_CONSTANTS.HEIGHT//3))
    WIN.blit(title_text, title_rect)
    instructions = [
        "Control one player at a time",
        "",
        "Arrow Keys - Move and Jump",
        "SPACE - Switch Players",
        "",
        "Press ENTER to Start"
    ]
    y_offset = WORLD_CONSTANTS.HEIGHT//2
    for line in instructions:
        text = instruction_font.render(line, True, "white")
        text_rect = text.get_rect(center=(WORLD_CONSTANTS.WIDTH//2, y_offset))
        WIN.blit(text, text_rect)
        y_offset += 40
    pygame.display.update()
#main game setup and loop
def main():
    run = True
    clock = pygame.time.Clock()
    # TODO: change game_started back to False
    game_started = True
    current_level = 1
    platforms = [pygame.Rect(p) for p in LEVELS[current_level]]
    while run:
        clock.tick(60) #60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                elif not game_started and event.key == pygame.K_RETURN: 
                    game_started = True
                elif game_started and event.key == pygame.K_SPACE:
                    player_manager.switch_player()
        
        if not game_started:
            draw_home_screen()
        else:
            keys = pygame.key.get_pressed()
            player_manager.calculate_movement(keys, platforms)
            
            draw(platforms)
    
    pygame.quit()

if __name__ == "__main__":
    main()