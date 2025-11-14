"""
animal_v8_inheritance_deep.py
Shows deeper inheritance: Mammal -> Canine/Feline -> Dog/Cat
"""
class Mammal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.warm_blooded = True

    def breathe(self):
        return f"{self.name} breathes air"

class Canine(Mammal):
    def bark(self):
        return "woof"

class Feline(Mammal):
    def purr(self):
        return "purr"

class Dog(Canine):
    def make_sound(self):
        return self.bark()

class Cat(Feline):
    def make_sound(self):
        return self.purr()

if __name__ == "__main__":
    print(Dog("Ranger",3).make_sound())
    print(Cat("Soot",2).make_sound())
