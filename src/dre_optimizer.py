"""DRE parameter optimizer."""

from typing import Dict
import random

from .dre_generator import DREGenerator


class DREOptimizer:
    """Optimizes DRE generator parameters for maximum elegance."""

    def __init__(self, generator: DREGenerator):
        self.gen = generator
        self.best_params: Dict[str, float] = {}
        self.best_elegance = float("inf")

    def search(self, iterations: int = 1000) -> Dict[str, float]:
        """Random search over the parameter space."""
        for _ in range(iterations):
            strength = random.uniform(0.01, 0.5)
            frequency = random.uniform(0.1, 10.0)
            self.gen.apply_em_modulation(strength, frequency)
            self.gen.run_cycle(num_steps=50)
            elegance = self.gen.evaluate()
            if elegance < self.best_elegance:
                self.best_elegance = elegance
                self.best_params = {"strength": strength, "frequency": frequency}
        return self.best_params

    def report(self) -> str:
        return f"Best parameters: {self.best_params}, Elegance: {self.best_elegance:.6e}"
