"""
animal_v10_modular.py
Organized with helper functions and configuration dict.
"""
class AnimalBase:
    def __init__(self, name, age, config=None):
        self.name = name
        self.age = age
        self.energy = 100
        self.config = config or {}

    def perform(self, action):
        actions = {
            "sleep": self._do_sleep,
            "sound": self._do_sound,
        }
        fn = actions.get(action)
        if fn:
            return fn()
        raise ValueError(f"Unknown action {action}")

    def _do_sleep(self):
        self.energy = 100
        return "slept"

    def _do_sound(self):
        return "?"

class Cat(AnimalBase):
    def _do_sound(self):
        return "meow"

def run_demo():
    c = Cat("Nova", 2, config={"favorite_food": "tuna"})
    print(c.perform("sound"))
    print(c.perform("sleep"))

if __name__ == "__main__":
    run_demo()
