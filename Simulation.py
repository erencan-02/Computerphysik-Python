from System import System
from Body import Body
from Constants import *

import pygame
import numpy as np
import json

ARROW_SCALE = 4
ARROW_VELOCITY_THRESHOLD = 0.1
MASS_SCALE = 20
VECTOR_FIELD_SPACING = 50  # Distance between field vectors
VECTOR_FIELD_SCALE = 200  # Scaling factor for vector field arrows

class Simulation:
    def __init__(self, initializer):
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("N-Body Simulation")
        self.clock = pygame.time.Clock()
        
        # System 
        self.system = initializer.initialize()
        
        # Simulation Setup
        self.running = True
        self.max_mass = self.system.max_mass()

    def run(self):
        center_of_mass_history = []
        
        while self.running:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update the system
            self.system.update(DT)
            
            # Draw
            self.draw_coordinate_system()
            self.draw_bodies(get_radius=lambda b: max(5, int((b.mass/self.max_mass) * MASS_SCALE)))
            center = self.draw_center_of_mass()
            center_of_mass_history.append(center)
            self.draw_vector_field()
            
            for i in range(1, len(center_of_mass_history)):
                pygame.draw.line(self.screen, GREEN, center_of_mass_history[i-1], center_of_mass_history[i], 1)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def draw_coordinate_system(self):
        
        # Draw X and Y axis
        pygame.draw.line(self.screen, GRAY, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
        pygame.draw.line(self.screen, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
        
        # Draw ticks on X axis
        for x in range(0, WIDTH, 50):
            pygame.draw.line(self.screen, GRAY, (x, HEIGHT // 2 - 5), (x, HEIGHT // 2 + 5), 1)
        
        # Draw ticks on Y axis
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(self.screen, GRAY, (WIDTH // 2 - 5, y), (WIDTH // 2 + 5, y), 1)
            
    def draw_arrow(self, position, vector, color, scale=1.0):
        if np.linalg.norm(vector) > 0:
            end_pos = position + vector * scale
            pygame.draw.line(self.screen, color, position, end_pos, 2)
            
            # Arrowhead
            angle = np.arctan2(vector[1], vector[0])
            arrow_size = 5
            left_wing = end_pos - np.array([arrow_size * np.cos(angle - np.pi / 6), arrow_size * np.sin(angle - np.pi / 6)])
            right_wing = end_pos - np.array([arrow_size * np.cos(angle + np.pi / 6), arrow_size * np.sin(angle + np.pi / 6)])
            pygame.draw.line(self.screen, color, end_pos, left_wing, 2)
            pygame.draw.line(self.screen, color, end_pos, right_wing, 2)
            
    def draw_center_of_mass(self):
        center = self.system.center_of_mass()
        pygame.draw.circle(self.screen, GREEN, (int(center[0]), int(center[1])), 5)
        
        return center
            
    def draw_bodies(self, get_radius=lambda x: 5):
        for body in self.system.bodies:

            radius = get_radius(body)

            pygame.draw.circle(self.screen, WHITE, (int(body.position[0]), int(body.position[1])), radius)
            
            if np.linalg.norm(body.velocity) > ARROW_VELOCITY_THRESHOLD:
                self.draw_arrow(body.position, body.velocity, RED, scale=2.0)

            if np.linalg.norm(body.acceleration) > ARROW_VELOCITY_THRESHOLD:
                self.draw_arrow(body.position, body.acceleration, BLUE, scale=4.0)
                
    def draw_vector_line(self, position, vector, color):
        if np.linalg.norm(vector) > 0:
            end_pos = position + vector * 0.5  # Shorten the line
            pygame.draw.line(self.screen, color, position, end_pos, 1)
                    
    def draw_vector_field(self):
        for x in range(0, WIDTH, VECTOR_FIELD_SPACING):
            for y in range(0, HEIGHT, VECTOR_FIELD_SPACING):
                field_pos = np.array([x, y], dtype=np.float64)
                acceleration = np.zeros(2, dtype=np.float64)
                    
                for body in self.system.bodies:
                    r_vec = body.position - field_pos
                    r_mag = np.linalg.norm(r_vec) 
                    
                    # if r_mag > 20:
                    #     continue
                    
                    acceleration += self.system.G * body.mass / r_mag**2 * r_vec
                    
                if np.linalg.norm(acceleration) <= 10:
                    scale = 1.0
                else:
                    scale = 10/np.linalg.norm(acceleration)
                    
                self.draw_arrow(field_pos, acceleration, GRAY, scale=scale)
        