# Generated by Django 3.0.7 on 2020-09-16 21:49

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_auto_20200916_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreparationMixin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('testapp.abstractvegetable',),
            managers=[
                ('mymanager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='abstractvegetable',
            name='instructions',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='abstractvegetable',
            name='type',
            field=models.CharField(choices=[('testapp.preparationmixin', 'preparation mixin'), ('testapp.fruit', 'fruit'), ('testapp.vegetable', 'vegetable'), ('testapp.kiwismoothie', 'kiwi smoothie')], db_index=True, max_length=255),
        ),
        migrations.CreateModel(
            name='KiwiSmoothie',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('testapp.fruit', 'testapp.preparationmixin'),
            managers=[
                ('mymanager', django.db.models.manager.Manager()),
            ],
        ),
    ]