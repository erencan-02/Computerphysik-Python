import json
import numpy as np
from System import System
from Body import Body


class Initializer():
    def __init__(self):
        pass
    
    def initialize(self) -> System:
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
    
class SunEarthMoonInitializer(Initializer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def initialize(self) -> System:
        
        # Positions
        center = np.array([self.width//2, self.height//2], dtype=np.float64)
        earth_position = center + np.array([200, 0], dtype=np.float64)
        moon_position = earth_position + np.array([10, 0], dtype=np.float64)
        
        # Velocities
        earth_velocity = np.array([0, 10], dtype=np.float64)
        moon_velocity = np.array([0, 2], dtype=np.float64)
        
        # Mass
        sun_mass = 1500
        earth_mass = 87
        moon_mass = 1    
        
        # Initialize Bodies
        sun = Body(sun_mass, center, np.zeros(2, dtype=np.float64))
        earth = Body(earth_mass, earth_position, earth_velocity)
        moon = Body(moon_mass, moon_position, moon_velocity)
        
        bodies = [sun, earth, moon]
        return System(G=1.0, bodies=bodies)
    
class TwoBodyOrbitInitializer(Initializer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def initialize(self) -> System:
        bodies = []
        center = np.array([self.width//2, self.height//2], dtype=np.float64)
        offset = np.array([200, 0], dtype=np.float64)
        
        sun = Body(1000, center, np.array([0, 0], dtype=np.float64))
        earth = Body(10, center + offset, np.array([-10, 10], dtype=np.float64))
        
        bodies.append(sun)
        bodies.append(earth)
        
        return System(G=1.0, bodies=bodies)
    
    
class TangentVelocityInitializer(Initializer):
    def __init__(self, width, height, n=10):
        self.width = width
        self.height = height
        self.n = n
    
    def initialize(self) -> System:
        bodies = []
        
        for i in range(self.n):
            angle = i * 2 * np.pi / self.n
            position = np.array([self.width//2 + 200 * np.cos(angle), self.height//2 + 200 * np.sin(angle)], dtype=np.float64)
            velocity = np.array([-np.sin(angle), np.cos(angle)], dtype=np.float64) * 5
            mass = 50
            
            body = Body(mass, position, velocity)
            bodies.append(body)
        
        return System(G=1.0, bodies=bodies)