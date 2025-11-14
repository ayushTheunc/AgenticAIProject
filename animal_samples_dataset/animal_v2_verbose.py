"""
animal_v2_verbose.py
Over-commented and verbose variable names.
"""
class AnimalEntity:
    # Initialize an animal entity with name and age
    def __init__(self, given_name, given_age):
        # store the name
        self.given_name = given_name
        # store the age in years
        self.given_age = given_age
        # energy level (0-100)
        self.energy_level = 100

    # generic sound maker
    def make_generic_sound(self):
        # returns a generic placeholder
        return "generic-animal-sound"

    # restful sleep
    def take_long_sleep_and_restore_energy(self):
        self.energy_level = 100
        return f"{self.given_name} now has energy {self.energy_level}"

class CatEntity(AnimalEntity):
    def make_generic_sound(self):
        return "meow-meow"

class DogEntity(AnimalEntity):
    def make_generic_sound(self):
        return "woof-woof"

if __name__ == "__main__":
    a = CatEntity("Cleo", 1)
    print(a.make_generic_sound())
    print(a.take_long_sleep_and_restore_energy())
