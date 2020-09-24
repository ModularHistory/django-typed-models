import os

import django
import sys

# Initialize Django
print('Initializing Django...')
my_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(my_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testapp.settings')

from django.core.management import call_command

django.setup()

call_command('makemigrations', interactive=True)

from django.contrib.contenttypes.models import ContentType
from django.db import models

import pytest

try:
    import yaml
    PYYAML_AVAILABLE = True
    del yaml
except ImportError:
    PYYAML_AVAILABLE = False

from django.core import serializers
from django.core.exceptions import FieldError

from .models import TypedModelManager
from testapp.models import (
    AngryBigCat,
    Animal,
    BigCat,
    Canine,
    Wolf,
    AbstractDog,
    # Dog,
    Feline,
    Parrot,
    AbstractVegetable,
    Vegetable,
    Fruit,
    UniqueIdentifier,
    Child2,
    PreparationMixin,
    Smoothie
)

PARROT = 'testapp.parrot'
CANINE = 'testapp.canine'
WOLF = 'testapp.wolf'
ABSTRACT_DOG = 'testapp.abstractdog'
# DOG = 'testapp.dog'
FELINE = 'testapp.feline'
BIG_CAT = 'testapp.bigcat'
ANGRY_BIG_CAT = 'testapp.angrybigcat'
SMOOTHIE = 'testapp.smoothie'

# TODO: update this dictionary if any new animal types are added
ANIMAL_CLASSES = {
    PARROT: Parrot,
    CANINE: Canine,
    WOLF: Wolf,
    ABSTRACT_DOG: AbstractDog,
    # DOG: Dog,
    FELINE: Feline,
    BIG_CAT: BigCat,
    ANGRY_BIG_CAT: AngryBigCat,
}
ANIMAL_TYPE_SET = set(ANIMAL_CLASSES.keys())
ANIMAL_CLASS_SET = set(ANIMAL_CLASSES.values())

# TODO: update CANINE_TYPE_SET if any new canine types are added
CANINE_TYPE_SET = {CANINE, WOLF}
CANINE_CLASS_SET = {ANIMAL_CLASSES[canine_type] for canine_type in CANINE_TYPE_SET}

# TODO: update FELINE_TYPE_SET if any new feline types are added
FELINE_TYPE_SET = {FELINE, BIG_CAT, ANGRY_BIG_CAT}
FELINE_CLASS_SET = {ANIMAL_CLASSES[feline_type] for feline_type in FELINE_TYPE_SET}


class TestTypedModels:
    """Tests for django-typed-models."""

    @pytest.fixture
    def animals(self, db):
        self.created_types = []

        for name in {'kitteh', 'cheetah'}:
            feline = Feline.objects.create(name=name)
            create_unique_identifier(feline, name=name)
            self.created_types.append(FELINE)

        fido = Canine.objects.create(name='fido')
        create_unique_identifier(fido, name='fido')
        self.created_types.append(CANINE)

        hopper = Wolf.objects.create(name='Hopper')
        create_unique_identifier(hopper, name='Hopper')
        self.created_types.append(WOLF)

        # ellie = Dog.objects.create(name='Ellie')
        # create_unique_identifier(ellie, name='Ellie')
        # self.created_types.append(DOG)

        simba = BigCat.objects.create(name='simba')
        create_unique_identifier(simba, name='simba')
        self.created_types.append(BIG_CAT)

        mufasa = AngryBigCat.objects.create(name='mufasa')
        create_unique_identifier(mufasa, name='mufasa')
        self.created_types.append(ANGRY_BIG_CAT)

        kajtek = Parrot.objects.create(name='Kajtek')
        create_unique_identifier(kajtek, name='Kajtek')
        self.created_types.append(PARROT)

        Smoothie.objects.create(name='Avocado Smoothie', yumminess=9)

        self.created_types = sorted(self.created_types)

    def test_can_instantiate_base_model(self, db):
        # direct instantiation works fine without a type, as long as you don't save
        animal = Animal()
        assert not animal.type
        assert type(animal) is Animal

    def test_cant_save_untyped_base_model(self, db):
        # direct instantiation shouldn't work
        with pytest.raises(RuntimeError):
            Animal.objects.create(name='uhoh')

        # ... unless a type is specified
        Animal.objects.create(name='dingo', type='testapp.canine')

        # ... unless that type is stupid
        with pytest.raises(ValueError):
            Animal.objects.create(name='dingo', type='macaroni.buffaloes')

    def test_cant_save_abstract_typed_model(self, db):
        with pytest.raises(AttributeError):
            AbstractDog.objects.create(name='Cloud')

    def test_get_types(self):
        assert set(Animal.get_types()) == ANIMAL_TYPE_SET
        assert set(Canine.get_types()) == CANINE_TYPE_SET, f'{Animal.get_types()}'
        assert set(Feline.get_types()) == FELINE_TYPE_SET

    def test_get_type_classes(self):
        assert set(Animal.get_type_classes()) == ANIMAL_CLASS_SET
        assert set(Canine.get_type_classes()) == CANINE_CLASS_SET
        assert set(Feline.get_type_classes()) == FELINE_CLASS_SET

    def test_type_choices(self):
        type_choices = {cls for cls, _ in Animal._meta.get_field('type').choices}
        assert type_choices == set(Animal.get_types())

    def test_base_model_queryset(self, animals):
        # all objects returned
        qs = Animal.objects.all().order_by('type')
        types, classes = [obj.type for obj in qs], [type(obj) for obj in qs]
        assert types == self.created_types, f'\n{types}\n!={self.created_types}'
        created_classes = [ANIMAL_CLASSES[animal_type] for animal_type in self.created_types]
        assert classes == created_classes, f'\n{classes}\n!={created_classes}'

    def test_proxy_model_queryset(self, animals):
        """Verify that query results are as expected based on animals created."""
        # for base_animal_type in {CANINE, FELINE}:
        #     cls = ANIMAL_CLASSES.get(base_animal_type)
        #     qs = cls.objects.all().order_by('type')
        #     created_types =

        qs = Canine.objects.all().order_by('type')
        created_canine_types = [animal_type for animal_type in self.created_types if animal_type in CANINE_TYPE_SET]
        created_canine_classes = [ANIMAL_CLASSES[canine_type] for canine_type in created_canine_types]
        n_created_canines = len(created_canine_types)
        assert qs.count() == n_created_canines
        assert len(qs) == n_created_canines
        assert [obj.type for obj in qs] == created_canine_types
        assert [type(obj) for obj in qs] == created_canine_classes

        qs = Feline.objects.all().order_by('type')
        created_feline_types = [animal_type for animal_type in self.created_types if animal_type in FELINE_TYPE_SET]
        created_feline_classes = [ANIMAL_CLASSES[feline_type] for feline_type in created_feline_types]
        n_created_felines = len(created_feline_types)
        assert qs.count() == n_created_felines
        assert len(qs) == n_created_felines
        assert [obj.type for obj in qs] == created_feline_types
        assert [type(obj) for obj in qs] == created_feline_classes

    def test_doubly_proxied_model_queryset(self, animals):
        qs = BigCat.objects.all().order_by('type')
        assert qs.count() == 2
        assert len(qs) == 2
        assert [obj.type for obj in qs] == ['testapp.angrybigcat', 'testapp.bigcat']
        assert [type(obj) for obj in qs] == [AngryBigCat, BigCat]

    def test_triply_proxied_model_queryset(self, animals):
        qs = AngryBigCat.objects.all().order_by('type')
        assert qs.count() == 1
        assert len(qs) == 1
        assert [obj.type for obj in qs] == ['testapp.angrybigcat']
        assert [type(obj) for obj in qs] == [AngryBigCat]

    def test_recast_auto(self, animals):
        cat = Feline.objects.get(name='kitteh')
        cat.type = 'testapp.bigcat'
        cat.recast()
        assert cat.type == 'testapp.bigcat'
        assert type(cat) == BigCat

    def test_recast_string(self, animals):
        cat = Feline.objects.get(name='kitteh')
        cat.recast('testapp.bigcat')
        assert cat.type == 'testapp.bigcat'
        assert type(cat) == BigCat

    def test_recast_modelclass(self, animals):
        cat = Feline.objects.get(name='kitteh')
        cat.recast(BigCat)
        assert cat.type == 'testapp.bigcat'
        assert type(cat) == BigCat

    def test_recast_fail(self, animals):
        cat = Feline.objects.get(name='kitteh')
        with pytest.raises(ValueError):
            cat.recast(AbstractVegetable)
        with pytest.raises(ValueError):
            cat.recast('typedmodels.abstractvegetable')
        with pytest.raises(ValueError):
            cat.recast(Vegetable)
        with pytest.raises(ValueError):
            cat.recast('typedmodels.vegetable')

    def test_fields_in_subclasses(self, animals):
        canine = Canine.objects.all()[0]
        angry = AngryBigCat.objects.all()[0]

        angry.mice_eaten = 5
        angry.save()
        assert AngryBigCat.objects.get(pk=angry.pk).mice_eaten == 5

        angry.canines_eaten.add(canine)
        assert list(angry.canines_eaten.all()) == [canine]

        # Feline class was created before Parrot and has mice_eaten field which is non-m2m, so it may break accessing
        # known_words field in Parrot instances (since Django 1.5).
        parrot = Parrot.objects.all()[0]
        parrot.known_words = 500
        parrot.save()
        assert Parrot.objects.get(pk=parrot.pk).known_words == 500

    def test_fields_cache(self):
        mice_eaten = Feline._meta.get_field('mice_eaten')
        known_words = Parrot._meta.get_field('known_words')
        assert mice_eaten in AngryBigCat._meta.fields
        assert mice_eaten in Feline._meta.fields
        assert mice_eaten not in Parrot._meta.fields
        assert known_words in Parrot._meta.fields
        assert known_words not in AngryBigCat._meta.fields
        assert known_words not in Feline._meta.fields

    def test_m2m_cache(self):
        canines_eaten = AngryBigCat._meta.get_field('canines_eaten')
        assert canines_eaten in AngryBigCat._meta.many_to_many
        assert canines_eaten not in Feline._meta.many_to_many
        assert canines_eaten not in Parrot._meta.many_to_many

    def test_related_names(self, animals):
        """Ensure that accessor names for reverse relations are generated properly."""
        canine = Canine.objects.all()[0]
        assert hasattr(canine, 'angrybigcat_set')

    def test_queryset_defer(self, db):
        """Ensure that qs.defer() works correctly."""
        Vegetable.objects.create(name='cauliflower', color='white', yumminess=1)
        Vegetable.objects.create(name='spinach', color='green', yumminess=5)
        Vegetable.objects.create(name='sweetcorn', color='yellow', yumminess=10)
        Fruit.objects.create(name='Apple', color='red', yumminess=7)

        qs = AbstractVegetable.objects.defer('yumminess')

        objs = set(qs)
        for o in objs:
            assert isinstance(o, AbstractVegetable)
            assert set(o.get_deferred_fields()) == {'yumminess'}
            # does a query, since this field was deferred
            assert isinstance(o.yumminess, float)

    @pytest.mark.parametrize(
        'fmt',
        [
            'xml',
            'json',
            pytest.param(
                'yaml',
                marks=[
                    pytest.mark.skipif(
                        not PYYAML_AVAILABLE, reason='PyYAML is not available'
                    )
                ],
            ),
        ],
    )
    def test_serialization(self, fmt, animals):
        """Helper function used to check serialization and deserialization for concrete format."""
        animals = Animal.objects.order_by('pk')
        serialized_animals = serializers.serialize(fmt, animals)
        deserialized_animals = [
            wrapper.object for wrapper in serializers.deserialize(fmt, serialized_animals)
        ]
        assert set(deserialized_animals) == set(animals)

    def test_generic_relation(self, animals):
        for animal in Animal.objects.all():
            assert hasattr(animal, 'unique_identifiers')
            assert animal.unique_identifiers.all()

        for uid in UniqueIdentifier.objects.all():
            cls = uid.referent.__class__
            animal = cls.objects.filter(unique_identifiers=uid)
            assert isinstance(animal.first(), Animal)

        for uid in UniqueIdentifier.objects.all():
            cls = uid.referent.__class__
            animal = cls.objects.filter(unique_identifiers__name=uid.name)
            assert isinstance(animal.first(), Animal)

    def test_manager_classes(self):
        assert isinstance(Animal.objects, TypedModelManager)
        assert isinstance(Feline.objects, TypedModelManager)
        assert isinstance(BigCat.objects, TypedModelManager)

        # This one has a custom manager defined, but that shouldn't prevent objects from working
        assert isinstance(AbstractVegetable.mymanager, models.Manager)
        assert isinstance(AbstractVegetable.objects, TypedModelManager)

        # subclasses work the same way
        assert isinstance(Vegetable.mymanager, models.Manager)
        assert isinstance(Vegetable.objects, TypedModelManager)

    def test_uniqueness_check_on_child(self, db):
        child2 = Child2.objects.create(a='a')

        # Regression test for https://github.com/craigds/django-typed-models/issues/42
        # FieldDoesNotExist: Child2 has no field named 'b'
        child2.validate_unique()

    def test_non_nullable_subclass_field_error(self):
        with pytest.raises(FieldError):
            class Bug(Animal):
                # should have null=True
                num_legs = models.PositiveIntegerField()

    def test_explicit_recast_with_class_on_untyped_instance(self):
        animal = Animal()
        assert not animal.type
        animal.recast(Feline)
        assert animal.type == 'testapp.feline'
        assert type(animal) is Feline

    def test_explicit_recast_with_string_on_untyped_instance(self):
        animal = Animal()
        assert not animal.type
        animal.recast('testapp.feline')
        assert animal.type == 'testapp.feline'
        assert type(animal) is Feline


def create_unique_identifier(obj, name: str) -> UniqueIdentifier:
    return UniqueIdentifier.objects.create(
        name=name,
        object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj),
    )
