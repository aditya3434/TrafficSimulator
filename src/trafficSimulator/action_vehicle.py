import numpy as np

class ActionVehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)\

    def set_default_config(self):
        self.v = 0  
        self.acc = 0
        self.steer = 0;
        self.x = 0;
        self.y = 0;
        self.angle = 0;
        self.color = (255,22,12)

    def get_state(self):
        return [self.v, (self.x, self.y), [self.acc, self.steer]]

    def set_state(self, state):
        self.acc = state[0]
        self.steer = state[1]

    def update(self, dt):
        # Update position and velocity
        self.angle += self.steer*dt*100

        cos = np.cos(np.radians(self.angle))
        sin = np.sin(np.radians(self.angle))

        self.v += self.acc*dt

        self.x += (self.v*dt)*cos
        self.y += (self.v*dt)*sin
        
        

