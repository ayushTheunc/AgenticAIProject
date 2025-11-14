"""
animal_v1_basic.py
Very simple, minimal OOP example.
"""
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 100

    def make_sound(self):
        return "some sound"

    def sleep(self):
        self.energy = 100
        return f"{self.name} sleeps"

class Cat(Animal):
    def make_sound(self):
        return "meow"

class Dog(Animal):
    def make_sound(self):
        return "woof"

if __name__ == "__main__":
    print(Cat("Mittens", 2).make_sound())
    print(Dog("Rex", 4).make_sound())
