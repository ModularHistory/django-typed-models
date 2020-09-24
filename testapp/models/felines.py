from django.db import models

from .animals import Animal
from .canines import Canine


class Feline(Animal):
    def say_something(self):
        return "meoww"

    mice_eaten = models.IntegerField(default=0)


class BigCat(Feline):
    """
    This model tests doubly-proxied models.
    """

    def say_something(self):
        return "roar"


class AngryBigCat(BigCat):
    """
    This model tests triple-proxied models. Because we can.
    """

    canines_eaten = models.ManyToManyField(Canine)

    def say_something(self):
        return "raawr"
