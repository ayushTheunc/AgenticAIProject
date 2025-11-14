# Intentional issues: logic bugs, poor error handling, and side-effects in constructors
class Animal:
    def __init__(self, name, age):
        # side-effect: printing during construction (bad for libraries)
        print("Creating", name)
        self.name = name
        self.age = age
        self.energy = "full"  # wrong type

    def sleep(self):
        # assumes numeric energy
        self.energy += 10

class Cat(Animal):
    def make_sound(self):
        return "meow" + 1  # TypeError

# no main guard; file will run on import
c = Cat("Bug", None)
c.sleep()
print(c.energy)
