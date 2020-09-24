from .animals import Animal


class Canine(Animal):

    def say_something(self):
        return "grrrrr"


class Wolf(Canine):

    def say_something(self):
        return "ah-ooooooh"


class AbstractDog(Animal):

    class Meta:
        abstract = True

    def say_something(self):
        return "bark bark"


# # TODO: Fix
# class Dog(AbstractDog):
#
#     def say_something(self):
#         return "woof woof"
