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

    sim.create_gen({
        'auto' : True,
        'vehicle_rate': 20,
        'vehicles': [
            [1, {"path": [4, 3, 2]}],
            [1, {"path": [1]}],
            [1, {"path": [6]}],
            [1, {"path": [7]}]
        ]
    })

    ego_vehicle = sim.create_single_gen({
        'auto' : False,
        'vehicle': [1, {"acc": 10, "x": 0, "y": 98, "model": "Kinematic", "L": 2.5, "c_a": 2.0, "c_r": 0.01}]
    })

    return sim

def func(sim):
    ego = sim.action_vehicles[0]

    x = ego.get_state()[1][0]
    
    if x > 100:
        return True

sim = create_sim()
win = Window(sim)
win.offset = (-150, -110)
win.run(func, steps_per_update=5)