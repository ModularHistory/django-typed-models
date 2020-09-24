from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import ForeignKey, PositiveIntegerField, CharField
from typedmodels.models import TypedModel


class UniqueIdentifier(models.Model):
    referent = GenericForeignKey()
    content_type = ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.CASCADE
    )
    object_id = PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    name = CharField(max_length=255)


class UniqueIdentifierMixin(models.Model):
    unique_identifiers = GenericRelation(
        UniqueIdentifier, related_query_name='referents'
    )

    class Meta:
        abstract = True


class Animal(TypedModel, UniqueIdentifierMixin):
    """
    Abstract model
    """

    name = models.CharField(max_length=255)

    def say_something(self):
        raise NotImplementedError

    # def __repr__(self):
    #     return u'<%s: %s>' % (self.__class__.__name__, self.name)

    def __str__(self):
        return str(self.name)


class Parent(TypedModel):
    a = models.CharField(max_length=1)


class Child1(Parent):
    b = models.OneToOneField('self', null=True, on_delete=models.CASCADE)


class Child2(Parent):
    pass
