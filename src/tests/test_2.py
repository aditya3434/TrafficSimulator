import yaml
from yaml.loader import SafeLoader
from trafficSimulator import *
import random

def create_sim():

    sim = Simulation()

    with open('scenario.yml') as f:
        scenario = yaml.load(f, Loader=SafeLoader)
    
    roads = [(tuple(road['start']), tuple(road['end'])) for road in scenario['roads']]

    sim.create_roads(roads)

    sim.create_gen(scenario['generator'])

    for vehicle in scenario['single_vehicles']:
        sim.create_single_gen(vehicle)
        
    return sim

def func(sim):
    ego1 = sim.action_vehicles[0]
    #ego2 = sim.action_vehicles[1]

    steer = random.uniform(-0.3, 0.3)

    ego1.set_state([0.5, steer])

    # Check if the ego vehicles collide with each other or with any auto vehicles
    # if sim.offroad(ego1, 3.5):
    #     return True
    
# Create simulation
sim = create_sim()

# Create window to display sim
win = Window(sim)
win.offset = (-150, -110)

# Run the simulation in the window
win.run(func, steps_per_update=5)