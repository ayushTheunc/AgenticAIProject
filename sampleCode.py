"""
Animal Management System
A simple demonstration of object-oriented programming with animals.
"""

class Animal:
    """Base class for all animals."""
    
    def __init__(self, name, age):
        """Initialize an animal with name and age."""
        self.name = name
        self.age = age
        self.energy = 100
    
    def make_sound(self):
        """Make a generic animal sound."""
        return "Some generic animal sound"
    
    def sleep(self):
        """Animal sleeps and restores energy."""
        self.energy = 100
        return f"{self.name} is sleeping and restored energy to {self.energy}"
    
    def get_info(self):
        """Return basic information about the animal."""
        return f"Name: {self.name}, Age: {self.age}, Energy: {self.energy}"


class Cat(Animal):
    """Cat class that extends Animal."""
    
    def __init__(self, name, age, breed="Mixed"):
        super().__init__(name, age)
        self.breed = breed
        self.lives_remaining = 9
    
    def make_sound(self):
        """Cat makes a meow sound."""
        return "Meow!"
    
    def purr(self):
        """Cat purrs when happy."""
        return f"{self.name} is purring contentedly"
    
    def hunt(self):
        """Cat goes hunting."""
        if self.energy >= 20:
            self.energy -= 20
            return f"{self.name} caught a mouse! Energy: {self.energy}"
        else:
            return f"{self.name} is too tired to hunt"


class Dog(Animal):
    """Dog class that extends Animal."""
    
    def __init__(self, name, age, breed="Mixed"):
        super().__init__(name, age)
        self.breed = breed
        self.loyalty = 100
    
    def make_sound(self):
        """Dog makes a bark sound."""
        return "Woof!"
    
    def fetch(self):
        """Dog plays fetch."""
        if self.energy >= 15:
            self.energy -= 15
            self.loyalty += 5
            return f"{self.name} fetched the ball! Energy: {self.energy}, Loyalty: {self.loyalty}"
        else:
            return f"{self.name} is too tired to fetch"
    
    def guard(self):
        """Dog guards the house."""
        return f"{self.name} is guarding the house vigilantly"


class Bear(Animal):
    """Bear class that extends Animal."""
    
    def __init__(self, name, age, species="Brown Bear"):
        super().__init__(name, age)
        self.species = species
        self.hibernating = False
    
    def make_sound(self):
        """Bear makes a roar sound."""
        return "ROAR!"
    
    def hibernate(self):
        """Bear hibernates for winter."""
        if not self.hibernating:
            self.hibernating = True
            self.energy = 50
            return f"{self.name} is now hibernating"
        else:
            return f"{self.name} is already hibernating"
    
    def wake_up(self):
        """Bear wakes up from hibernation."""
        if self.hibernating:
            self.hibernating = False
            self.energy = 80
            return f"{self.name} woke up from hibernation"
        else:
            return f"{self.name} is already awake"
    
    def fish(self):
        """Bear goes fishing."""
        if not self.hibernating and self.energy >= 25:
            self.energy -= 25
            return f"{self.name} caught a salmon! Energy: {self.energy}"
        elif self.hibernating:
            return f"{self.name} can't fish while hibernating"
        else:
            return f"{self.name} is too tired to fish"


class Foo:
    """A utility class for demonstration purposes."""
    
    def __init__(self, value=42):
        """Initialize Foo with a value."""
        self.value = value
        self.operations_count = 0
    
    def bar(self):
        """A method that returns the classic 'bar' response to 'foo'."""
        self.operations_count += 1
        return f"bar - operation #{self.operations_count}"
    
    def calculate(self, x, y, operation="add"):
        """Perform basic calculations."""
        self.operations_count += 1
        
        if operation == "add":
            result = x + y
        elif operation == "subtract":
            result = x - y
        elif operation == "multiply":
            result = x * y
        elif operation == "divide":
            if y != 0:
                result = x / y
            else:
                return "Error: Division by zero"
        else:
            return f"Error: Unknown operation '{operation}'"
        
        return f"Result of {x} {operation} {y} = {result}"
    
    def reset(self):
        """Reset the operations counter."""
        self.operations_count = 0
        return "Operations counter reset"


def animal_playground():
    """Demonstrate the animal classes."""
    # Create animals
    cat = Cat("Whiskers", 3, "Siamese")
    dog = Dog("Buddy", 5, "Golden Retriever")
    bear = Bear("Bruno", 8, "Grizzly Bear")
    
    print("=== Animal Playground ===")
    
    # Display animal info
    animals = [cat, dog, bear]
    for animal in animals:
        print(f"\n{animal.__class__.__name__}: {animal.get_info()}")
        print(f"Sound: {animal.make_sound()}")
    
    # Demonstrate specific behaviors
    print(f"\n{cat.purr()}")
    print(cat.hunt())
    
    print(f"\n{dog.fetch()}")
    print(dog.guard())
    
    print(f"\n{bear.hibernate()}")
    print(bear.fish())  # Should fail while hibernating
    print(bear.wake_up())
    print(bear.fish())  # Should succeed now


    
    
    return "Playground demonstration complete"


def foo_demonstration():
    """Demonstrate the Foo class."""
    print("\n=== Foo Demonstration ===")
    
    foo = Foo(100)
    print(foo.bar())
    print(foo.calculate(10, 5, "add"))
    print(foo.calculate(10, 5, "multiply"))
    print(foo.calculate(10, 0, "divide"))  # Should handle division by zero
    print(foo.reset())
    
    return "Foo demonstration complete"


if __name__ == "__main__":
    try:
        result1 = animal_playground()
        result2 = foo_demonstration()
        print(f"\n{result1}")
        print(f"{result2}")
    except Exception as e:
        print(f"An error occurred: {e}")
