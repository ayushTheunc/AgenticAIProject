"""
animal_v14_docstring_heavy.py
Sphinx-style docstrings and thorough documentation.
"""
class Animal:
    """
    Animal represents a generic animal.

    :param name: The animal's name.
    :param age: Age in years.
    :type name: str
    :type age: int
    """

    def __init__(self, name, age):
        """
        Initialize an Animal object.
        """
        self.name = name
        self.age = age
        self.energy = 100

    def make_sound(self):
        """
        Return a representative sound. Override in subclasses.
        :rtype: str
        """
        return ""

class Dog(Animal):
    """
    Dog subclass that implements make_sound.
    """

    def make_sound(self):
        """
        Return dog's sound.
        """
        return "Woof"
