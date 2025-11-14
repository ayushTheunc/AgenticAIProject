"""
animal_v6_pep8.py
Clean, PEP8-compliant, readable implementation.
"""
from typing import List


class Animal:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.energy = 100

    def make_sound(self) -> str:
        raise NotImplementedError

    def sleep(self) -> None:
        self.energy = 100

    def info(self) -> str:
        return f"{self.name} (age {self.age}) - energy: {self.energy}"


class Cat(Animal):
    def __init__(self, name: str, age: int, breed: str = "Mixed") -> None:
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self) -> str:
        return "Meow"


class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof"


def show_animals(animals: List[Animal]) -> None:
    for a in animals:
        print(a.info(), "-", a.make_sound())


if __name__ == "__main__":
    animals = [Cat("Milo", 1, "Tabby"), Dog("Bailey", 3)]
    show_animals(animals)
