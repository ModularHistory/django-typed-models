from django.db import models

from .animals import Animal


class Parrot(Animal):
    known_words = models.IntegerField(null=True)

    def say_something(self):
        return "hello"
