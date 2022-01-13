import sys
sys.path.append('../')

from trafficSimulator import *
import random
import model as md
import matplotlib.pyplot as plt
import numpy as np

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

    return sim

def choose_action(choice):
    if choice == 0:
        return [0, 0]
    elif choice == 1:
        return [0.3, 0]
    else:
        return [0.8, 0]

def step(sim, epi, loss, model, steps_per_update):

    reward = 0
    done = False
    ego = sim.action_vehicles[0]

    x = ego.get_state()[1][0]
    vel = ego.get_state()[0]
    state = [x, vel]
    state = np.reshape(state, (1,2))

    choice = model.act(state)
    action = choose_action(choice)
    ego.set_state(action)

    sim.run(steps_per_update)

    x = ego.get_state()[1][0]
    vel = ego.get_state()[0]
    next_state = [x, vel]
    next_state = np.reshape(next_state, (1,2))

    reward -= (3-0.01*x)

    model.remember(state, choice, reward, next_state, done)
    model.replay(done, epi, loss)

    if x > 150:
        reward += 1000
        done = True

    return model, reward, done

loss = []
straight_model = md.DQN(3,2,'straight_model')
print("Epsilon : ", straight_model.epsilon)
x = []

episodes = 500

for i in range(episodes):
    sim = create_sim()
    win = Window(sim)
    win.offset = (-150, -110)
    score, straight_model = win.run(step, i, loss, straight_model, steps_per_update=4)
    print("Epsilon : ", straight_model.epsilon)
    loss.append(score)
    print("Episode : ",i+1, " --> Score : ", score)
    x.append(i+1)

plt.plot(x, loss)
plt.savefig('train.png')