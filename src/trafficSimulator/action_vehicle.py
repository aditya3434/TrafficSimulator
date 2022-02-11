import numpy as np

class ActionVehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)\

    def set_default_config(self):

        self.model = "Normal"

        # Normal Driving parameters
        self.v = 0  
        self.acc = 0
        self.steer = 0;
        self.x = 0;
        self.y = 0;
        self.angle = 0;

        # Kinematic Model parameters
        self.L = 1
        self.max_steer = 1
        self.c_r = 0
        self.c_a = 0

        self.color = (255,22,12)


    # Get all attributes of the action vehicle
    def get_state(self):
        return [self.v, (self.x, self.y), self.angle, [self.acc, self.steer]]

    # Set acceleration and steer of the vehicle
    def set_state(self, state):
        self.acc = state[0]
        self.steer = state[1]

    # Update position and velocity
    def update(self, dt):

        if self.model == "Kinematic":
            f_load = self.v * (self.c_r + self.c_a * self.v)
            self.v += dt * (self.acc - f_load)

            # Compute the radius and angular velocity of the kinematic bicycle model
            delta = np.clip(self.steer, -self.max_steer, self.max_steer)
            yaw = np.radians(self.angle)

            # Compute the state change rate
            x_dot = self.v * np.cos(yaw)
            y_dot = self.v * np.sin(yaw)
            omega = self.v * np.tan(delta) / self.L

            # Compute the final state using the discrete time model
            self.x += x_dot * dt
            self.y += y_dot * dt
            self.angle += omega * dt

        else :
            # Changing angle according to steer
            self.angle += self.steer*dt*100

            self.angle = self.angle%360

            cos = np.cos(np.radians(self.angle))
            sin = np.sin(np.radians(self.angle))

            # Calculating velocity change
            self.v += self.acc*dt

            # Calculating position change
            self.x += (self.v*dt)*cos
            self.y += (self.v*dt)*sin
        
        

