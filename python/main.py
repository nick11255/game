from sys import path
path.append(".")

import pygame
import time
import random
# type: ignore
# pylint: disable=all

#window setup
pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game")
BG = pygame.image.load("assets/game background.jpeg")

#game constants
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 10
JUMP_VEL = 15
GRAVITY = 0.8


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
def check_platform_collision(player, platforms, vel_y):
    """Check if player is landing on a platform"""
    player_bottom = player.y + player.height
    
    for platform in platforms:
        plat_rect = pygame.Rect(platform)
        
        # Check if player is falling onto platform
        if (vel_y > 0 and 
            player.x + player.width > plat_rect.x and 
            player.x < plat_rect.x + plat_rect.width):
            
            # Check if player's bottom crosses platform's top
            if player_bottom >= plat_rect.y and player_bottom <= plat_rect.y + plat_rect.height:
                return plat_rect.y - player.height
    
    return None
#makes players and draws them. ghost player is drawn differently than when active
def draw(player1, player2, active_player, platforms): 
    WIN.blit(BG, (0,0))
    for platform in platforms:
        pygame.draw.rect(WIN, (100, 100, 100), platform)
    if active_player == 1:
       pygame.draw.rect(WIN, (100, 100, 255), player2)
       pygame.draw.rect(WIN, "red", player1)
    else:
        pygame.draw.rect(WIN, (255, 100, 100), player1)  
        pygame.draw.rect(WIN, "blue", player2)
    pygame.display.update()

#home screen 
def draw_home_screen():
    WIN.fill((20, 20, 40))
    title_font = pygame.font.SysFont("georgia", 55, bold=True)
    instruction_font = pygame.font.SysFont("georgia", 30)
    title_text = title_font.render("GHOST SWITCH PLATFORMER", True, "white")
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    WIN.blit(title_text, title_rect)
    instructions = [
        "Control one player at a time",
        "",
        "Arrow Keys - Move and Jump",
        "SPACE - Switch Players",
        "",
        "Press ENTER to Start"
    ]
    y_offset = HEIGHT//2
    for line in instructions:
        text = instruction_font.render(line, True, "white")
        text_rect = text.get_rect(center=(WIDTH//2, y_offset))
        WIN.blit(text, text_rect)
        y_offset += 40
    pygame.display.update()
#main game setup and loop
def main():
    run = True
    player1 = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_vel_y = 0
    player1_is_jumping = False
    player1_vel_x = 0
    player2 = pygame.Rect(800, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2_vel_y = 0
    player2_is_jumping = False
    player2_vel_x = 0
    active_player = 1 #tracks which player is active
    clock = pygame.time.Clock()
    game_started = False
    current_level = 1
    platforms = [pygame.Rect(p) for p in LEVELS[current_level]]
    while run:
        clock.tick(60) #60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_RETURN: 
                    game_started = True
                elif game_started and event.key == pygame.K_SPACE:
                    active_player = 2 if active_player == 1 else 1 #main switch mechanic
        
        if not game_started:
            draw_home_screen()
        else:
            keys = pygame.key.get_pressed() 
            if active_player == 1:
                current_player = player1
                current_vel_y = player1_vel_y#universal current player variables
                current_is_jumping = player1_is_jumping
                current_vel_x = player1_vel_x
            else:
                current_player = player2
                current_vel_y = player2_vel_y
                current_is_jumping = player2_is_jumping
                current_vel_x = player2_vel_x
            
            if keys[pygame.K_LEFT] and current_player.x - PLAYER_VEL >= 0: #left moveement and collision for walls
                current_player.x -= PLAYER_VEL
                current_vel_x = -PLAYER_VEL
            elif keys[pygame.K_RIGHT] and current_player.x + PLAYER_VEL + current_player.width <= WIDTH: #right moveement and collision for walls
                current_player.x += PLAYER_VEL
                current_vel_x = PLAYER_VEL
            else:
                current_vel_x = 0
            
            if keys[pygame.K_UP] and not current_is_jumping: #jump logic
                current_is_jumping = True
                current_vel_y = -JUMP_VEL
            
            if current_is_jumping:   #jump physics
                current_player.y += current_vel_y
                current_vel_y += GRAVITY
    
    # platform collision
            platform_y = check_platform_collision(current_player, platforms, current_vel_y)
            if platform_y is not None:
                current_player.y = platform_y
                current_is_jumping = False
                current_vel_y = 0
    # ground collision (needs work) 
            elif current_player.y >= HEIGHT - PLAYER_HEIGHT:
                current_player.y = HEIGHT - PLAYER_HEIGHT
                current_is_jumping = False
                current_vel_y = 0
            
            if active_player == 1:    #save all current values to the right player
                player1_vel_y = current_vel_y
                player1_is_jumping = current_is_jumping
                player1_vel_x = current_vel_x
                
                if player2_is_jumping: #ghost player mechanics
                    player2.y += player2_vel_y
                    player2_vel_y += GRAVITY
                    if player2.y >= HEIGHT - PLAYER_HEIGHT:
                        player2.y = HEIGHT - PLAYER_HEIGHT
                        player2_is_jumping = False
                        player2_vel_y = 0
                player2.x += player2_vel_x
                player2_vel_x = 0
                if player2.x < 0:
                    player2.x = 0
                elif player2.x + player2.width > WIDTH:
                    player2.x = WIDTH - player2.width
            else:
                player2_vel_y = current_vel_y  #same ghost mechanics as before, but for when player 2 is active
                player2_is_jumping = current_is_jumping
                player2_vel_x = current_vel_x
                if player1_is_jumping:
                    player1.y += player1_vel_y
                    player1_vel_y += GRAVITY
                    if player1.y >= HEIGHT - PLAYER_HEIGHT:
                        player1.y = HEIGHT - PLAYER_HEIGHT
                        player1_is_jumping = False
                        player1_vel_y = 0
                player1.x += player1_vel_x
                player1_vel_x = 0
                if player1.x < 0:
                    player1.x = 0
                elif player1.x + player1.width > WIDTH:
                    player1.x = WIDTH - player1.width
            
            draw(player1, player2, active_player, platforms)
    
    pygame.quit()

if __name__ == "__main__":
    main()