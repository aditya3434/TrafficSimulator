from trafficSimulator import *
import random

def create_sim():
    # Create simulation
    sim = Simulation()

    sim.create_roads([
        ((0, 98), (300, 98)),
    ])

    sim.create_single_gen({
        'auto' : True,
        'vehicle': [1, {"path": [0]}]
    })


    sim.create_single_gen({
        'auto' : False,
        'vehicle': [1, {"v": 6, "steer": 0.0, "x": 0, "y": 70, "model": "Normal"}]
    })

    return sim

def func_P(sim):
    ego = sim.action_vehicles[0]

    x = ego.get_state()[1][0]

    y = ego.get_state()[1][1]

    steer = 0.003*(98-y)

    print(y)

    ego.set_state([0, steer])

    if x > 299:
        return True

def func_PD(sim):
    ego = sim.action_vehicles[0]

    x = ego.get_state()[1][0]

    prev_y = ego.get_state()[1][1]

    sim.run(1)

    y = ego.get_state()[1][1]

    print(x, y)

    dev = y-prev_y

    steer = 0.01*(98-y)-dev

    ego.set_state([0, steer])

    if x > 299:
        return True

def func_PID(sim):
    ego = sim.action_vehicles[0]

    x = ego.get_state()[1][0]

    prev_y = ego.get_state()[1][1]

    sim.run(1)

    y = ego.get_state()[1][1]

    sim.integ += (98-y)

    dev = y-prev_y

    steer = 0.01*(98-y)-dev+0.00005*sim.integ

    ego.set_state([0, steer])

    if x > 299:
        return True

funcs = [func_P, func_PD, func_PID]

for func in funcs:
    # Create simulation
    sim = create_sim()

    # Create window to display sim
    win = Window(sim)
    win.offset = (-150, -110)

    # Run the simulation in the window
    win.run(func, steps_per_update=5)