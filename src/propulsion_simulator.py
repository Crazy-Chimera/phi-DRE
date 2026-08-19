import math
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass
class VehicleState:
    x: float = 128.0
    y: float = 128.0
    vx: float = 0.0
    vy: float = 0.0
    throttle: float = 0.0
    brake: float = 0.0
    heading: float = 0.0


class PropulsionSimulator:
    def __init__(self, grid_size: int = 256, mass: float = 1000.0):
        self.grid_size = grid_size
        self.mass = mass
        self.phi = np.ones((grid_size, grid_size)) * 0.5
        self.ref_index = 1.0 / np.sqrt(self.phi + 1e-6)
        self.vehicle = VehicleState()
        self.time = 0.0

    def apply_modulation(self):
        x, y = self.vehicle.x, self.vehicle.y
        sigma = 3.0
        x_front = x + math.cos(self.vehicle.heading) * 5.0
        y_front = y + math.sin(self.vehicle.heading) * 5.0
        x_back = x - math.cos(self.vehicle.heading) * 5.0
        y_back = y - math.sin(self.vehicle.heading) * 5.0
        modulation = np.zeros((self.grid_size, self.grid_size))
        xx, yy = np.meshgrid(np.arange(self.grid_size), np.arange(self.grid_size))
        front_amp = self.vehicle.throttle * 0.1
        if front_amp > 0:
            r_front = np.sqrt((xx - x_front) ** 2 + (yy - y_front) ** 2)
            modulation += front_amp * np.exp(-(r_front**2) / (2 * sigma**2))
        back_amp = self.vehicle.brake * 0.1
        if back_amp > 0:
            r_back = np.sqrt((xx - x_back) ** 2 + (yy - y_back) ** 2)
            modulation -= back_amp * np.exp(-(r_back**2) / (2 * sigma**2))
        self.phi = np.clip(0.5 + modulation, 0.1, 1.0)
        self.ref_index = 1.0 / np.sqrt(self.phi + 1e-6)

    def compute_force(self) -> Tuple[float, float]:
        grad_y, grad_x = np.gradient(self.ref_index)
        xi = int(np.clip(self.vehicle.x, 1, self.grid_size - 2))
        yi = int(np.clip(self.vehicle.y, 1, self.grid_size - 2))
        hbar = 1.054e-34
        c = 3e8
        Q = 1e6
        fx = -hbar * c * grad_x[yi, xi] * Q
        fy = -hbar * c * grad_y[yi, xi] * Q
        return fx, fy

    def step(self, dt: float = 0.001):
        self.apply_modulation()
        fx, fy = self.compute_force()
        ax = fx / self.mass
        ay = fy / self.mass
        self.vehicle.vx += ax * dt
        self.vehicle.vy += ay * dt
        self.vehicle.x += self.vehicle.vx * dt / 0.01
        self.vehicle.y += self.vehicle.vy * dt / 0.01
        self.vehicle.x = np.clip(self.vehicle.x, 2, self.grid_size - 3)
        self.vehicle.y = np.clip(self.vehicle.y, 2, self.grid_size - 3)
        self.time += dt

    def run(self, throttle: float, duration: float = 10.0):
        steps = int(duration / 0.001)
        self.vehicle.throttle = throttle
        for _ in range(steps):
            self.step()
        speed = math.sqrt(self.vehicle.vx**2 + self.vehicle.vy**2)
        return {"speed": speed, "position": (self.vehicle.x, self.vehicle.y)}
