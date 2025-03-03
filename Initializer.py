import json
import numpy as np
from System import System
from Body import Body


class Initializer():
    def __init__(self):
        pass
    
    def initialize(self, model) -> System:
        raise NotImplementedError
    
class ConfigInitializer(Initializer):
    def __init__(self, config):
        self.config = config
    
    def initialize(self) -> System:
        bodies = []
        
        with open(self.config, 'r') as file:
            data = json.load(file)

            for body_data in data.get("bodies", []):
                position = np.array(body_data["position"], dtype=np.float64)
                velocity = np.array(body_data["velocity"], dtype=np.float64)
                body = Body(body_data["mass"], position, velocity)
                
                bodies.append(body)
                
        return System(G=1.0, bodies=bodies)
    
class RandomGaussianInitializer(Initializer):
    def __init__(self, num_bodies, width, height):
        self.num_bodies = num_bodies
        self.width = width
        self.height = height
    
    def initialize(self) -> System:
        bodies = []
        
        for _ in range(self.num_bodies):
            position = np.random.normal(size=(2)) * self.width//4 + self.width//2 
            velocity = np.random.uniform(low=-3, high=3, size=(2)) * 5
            mass = np.random.uniform(1, 10)
            
            body = Body(mass, position, velocity)
            bodies.append(body)
                    
        return System(G=1.0, bodies=bodies)
    
class OrbitInitializer(Initializer):
    def __init__(self):
        pass
    
    def initialize(self) -> System:
        bodies = []
        
        sun = Body(1000, np.array([400, 400], dtype=np.float64), np.array([0, 0], dtype=np.float64))
        earth = Body(1, np.array([400, 200], dtype=np.float64), np.array([0, 10], dtype=np.float64))
        
        bodies.append(sun)
        bodies.append(earth)
        
        return System(G=1.0, bodies=bodies)