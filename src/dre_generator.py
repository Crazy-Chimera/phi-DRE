"""
Φ‑DRE Generator – Dynamic Refractive Energy according to the Theory of Everything.
Modulates the refractive index of the Φ field and extracts energy from information gradients.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List

import numpy as np


@dataclass
class PhField:
    """Φ field – entanglement density (0–1)."""

    grid: np.ndarray = field(default_factory=lambda: np.ones((100, 100)) * 0.5)
    ref_index: np.ndarray = field(default_factory=lambda: np.ones((100, 100)) * 1.0)
    modulation_strength: float = 0.1
    frequency: float = 1.0  # MHz


class DREGenerator:
    """Dynamic Refractive Energy generator."""

    def __init__(self, grid_size: int = 100):
        self.grid_size = grid_size
        self.field = PhField()
        self.field.grid = np.ones((grid_size, grid_size)) * 0.5
        self.field.ref_index = 1.0 / np.sqrt(self.field.grid + 1e-6)
        self.energy_output = 0.0
        self.efficiency = 0.0
        self.time = 0.0

    def apply_em_modulation(self, strength: float, frequency: float):
        """Apply electromagnetic modulation to the refractive index."""
        self.field.modulation_strength = strength
        self.field.frequency = frequency
        phase = 2 * math.pi * frequency * self.time
        modulation = strength * np.sin(phase) * np.exp(-np.linspace(-2, 2, self.grid_size) ** 2)
        self.field.grid = np.clip(0.5 + modulation[None, :] * 0.1, 0.1, 1.0)
        self.field.ref_index = 1.0 / np.sqrt(self.field.grid + 1e-6)

    def compute_energy_output(self) -> float:
        """Compute energy from information gradients."""
        grad_n = np.gradient(self.field.ref_index)
        grad_magnitude = np.sqrt(grad_n[0] ** 2 + grad_n[1] ** 2)
        epsilon_0 = 8.854e-12
        c = 3e8
        area = 1.0
        power = 0.5 * epsilon_0 * c * np.mean(grad_magnitude**2) * area
        return power

    def compute_efficiency(self) -> float:
        """Efficiency – ratio of output energy to input energy."""
        input_energy = self.field.modulation_strength**2 * self.field.frequency
        if input_energy > 0:
            return self.energy_output / input_energy
        return 0.0

    def run_cycle(self, num_steps: int = 100) -> List[Dict[str, float]]:
        """Run one modulation cycle."""
        outputs = []
        for step in range(num_steps):
            self.time = step / num_steps
            self.apply_em_modulation(
                strength=self.field.modulation_strength,
                frequency=self.field.frequency,
            )
            self.energy_output = self.compute_energy_output()
            self.efficiency = self.compute_efficiency()
            outputs.append(
                {
                    "time": self.time,
                    "phi_avg": float(np.mean(self.field.grid)),
                    "n_avg": float(np.mean(self.field.ref_index)),
                    "power": float(self.energy_output),
                    "efficiency": float(self.efficiency),
                }
            )
        return outputs

    def evaluate(self) -> float:
        """Elegance of the generator – C/K."""
        C = self.field.modulation_strength * self.field.frequency
        K = self.energy_output
        return C / max(K, 1e-30)

    def get_status_report(self) -> str:
        """Generate a human‑readable status report."""
        lines = []
        lines.append("=" * 50)
        lines.append("Φ‑DRE GENERATOR STATUS")
        lines.append("=" * 50)
        lines.append(f"Modulation strength: {self.field.modulation_strength:.4f}")
        lines.append(f"Frequency: {self.field.frequency:.2f} MHz")
        lines.append(f"Average Φ: {np.mean(self.field.grid):.4f}")
        lines.append(f"Average refractive index: {np.mean(self.field.ref_index):.4f}")
        lines.append(f"Output energy: {self.energy_output:.6e} W")
        lines.append(f"Efficiency: {self.efficiency:.6f}")
        lines.append(f"Elegance (C/K): {self.evaluate():.6e}")
        return "\n".join(lines)
