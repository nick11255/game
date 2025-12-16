import pygame
import time
import random

pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game")
BG = pygame.image.load("game background.jpeg")


PLAYER_WIDTH = 40 #game constants
PLAYER_HEIGHT = 60
PLAYER_VEL = 10
JUMP_VEL = 15
GRAVITY = 0.8



def draw(player1, player2, active_player): 
    WIN.blit(BG, (0,0))
    if active_player == 1:
       pygame.draw.rect(WIN, (100, 100, 255), player2)
       pygame.draw.rect(WIN, "red", player1)
    else:
        pygame.draw.rect(WIN, (255, 100, 100), player1)  
        pygame.draw.rect(WIN, "blue", player2)
    
    pygame.display.update()

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
    
    active_player = 1
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    active_player = 2 if active_player == 1 else 1

        keys = pygame.key.get_pressed()
        if active_player == 1:
           current_player = player1
           current_vel_y = player1_vel_y
           current_is_jumping = player1_is_jumping
           current_vel_x = player1_vel_x
        else:
           current_player = player2
           current_vel_y = player2_vel_y
           current_is_jumping = player2_is_jumping
           current_vel_x = player2_vel_x
        if keys[pygame.K_LEFT] and current_player.x - PLAYER_VEL >= 0:
            current_player.x -= PLAYER_VEL
            current_vel_x = -PLAYER_VEL
        elif keys[pygame.K_RIGHT] and current_player.x + PLAYER_VEL + current_player.width <= WIDTH:
            current_player.x += PLAYER_VEL
            current_vel_x = PLAYER_VEL
        else: current_vel_x = 0
       
        if keys[pygame.K_UP] and not current_is_jumping:
            current_is_jumping = True
            current_vel_y = -JUMP_VEL
        
        # Apply gravity
        if current_is_jumping:
            current_player.y += current_vel_y
            current_vel_y += GRAVITY
            
            # Check if landed
            if current_player.y >= HEIGHT - PLAYER_HEIGHT:
                current_player.y = HEIGHT - PLAYER_HEIGHT
                current_is_jumping = False
                current_vel_y = 0
        
        # Update active player's state
        if active_player == 1:
            player1_vel_y = current_vel_y
            player1_is_jumping = current_is_jumping
            player1_vel_x = current_vel_x
            
            # Ghost player 2 continues with its momentum
            if player2_is_jumping:
                player2.y += player2_vel_y
                player2_vel_y += GRAVITY
                if player2.y >= HEIGHT - PLAYER_HEIGHT:
                    player2.y = HEIGHT - PLAYER_HEIGHT
                    player2_is_jumping = False
                    player2_vel_y = 0
            
            # Apply horizontal momentum to ghost
            player2.x += player2_vel_x
            player2_vel_x = 0
            # Boundary check
            if player2.x < 0:
                player2.x = 0
                player2_vel_x = 0
            elif player2.x + player2.width > WIDTH:
                player2.x = WIDTH - player2.width
                player2_vel_x = 0
                
        else:
            player2_vel_y = current_vel_y
            player2_is_jumping = current_is_jumping
            player2_vel_x = current_vel_x
            
            # Ghost player 1 continues with its momentum
            if player1_is_jumping:
                player1.y += player1_vel_y
                player1_vel_y += GRAVITY
                if player1.y >= HEIGHT - PLAYER_HEIGHT:
                    player1.y = HEIGHT - PLAYER_HEIGHT
                    player1_is_jumping = False
                    player1_vel_y = 0
            
            # Apply horizontal momentum to ghost
            player1.x += player1_vel_x
            player1_vel_x = 0
            # Boundary check
            if player1.x < 0:
                player1.x = 0
                player1_vel_x = 0
            elif player1.x + player1.width > WIDTH:
                player1.x = WIDTH - player1.width
                player1_vel_x = 0
        
        draw(player1, player2, active_player)
    pygame.quit()
if __name__ == "__main__":
    main()
