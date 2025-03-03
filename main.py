from Simulation import Simulation
from Initializer import *

if __name__ == "__main__":
    initializer = OrbitInitializer()
    sim = Simulation(initializer=initializer)
    sim.run()