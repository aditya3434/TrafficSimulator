import pygame
from pygame import gfxdraw
import numpy as np
import random
from scipy.spatial import distance
import math

class Window:
    def __init__(self, sim, config={}):
        # Simulation to draw
        self.sim = sim

        # Set default configurations
        self.set_default_config()
        self.running = True

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)
        
    def set_default_config(self):
        """Set default configuration"""
        self.width = 1400
        self.height = 900
        self.bg_color = (250, 250, 250)

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False


    def loop(self, loop=None):
        """Shows a window visualizing the simulation and runs the loop function."""
        
        # Create a pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        score = 0

        # Draw loop
        while self.running:
            # Update simulation
            if loop:
                reward, model = loop(self.sim)
                score += reward

            # Draw simulation
            self.draw()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

            # Handle all events
            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse button down
                    if event.button == 1:
                        # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Mouse wheel up
                        self.zoom *=  (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5:
                        # Mouse wheel down 
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION:
                    # Drag content
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

        return score, model        

    def run(self, step=None, steps_per_update=1):
        """Runs the simulation by updating in every loop."""
        def loop(sim):
            sim.run(steps_per_update)

            if step:
                done = step(sim)
                if done:
                    self.running = False
            return 0, None

        return self.loop(loop)

    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width/2 + (x + self.offset[0])*self.zoom),
            int(self.height/2 + (y + self.offset[1])*self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width/2)/self.zoom),
            int(-self.offset[1] + (y - self.height/2)/self.zoom)
        )


    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)
            
    def draw_arc(self, center, start_angle, end_angle, radius_in, color_out):

        center = self.convert(*center)
        rect = pygame.Rect(center[0]-self.zoom*radius_in,center[1]-self.zoom*radius_in,2*radius_in*self.zoom, 2*radius_in*self.zoom)
        pygame.draw.arc(self.screen,color_out,rect,-end_angle,-start_angle, 6*self.zoom)
        # gfxdraw.pie(self.screen,*self.convert(*center), radius_in,start_angle,end_angle, color_in)
        # gfxdraw.arc(self.screen,*self.convert(*center), 11,0,3, color_out)
        #i  = 0


    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size
        #print(pos)
        #print(size)

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        #print(x)
        #print(y)
        #print(cos)
        #print(sin)
        
        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        #print(vertices)
        self.polygon(vertices, color, filled=filled)
        #pygame.draw.rect(self.screen, color, (x, y, l, h))

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(150, 150, 190)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )


    def draw_axes(self, color=(100, 100, 100)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150,150,150)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*i)),
                self.convert((x_end, unit*i)),
                color
            )

    def draw_roads(self):
        for road in self.sim.roads:
            # Draw road background
            #print(road.start)
            if road.type <=2 :
                self.rotated_box(
                    road.start,
                    (road.length, 6*road.type),
                    cos=road.angle_cos,
                    sin=road.angle_sin,
                    color=(128, 128, 128),
                    centered=False
                )
                # Draw road lines
                # self.rotated_box(
                #     road.start,
                #     (road.length, 0.25),
                #     cos=road.angle_cos,
                #     sin=road.angle_sin,
                #     color=(0, 0, 0),
                #     centered=False
                # )

                # Draw road arrow
                if road.length > 5: 
                    for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                        pos = (
                            road.start[0] + (road.length/2 + i + 3) * road.angle_cos,
                            road.start[1] + (road.length/2 + i + 3) * road.angle_sin
                        )

                        self.rotated_box(
                            pos,
                            (-1.25, 0.2),
                            cos=road.angle_cos,
                            sin=road.angle_sin,
                            color=(255, 255, 255)
                        )   
                        
            else:
                start_angle = np.arctan2(road.start[1] - road.center[1],road.start[0] - road.center[0])
                end_angle = np.arctan2(road.end[1] - road.center[1],road.end[0] - road.center[0])
                self.draw_arc(road.center,
                              (start_angle),
                              (end_angle),
                              (distance.euclidean(road.center,road.start)+3*(road.type-2)),
                              (128, 128, 128)
                        )
            


            # TODO: Draw road arrow

    def draw_vehicle(self, vehicle, road):
        
        l, h = vehicle.l,  2
        if road.type<=2:
            sin, cos = road.angle_sin, road.angle_cos
            x = road.start[0] + cos * vehicle.x 
            y = road.start[1] + sin * vehicle.x 
            
        else:
            theta = vehicle.x/road.radius
            #print(theta)
            start_angle = -np.arctan2(road.start[1] - road.center[1],road.start[0] - road.center[0])
            end_angle = -np.arctan2(road.end[1] - road.center[1],road.end[0] - road.center[0])
            #if(start_angle)
            if(start_angle > end_angle):
                final_angle = start_angle-theta
            else:
                final_angle = start_angle+theta
            
            sin, cos = math.sin(math.pi/2-final_angle), math.cos(math.pi/2-final_angle)
            x = road.center[0] + sin* road.radius
            y = road.center[1] - cos * road.radius
            

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def draw_action_vehicle(self, vehicle):
        l, h = 4,  2

        cos = np.cos(np.radians(vehicle.angle))
        sin = np.sin(np.radians(vehicle.angle))

        self.rotated_box((vehicle.x, vehicle.y), (l, h), cos=cos, sin=sin, color = vehicle.color, centered=True)

    def draw_vehicles(self):
        for road in self.sim.roads:
            # Draw vehicles
            for vehicle in road.vehicles:
                self.draw_vehicle(vehicle, road)

    def draw_action_vehicles(self):
        for av in self.sim.action_vehicles:
            self.draw_action_vehicle(av)

    def draw_signals(self):
        for signal in self.sim.traffic_signals:
            for i in range(len(signal.roads)):
                color = (0, 255, 0) if signal.current_cycle[i] else (255, 0, 0)
                for road in signal.roads[i]:
                    a = 0
                    position = (
                        (1-a)*road.end[0] + a*road.start[0],        
                        (1-a)*road.end[1] + a*road.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=road.angle_cos, sin=road.angle_sin,
                        color=color)

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))
        x, y = pygame.mouse.get_pos()
        (x, y) = self.inverse_convert(x, y)
        text_x = self.text_font.render(f'x={x}', False, (0, 0, 0))
        text_y = self.text_font.render(f'y={y}', False, (0, 0, 0))
        
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))
        self.screen.blit(text_x, (200, 0))
        self.screen.blit(text_y, (300, 0))


    def draw(self):
        # Fill background
        self.background(*self.bg_color)

        # Major and minor grid and axes
        # self.draw_grid(10, (220,220,220))
        # self.draw_grid(100, (200,200,200))
        # self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_action_vehicles()
        self.draw_signals()

        # Draw status info
        self.draw_status()
        