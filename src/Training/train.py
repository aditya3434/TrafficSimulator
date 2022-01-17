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

# Discrete choices for our vehicle
def choose_action(choice):
    if choice == 0:
        return [0, 0]
    elif choice == 1:
        return [0.3, 0]
    else:
        return [0.8, 0]

# Agent step function
def step(sim, epi, loss, model, steps_per_update):

    # Initializing reward and done state
    reward = 0
    done = False

    # Ego vehicle which we are training
    ego = sim.action_vehicles[0]

    # X-coordinate of ego vehicle
    x = ego.get_state()[1][0]

    # Velocity of ego vehicle
    vel = ego.get_state()[0]

    # Current state
    state = [x, vel]
    state = np.reshape(state, (1,2))

    # Model gives choice
    choice = model.act(state)
    action = choose_action(choice)
    ego.set_state(action)

    # Agent takes choice and updates environment
    sim.run(steps_per_update)

    # Analyzing new state
    x = ego.get_state()[1][0]
    vel = ego.get_state()[0]
    next_state = [x, vel]
    next_state = np.reshape(next_state, (1,2))

    # Calculating step reward
    reward -= (3-0.01*x)

    # Model learning
    model.remember(state, choice, reward, next_state, done)
    model.replay(done, epi, loss)

    # If ego vehicle reaches the end of the road, sim ends
    if x > 299:
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