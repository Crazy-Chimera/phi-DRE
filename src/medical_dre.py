import math
from dataclasses import dataclass
from typing import List, Dict

import numpy as np


@dataclass
class BiologicalSource:
    name: str
    frequency: float
    amplitude: float
    phase: float = 0.0


class BodyFieldSimulator:
    def __init__(self):
        self.sources = [
            BiologicalSource("heart", 1.2, 1e-4),
            BiologicalSource("lungs", 0.3, 1e-5),
            BiologicalSource("nerves", 100.0, 1e-6),
            BiologicalSource("muscles", 20.0, 1e-5),
        ]

    def compute_phi(self, t: float) -> float:
        phi = 0.5
        for source in self.sources:
            phi += source.amplitude * math.sin(2 * math.pi * source.frequency * t + source.phase)
        phi += np.random.normal(0, 1e-7)
        return float(np.clip(phi, 0.1, 1.0))

    def compute_gradient(self, t: float) -> float:
        dt = 0.0001
        return (self.compute_phi(t) - self.compute_phi(t - dt)) / dt


class MedicalDREGenerator:
    def __init__(self, efficiency: float = 0.5, volume: float = 1e-6):
        self.efficiency = efficiency
        self.volume = volume
        self.field = BodyFieldSimulator()
        self.power_output = 0.0

    def generate_power(self, t: float) -> float:
        grad = self.field.compute_gradient(t)
        phi = self.field.compute_phi(t)
        grad_n = -0.5 * phi ** (-1.5) * grad
        power = self.efficiency * grad_n**2 * self.volume
        self.power_output = max(0.0, power)
        return self.power_output


class Implant:
    def __init__(self, buffer_capacity: float = 1e-6, device_consumption: float = 1e-6):
        self.generator = MedicalDREGenerator()
        self.buffer_capacity = buffer_capacity
        self.device_consumption = device_consumption
        self.energy_buffer = buffer_capacity * 0.5

    def run(self, duration: float = 60.0, dt: float = 0.001) -> List[Dict[str, float]]:
        history = []
        steps = int(duration / dt)
        for i in range(steps):
            t = i * dt
            power = self.generator.generate_power(t)
            self.energy_buffer += power * dt
            self.energy_buffer -= self.device_consumption * dt
            self.energy_buffer = float(np.clip(self.energy_buffer, 0, self.buffer_capacity))
            history.append({"time": t, "power": power, "buffer": self.energy_buffer})
        return history
