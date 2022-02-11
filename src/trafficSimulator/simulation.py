import math
from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .single_vehicle_generator import SingleVehicleGenerator
from .traffic_signal import TrafficSignal

class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.action_vehicles = []
        self.traffic_signals = []
        self.integ = 0

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_single_gen(self, config={}):
        gen = SingleVehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_signal(self, roads, config={}):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        return sig

    def ego_collide(self, v1, v2):
        dist = self.distance(v1, v2.x, v2.y)
        if dist < 1:
            return True
        return False

    def auto_collide(self, v1):
        for road in self.roads:
            for v in road.vehicles:
                x = road.start[0]+(v.x*road.angle_cos)
                y = road.start[1]+(v.x*road.angle_sin)
                dist = self.distance(v1, x, y)
                if dist < 1:
                    return True
        return False

    def offroad(self, v, offset):
        for road in self.roads:
            x1, y1 = v.x, v.y
            x2, y2 = road.start[0], road.start[1]
            x3, y3 = road.end[0], road.end[1]
            area = 0.5*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))
            area = abs(area)
            dist = (2*area)/road.length
            if dist < offset and abs(x1-max(x2, x3)) < offset/2 and abs(x1-min(x2, x3)) < offset/2:
                return False
        return True

    def distance(self, v, x, y):
        return math.sqrt((v.x-x)**2+(v.y-y)**2)

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.dt)

        # Add vehicles
        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self)

        for av in self.action_vehicles:
            av.update(self.dt)

        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Create a copy and reset some vehicle properties
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                # In all cases, remove it from its road
                road.vehicles.popleft() 
        # Increment time
        self.t += self.dt
        self.frame_count += 1

            


    def run(self, steps):
        for _ in range(steps):
            self.update()