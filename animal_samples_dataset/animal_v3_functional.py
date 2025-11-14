# Functional style: no classes, use dicts and functions
def create_animal(kind, name, age):
    return {"kind": kind, "name": name, "age": age, "energy": 100}

def make_sound(animal):
    return {"cat":"meow","dog":"woof"}.get(animal["kind"], "sound")

def change_energy(animal, delta):
    animal["energy"] = max(0, min(100, animal["energy"] + delta))
    return animal["energy"]

def feed(animal):
    return change_energy(animal, +20)

def play(animal):
    if animal["energy"] >= 10:
        return change_energy(animal, -10)
    return animal["energy"]

if __name__ == "__main__":
    a = create_animal("cat","Luna",3)
    print(make_sound(a), play(a), feed(a))
