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

    def normalize_angle(self, angle):
        """
        Normalize an angle to [-pi, pi].
        :param angle: (float)
        :return: (float) Angle in radian in [-pi, pi]
        """
        while angle > np.pi:
            angle -= 2.0 * np.pi

        while angle < -np.pi:
            angle += 2.0 * np.pi

        return angle

    # Update position and velocity
    def update(self, dt):

        if self.model == "Kinematic":
            delta = np.clip(self.steer, -self.max_steer, self.max_steer)

            self.x += self.v * np.cos(self.yaw) * dt
            self.y += self.v * np.sin(self.yaw) * dt
            self.yaw += self.v / self.L * np.tan(delta) * dt
            self.yaw = self.normalize_angle(self.yaw)
            self.v += self.acc * dt

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
        
        

