"""
animal_v7_optimized.py
Adds caching-like behavior and slightly more complex logic.
"""
from functools import lru_cache
import random

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100

    def expended_energy(self, activity_level):
        # energy cost scales nonlinearly
        cost = int((activity_level ** 1.5) * (1 + self.age * 0.01))
        self.energy = max(0, self.energy - cost)
        return cost

    def rest(self):
        self.energy = min(100, self.energy + 30)

class Dog(Animal):
    @lru_cache(maxsize=32)
    def preferred_treat(self, mood):
        # pretend expensive lookup
        choices = ("biscuit", "sausage", "cheese", "apple")
        return random.choice(choices) if mood > 0.5 else choices[0]

if __name__ == "__main__":
    d = Dog("Bolt", 5)
    print(d.preferred_treat(0.3))
    print(d.expended_energy(7))
    d.rest()
    print(d.energy)
