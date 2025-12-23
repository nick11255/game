"""
All player logic is stored as a single player. In the draw step, both players are offset from the same position.
The local player world is positioned such that top left is (0,0).
The player's position is the top left corner of the player
"""

from sys import path
path.append(".")
import pygame
from pygame.math import Vector2
from python.constants import *

# enum for which player
class PLAYER_ENUM:
    PLAYER1 = 1
    PLAYER2 = 2

class PlayerManager:
    """Singleton class for managing the player. I made this a class since using file global variables is messy."""
    def __init__(self):
        self.player_pos = Vector2(0, 0)
        self.player_vel = Vector2(0, 0)
        self.player_is_jumping = False
        self.active_player = PLAYER_ENUM.PLAYER1

        self.player1_rect = pygame.Rect(0, 0, PLAYER_CONSTANTS.WIDTH, PLAYER_CONSTANTS.HEIGHT)
        self.player2_rect = pygame.Rect(0, 0, PLAYER_CONSTANTS.WIDTH, PLAYER_CONSTANTS.HEIGHT)

    def local_to_world(self, player_local_pos, which_player):
        """Convert local player position to world positions for both players"""
        if which_player == PLAYER_ENUM.PLAYER1:
            return (player_local_pos.x - 200, player_local_pos.y)
        else:
            return (player_local_pos.x + 200, player_local_pos.y)

    def world_to_local(self, player_world_pos, which_player):
        """Convert world player position to local position"""
        if which_player == PLAYER_ENUM.PLAYER1:
            return Vector2(player_world_pos.x + 200, player_world_pos.y)
        else:
            return Vector2(player_world_pos.x - 200, player_world_pos.y)

    def switch_player(self):
        global active_player
        active_player = PLAYER_ENUM.PLAYER2\
            if active_player == PLAYER_ENUM.PLAYER1\
            else PLAYER_ENUM.PLAYER1

    def check_floor_collision(self, platforms):
        """Check if player is landing on a platform. If the player is touching a platform, return the y position of the platform top. Otherwise, return None."""
        player_bottom = self.player_pos.y + PLAYER_CONSTANTS.HEIGHT
        
        if self.player_pos.y >= WORLD_CONSTANTS.HEIGHT - PLAYER_CONSTANTS.HEIGHT:
            return WORLD_CONSTANTS.HEIGHT - PLAYER_CONSTANTS.HEIGHT

        for platform in platforms:
            plat_rect = pygame.Rect(platform)
            
            # Check if player is falling onto platform
            if (self.player_pos.x + PLAYER_CONSTANTS.WIDTH > plat_rect.x and 
                self.player_pos.x < plat_rect.x + plat_rect.width):
                
                # Check if player's bottom crosses platform's top
                if player_bottom >= plat_rect.y and player_bottom <= plat_rect.y + plat_rect.height:
                    return plat_rect.y - PLAYER_CONSTANTS.HEIGHT
        return None

    def calculate_movement(self, keys, platforms):
        # calculate velocity then add that velocity to position at the end
        if keys[pygame.K_LEFT]: #left moveement and collision for walls
            self.player_vel.x = -PLAYER_CONSTANTS.X_VEL
        elif keys[pygame.K_RIGHT]: #right moveement and collision for walls
            self.player_vel.x = PLAYER_CONSTANTS.X_VEL
        else:
            self.player_vel.x = 0
        
        if keys[pygame.K_UP] and not self.player_is_jumping: #jump logic
            self.player_is_jumping = True
            self.player_vel.y = -PLAYER_CONSTANTS.JUMP_VEL

        if self.player_is_jumping:
            self.player_vel.y += PLAYER_CONSTANTS.GRAVITY
        
        """
        Instead of accounting for the world borders as a separate thing, we should make colliders for the world border.
        This will simplify the code since platforms and world borders will be the same thing. (I haven't done this yet if you want to work on it)
        """

        self.player_pos += self.player_vel
        # clamp player position if against a wall
        if self.player_pos.x < 0: # left wall
            self.player_pos.x = 0
        elif self.player_pos.x > WORLD_CONSTANTS.WIDTH - PLAYER_CONSTANTS.WIDTH: # right wall
            self.player_pos.x = WORLD_CONSTANTS.WIDTH - PLAYER_CONSTANTS.WIDTH

        # platform collision
        platform_y = self.check_floor_collision(platforms)
        if platform_y is not None:
            self.player_pos.y = platform_y
            self.player_is_jumping = False
            self.player_vel.y = 0
        else:
            self.player_is_jumping = True

        # update player rectangles to match new position
        

        """I'm not sure what this code was trying to do, so I'm leaving it commented out for now."""
        # # ground collision
        # if active_player == 1:    #save all current values to the right player
        #     player1_vel_y = current_vel_y
        #     player1_is_jumping = current_is_jumping
        #     player1_vel_x = current_vel_x

        #     if player2_is_jumping: #ghost player mechanics
        #         player2.y += player2_vel_y
        #         player2_vel_y += GRAVITY
        #         if player2.y >= HEIGHT - PLAYER_HEIGHT:
        #             player2.y = HEIGHT - PLAYER_HEIGHT
        #             player2_is_jumping = False
        #             player2_vel_y = 0
        #     player2.x += player2_vel_x
        #     player2_vel_x = 0
        #     if player2.x < 0:
        #         player2.x = 0
        #     elif player2.x + player2.width > WIDTH:
        #         player2.x = WIDTH - player2.width
        #     else:
        #     player2_vel_y = current_vel_y  #same ghost mechanics as before, but for when player 2 is active
        #     player2_is_jumping = current_is_jumping
        #     player2_vel_x = current_vel_x
        #     if player1_is_jumping:
        #         player1.y += player1_vel_y
        #         player1_vel_y += GRAVITY
        #         if player1.y >= HEIGHT - PLAYER_HEIGHT:
        #             player1.y = HEIGHT - PLAYER_HEIGHT
        #             player1_is_jumping = False
        #             player1_vel_y = 0
        #     player1.x += player1_vel_x
        #     player1_vel_x = 0
        #     if player1.x < 0:
        #         player1.x = 0
        #     elif player1.x + player1.width > WIDTH:
        #         player1.x = WIDTH - player1.width

    def draw_players(self, window):
        player_rect = pygame.Rect(self.player_pos.x, self.player_pos.y, PLAYER_CONSTANTS.WIDTH, PLAYER_CONSTANTS.HEIGHT)
        pygame.draw.rect(window, PLAYER_CONSTANTS.PLAYER_1_ACTIVE_COLOR, player_rect)
        # if active_player == 1:
        #    pygame.draw.rect(window, PLAYER_CONSTANTS.PLAYER_1_ACTIVE_COLOR, player1_rect)
        #    pygame.draw.rect(window, PLAYER_CONSTANTS.PLAYER_2_GHOST_COLOR, player2_rect)
        # else:
        #     pygame.draw.rect(window, PLAYER_CONSTANTS.PLAYER_2_ACTIVE_COLOR, player2_rect)  
        #     pygame.draw.rect(window, PLAYER_CONSTANTS.PLAYER_1_GHOST_COLOR, player1_rect)