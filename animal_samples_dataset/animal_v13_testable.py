"""
animal_v13_testable.py
Designed for unit testing: functions return values instead of printing.
"""
class Animal:
    def __init__(self, name):
        self.name = name
        self.energy = 100

    def sleep(self):
        self.energy = 100
        return self.energy

    def play(self, cost=10):
        if self.energy >= cost:
            self.energy -= cost
            return True
        return False

# Example of a testable helper
def create_and_play(name, cost):
    a = Animal(name)
    succeeded = a.play(cost)
    return {"name": a.name, "succeeded": succeeded, "energy": a.energy}

if __name__ == "__main__":
    print(create_and_play("Test", 20))
