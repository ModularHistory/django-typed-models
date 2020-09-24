from django.db import models

from typedmodels.models import TypedModel


class Source(TypedModel):
    description = models.CharField(max_length=255, null=True)


class TitledSource(Source):
    title = models.CharField(max_length=255, null=True)


class TextualSource(Source):
    editors = models.CharField(max_length=200, null=True, blank=True)


class Piece(TextualSource):
    page_number = models.PositiveSmallIntegerField(null=True, blank=True)
    end_page_number = models.PositiveSmallIntegerField(null=True, blank=True)


class Article(TitledSource, Piece):
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    volume = models.PositiveSmallIntegerField(null=True, blank=True)
