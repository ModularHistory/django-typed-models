from django.db import models

from typedmodels.models import TypedModel


class AbstractVegetable(TypedModel):
    """
    This is an entirely different typed model.
    """

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    yumminess = models.FloatField(null=False)

    mymanager = models.Manager()


class PreparationMixin(AbstractVegetable):
    """This is a mixin."""

    instructions = models.CharField(max_length=500, null=True)


class Fruit(AbstractVegetable):
    pass


class Vegetable(AbstractVegetable):
    pass


class Smoothie(Fruit, PreparationMixin):
    pass
