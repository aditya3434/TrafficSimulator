from .vehicle import Vehicle
from .action_vehicle import ActionVehicle
from numpy.random import randint

class SingleVehicleGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        """Set default configuration"""
        self.vehicle = {}
        self.spawn_time = 0

    def init_properties(self):
        if self.auto:
            self.vehicle_state = self.generate_auto_vehicle()
        else:
            self.vehicle_state = self.generate_action_vehicle()
        self.spawn = False

    def generate_auto_vehicle(self):
        return Vehicle(self.vehicle)

    def generate_action_vehicle(self):
        return ActionVehicle(self.vehicle)

    def update(self):
        """Add vehicles"""
        if not self.spawn and self.sim.t >= self.spawn_time:
            if self.auto:
                road = self.sim.roads[self.vehicle_state.path[0]]      
                if len(road.vehicles) == 0\
                   or road.vehicles[-1].x > self.vehicle_state.s0 + self.vehicle_state.l:
                    # If there is space for the generated vehicle; add it
                    road.vehicles.append(self.vehicle_state)
                self.vehicle_state = self.generate_auto_vehicle()
            else:
                self.vehicle_state = self.generate_action_vehicle()
                self.sim.action_vehicles.append(self.vehicle_state)
            self.spawn = True
            

