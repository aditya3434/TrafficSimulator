from trafficSimulator import *
import random
import model as md
import matplotlib.pyplot as plt
import numpy as np

class ModelWindow(Window):

    def __init__(self, sim, config={}):
        super().__init__(sim, config)

    def run(self, step=None, epi = 0, loss = None, model = None, steps_per_update=1):
        """Runs the simulation by updating in every loop."""
        def loop(sim):

            if not step:
                return 0, None

            ego = sim.action_vehicles[0]

            dist = sim.distance(ego, 150, 115)
            angle = ego.get_state()[2]

            state = [dist, angle]
            state = np.reshape(state, (1,2))

            choice = model.act(state)
            action = choose_action(choice)
            ego.set_state(action)

            sim.run(steps_per_update)

            reward, done = step(sim, steps_per_update)

            dist = sim.distance(ego, 150, 115)
            angle = ego.get_state()[2]

            next_state = [dist, angle]
            next_state = np.reshape(next_state, (1,2))

            model.remember(state, choice, reward, next_state, done)
            model.replay(done, epi, loss)

            if done:
                self.running = False

            return reward, model

        return self.loop(loop)


def create_sim():
    
    sim = Simulation()

    sim.create_roads([
        ((0, 100), (140, 100)),
        ((150, 110), (150, 200)),

        *curve_road((140, 100), (150, 110), (150, 100))
    ])

    sim.create_single_gen({
        'auto' : False,
        'vehicle': {"v": 4, "x": 140, "y": 100}
    })

    return sim

# Discrete choices for our vehicle
def choose_action(choice):
    if choice == 0:
        return [0.2, 0.2]
    elif choice == 1:
        return [0.2, 0.4]
    else:
        return [0.2, 0]

# Agent step function
def step(sim, steps_per_update):

    # Initializing reward and done state
    reward = 0
    done = False

    ego = sim.action_vehicles[0]

    dist = sim.distance(ego, 150, 115)
    angle = ego.get_state()[2]

    reward = 0.5*(50-dist)+0.1*(90-angle)
    
    # If ego vehicle reaches the end of the road, sim ends
    if dist < 3:
        print("Target reached!")
        reward += 1000
        done = True
    elif sim.offroad(ego, 4):
        print("Target offroad!")
        reward -= 1000
        done = True
    elif sim.t > 15:
        print("Timeout!")
        reward -= 1000
        done = True

    return reward, done

# Keeping track of scores
loss = []

# DQN model for our autonomous vehicle
turn_model = md.DQN(3,2,'turn_model')
x = []

# No. of training episodes
episodes = 500

# Training Loop
for i in range(episodes):
    # Create simulation
    sim = create_sim()
    sim.run(1)

    # Create window to display simulation
    win = ModelWindow(sim)
    win.offset = (-150, -110)

    # Get total score an updated model after simulation ends
    score, turn_model = win.run(step, i, loss, turn_model, steps_per_update=4)
    print("Epsilon : ",turn_model.epsilon)
    
    # Append total score to list
    loss.append(score)
    print("Episode : ",i+1, " --> Score : ", score)
    x.append(i+1)

plt.plot(x, loss)
plt.savefig('train_2.png')

# sim = create_sim()
# print(sim.roads)
# win = Window(sim)
# win.offset = (-150, -110)
# win.run(steps_per_update=5)