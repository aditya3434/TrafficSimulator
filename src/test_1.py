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
        'vehicle': [1, {"acc": 0.5, "x": 0, "y": 98}]
    })

    ego_vehicle2 = sim.create_single_gen({
        'auto' : False,
        'vehicle': [1, {"acc": 0.5, "x": 300, "y": 98, "angle": 180}]
    })


    return sim

episodes = 1

def choose_action(choice):
    if choice == 0:
        return [0, 0]
    elif choice == 1:
        return [0.3, 0]
    else:
        return [0.8, 0.2]

def func(sim):

    reward = 0
    done = False
    ego1 = sim.action_vehicles[0]
    ego2 = sim.action_vehicles[1]
    choice = random.randint(0, 2)
    state = choose_action(choice)

    ego1.set_state(state)
    ego2.set_state(state)
    x = ego1.get_state()[1][0]
    vel = ego1.get_state()[0]

    reward += 0.1*vel

    if x > 299:
        done = True

    return reward, done

for i in range(episodes):
    sim = create_sim()
    win = Window(sim)
    win.offset = (-150, -110)
    score = win.run(func, steps_per_update=5)
    print("Reward : ", score)