from trafficSimulator import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([
    ((0, 100), (140, 100)),
    ((150, 110), (150, 200)),
    ((140, 100), (150, 110), 3,(140, 110))
])

sim.create_gen({
    'vehicle_rate': 5,
    'vehicles': [
        {"path": [0, 2, 1]}
    ]
})


# Start simulation
win = Window(sim)
win.offset = (-150, -110)
win.run(steps_per_update=5)