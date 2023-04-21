"""This is a sample module"""
import math


def sample_function(name):
    """This is a sample function."""
    return f"Hello, {name}! Sqrt(2) = " + str(math.sqrt(2))


class Person:
    """This is a sample class."""

    def __init__(self, name):
        """This is the constructor."""
        self.name = name

    def say_hello(self):
        """This is a sample method."""
        return f"Hello, I am {self.name}."
