from scipy.spatial import distance
from collections import deque
import math

class Road:
    def __init__(self, start, end, type = 1, center = None):
        self.start = start
        self.end = end
        # type = 1 single lane straint
        # type = 1 double lane straint
        # type = 3 single lane circular
        # type = 4 double lane circular  ## TODO make it eclipse rather than circular
        self.type = type
        
        # if type = 1 or 2 then centre is None
        self.center = center


        self.vehicles = deque()

        self.init_properties()
        
    def angle(self, A, B, C):
        Ax, Ay = A[0]-B[0], A[1]-B[1]
        Cx, Cy = C[0]-B[0], C[1]-B[1]
        a = math.atan2(Ay, Ax)
        c = math.atan2(Cy, Cx)
        if a < 0: a += math.pi*2
        if c < 0: c += math.pi*2
        return (math.pi*2 + c - a) if a > c else (c - a)

    def init_properties(self):
        if(self.type<=2):
            self.length = distance.euclidean(self.start, self.end)
        else:
            self.radius = distance.euclidean(self.center, self.end)
            self.length = distance.euclidean(self.start, self.center) * self.angle(self.start,self.center,self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def update(self, dt):
        n = len(self.vehicles)

        if n > 0:
            # Update first vehicle
            self.vehicles[0].update(None, dt)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)

             # Check for traffic signal
            if self.traffic_signal_state:
                # If traffic signal is green or doesn't exist
                # Then let vehicles pass
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                # If traffic signal is red
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    # Slow vehicles in slowing zone
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._v_max)
                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and\
                   self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                    # Stop vehicles in the stop zone
                    self.vehicles[0].stop()
