"""
animal_v4_typing.py
Uses dataclasses and type hints.
"""
from dataclasses import dataclass
from typing import Protocol

@dataclass
class Animal:
    name: str
    age: int
    energy: int = 100

    def make_sound(self) -> str:
        return "?"

    def sleep(self) -> None:
        self.energy = 100

class Hunter(Protocol):
    def hunt(self) -> str: ...

@dataclass
class Cat(Animal):
    breed: str = "Mixed"

    def make_sound(self) -> str:
        return "meow"

    def hunt(self) -> str:
        if self.energy >= 20:
            self.energy -= 20
            return f"{self.name} hunted successfully"
        return f"{self.name} too tired"

if __name__ == "__main__":
    c = Cat("Shadow", 4, breed="Siamese")
    print(c)
    c.hunt()
    print(c.energy)
