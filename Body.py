import numpy as np


class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(2, dtype=np.float64)
    
    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt