from Simulation import Simulation
from Initializer import *
import Constants

if __name__ == "__main__":
    # initializer = RandomGaussianInitializer(num_bodies=10, width=Constants.WIDTH, height=Constants.HEIGHT)
    # initializer = TwoBodyOrbitInitializer(width=Constants.WIDTH, height=Constants.HEIGHT)
    initializer = TangentVelocityInitializer(width=Constants.WIDTH, height=Constants.HEIGHT)
    
    sim = Simulation(initializer=initializer)
    sim.run()