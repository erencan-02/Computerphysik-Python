import numpy as np


class System:
    def __init__(self, G=1.0, softening=2):
        self.G = G
        self.softening = softening
        self.bodies = []
    
    def add_body(self, body):
        self.bodies.append(body)
    
    def compute_forces(self):
        for body in self.bodies:
            body.acceleration = np.zeros(2, dtype=np.float64)
        
        for i in range(len(self.bodies)-1):
            body1 = self.bodies[i]
            
            for j in range(i+1, len(self.bodies)):
                body2 = self.bodies[j]
                
                r_vec = body2.position - body1.position
                r_mag = np.linalg.norm(r_vec) + self.softening
                
                if r_mag > 0:
                    force = ((self.G * body1.mass * body2.mass) / r_mag**2) * r_vec
                    
                    body1.acceleration += force / body1.mass
                    body2.acceleration += -force / body2.mass
    
    def update(self, dt):
        self.compute_forces()
        for body in self.bodies:
            body.update(dt)
            
    def max_mass(self):
        return max([body.mass for body in self.bodies])
