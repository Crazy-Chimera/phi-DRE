import math
from dataclasses import dataclass

import numpy as np


@dataclass
class CubeSatConfig:
    mass: float = 10.0
    orbit_altitude: float = 400.0
    orbit_velocity: float = 7.67e3
    generator_efficiency: float = 0.5
    num_qubits: int = 1000
    coherence_time: float = 100e-6
    coupling_constant: float = 1e-27
    solar_wind_strength: float = 5e-5


class SpaceFieldSimulator:
    def __init__(self, config: CubeSatConfig):
        self.config = config

    def compute_phi(self, t: float, altitude: float) -> float:
        solar_modulation = self.config.solar_wind_strength * math.sin(2 * math.pi * t / 100.0)
        cosmic_ray = np.random.normal(0, 1e-6)
        gravity_modulation = 1e-7 * (400.0 / altitude)
        phi = 0.5 + solar_modulation + cosmic_ray + gravity_modulation
        return float(np.clip(phi, 0.1, 1.0))

    def compute_gradient(self, t: float, altitude: float) -> float:
        dt = 0.001
        return (self.compute_phi(t + dt, altitude) - self.compute_phi(t, altitude)) / dt


class SuperconductingResonator:
    def __init__(self, config: CubeSatConfig):
        self.config = config

    def compute_gain(self) -> float:
        N = self.config.num_qubits
        g = self.config.coupling_constant
        T2 = self.config.coherence_time
        hbar = 1.054e-34
        return N * g * T2 / hbar

    def amplify(self, gradient: float) -> float:
        return gradient * self.compute_gain()


class SpaceThruster:
    def __init__(self, config: CubeSatConfig, resonator: SuperconductingResonator):
        self.config = config
        self.resonator = resonator

    def generate_thrust(self, gradient: float) -> float:
        hbar = 1.054e-34
        c = 3e8
        amplified = self.resonator.amplify(gradient)
        return -hbar * c * amplified


class CubeSat:
    def __init__(self, config: CubeSatConfig):
        self.config = config
        self.field = SpaceFieldSimulator(config)
        self.resonator = SuperconductingResonator(config)
        self.thruster = SpaceThruster(config, self.resonator)
        self.altitude = config.orbit_altitude
        self.velocity = config.orbit_velocity
        self.time = 0.0

    def step(self, dt: float = 0.01):
        gradient = self.field.compute_gradient(self.time, self.altitude)
        thrust = self.thruster.generate_thrust(gradient)
        acceleration = thrust / self.config.mass
        self.velocity += acceleration * dt
        self.altitude += self.velocity * dt * 0.001
        self.time += dt

    def run(self, duration: float = 3600.0):
        steps = int(duration / 0.01)
        for _ in range(steps):
            self.step()

    def get_report(self) -> str:
        return (
            f"Amplification factor: {self.resonator.compute_gain():.2e}\n"
            f"Final velocity: {self.velocity:.2f} m/s\n"
            f"Velocity change: {self.velocity - self.config.orbit_velocity:.2f} m/s\n"
            f"Final altitude: {self.altitude:.2f} km"
        )
