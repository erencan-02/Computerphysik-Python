from System import System
from Body import Body

import pygame
import numpy as np
import json

# Screen dimensions
WIDTH = 800
HEIGHT = 800

# Colours
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Time step
DT = 0.2

ARROW_SCALE = 2
ARROW_VELOCITY_THRESHOLD = 0.1
MASS_SCALE = 20

class Simulation:
    def __init__(self, json_file):
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("N-Body Simulation")
        self.clock = pygame.time.Clock()
        
        # System 
        self.system = System(G=1.0)
        
        # Simulation Setup
        self.running = True
        # self.init_bodies(json_file)
        self.init_bodies_random(10)
        self.max_mass = self.system.max_mass()

    
    def init_bodies(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.system.G = data.get("G", 1)
            for body_data in data.get("bodies", []):
                position = np.array(body_data["position"], dtype=np.float64)
                velocity = np.array(body_data["velocity"], dtype=np.float64)
                body = Body(body_data["mass"], position, velocity)
                
                self.system.add_body(body)
                
    def init_bodies_random(self, num_bodies):
        # Generate with position based on gaussian distribution
        for _ in range(num_bodies):
            position = np.random.normal(2) * 50 + WIDTH//2 
            velocity = np.random.randn(2) * 2
            mass = np.random.uniform(1, 10)
            
            body = Body(mass, position, velocity)
            self.system.add_body(body)
    
    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.system.update(DT)
            # self.draw_coordinate_system()
            self.draw_bodies()
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
            
    def draw_arrow(self, position, vector, color):
        if np.linalg.norm(vector) > 0:
            end_pos = position + vector * ARROW_SCALE
            pygame.draw.line(self.screen, color, position, end_pos, 2)
            
            # Arrowhead
            angle = np.arctan2(vector[1], vector[0])
            arrow_size = 5
            left_wing = end_pos - np.array([arrow_size * np.cos(angle - np.pi / 6), arrow_size * np.sin(angle - np.pi / 6)])
            right_wing = end_pos - np.array([arrow_size * np.cos(angle + np.pi / 6), arrow_size * np.sin(angle + np.pi / 6)])
            pygame.draw.line(self.screen, color, end_pos, left_wing, 2)
            pygame.draw.line(self.screen, color, end_pos, right_wing, 2)
            
    def draw_bodies(self):
        for body in self.system.bodies:
            
            radius = max(5, int((body.mass/self.max_mass) * MASS_SCALE))
            pygame.draw.circle(self.screen, WHITE, (int(body.position[0]), int(body.position[1])), radius)
            
            # if np.linalg.norm(body.velocity) > ARROW_VELOCITY_THRESHOLD:
            #     self.draw_arrow(body.position, body.velocity, RED)
