import sys
sys.path.append('../')

from trafficSimulator import *
import random

def create_sim():
    # Create simulation
    sim = Simulation()

    # Add multiple roads
    sim.create_roads([
        ((300, 98), (0, 98)),
        ((0, 102), (300, 102)),
        ((180, 60), (0, 60)),
        ((220, 55), (180, 60)),
        ((300, 30), (220, 55)),
        ((180, 60), (160, 98)),
        ((0, 178), (300, 178)),
        ((300, 182), (0, 182)),
        ((160, 102), (155, 180)),
        ((160, 98), (0, 98))
    ])

    # Creating a generator that keeps spawning auto-vehicles
    sim.create_gen({
        'vehicle_rate': 10,
        'vehicles': [
            [1, {"path": [4, 3, 5, 9]}],
            [1, {"path": [4, 3, 2]}],
            [1, {"path": [1]}],
            [1, {"path": [6]}],
            [1, {"path": [7]}]
        ]
    })

    # Creating 2 ego vehicles
    ego_vehicle1 = sim.create_single_gen({
        'auto' : False,
        'vehicle': [1, {"acc": 10, "x": 0, "y": 98, "model": "Kinematic", "L": 2.5, "c_a": 2.0, "c_r": 0.01}]
    })

    ego_vehicle2 = sim.create_single_gen({
        'auto' : False,
        'vehicle': [1, {"acc": 0.5, "x": 300, "y": 102, "model": "Normal", "angle": 180}]
    })

    return sim

def func(sim):
    ego1 = sim.action_vehicles[0]
    ego2 = sim.action_vehicles[1]

    # Check if the ego vehicles collide with each other or with any auto vehicles
    if sim.ego_collide(ego1, ego2) or sim.auto_collide(ego1) or sim.auto_collide(ego2):
        return True
    
# Create simulation
sim = create_sim()

# Create window to display sim
win = Window(sim)
win.offset = (-150, -110)

# Run the simulation in the window
win.run(func, steps_per_update=5)