# Generated by Django 3.0.7 on 2020-09-16 21:55

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_auto_20200916_2149'),
    ]

    operations = [
        migrations.DeleteModel(
            name='KiwiSmoothie',
        ),
        migrations.CreateModel(
            name='Smoothie',
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
        migrations.AlterField(
            model_name='abstractvegetable',
            name='type',
            field=models.CharField(choices=[('testapp.preparationmixin', 'preparation mixin'), ('testapp.fruit', 'fruit'), ('testapp.vegetable', 'vegetable'), ('testapp.smoothie', 'smoothie')], db_index=True, max_length=255),
        ),
    ]
