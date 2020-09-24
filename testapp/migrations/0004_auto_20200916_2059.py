# Generated by Django 3.0.7 on 2020-09-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0003_auto_20200916_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='type',
            field=models.CharField(choices=[
                ('testapp.parrot', 'parrot'),
                ('testapp.canine', 'canine'),
                ('testapp.wolf', 'wolf'),
                ('testapp.abstractdog', 'abstract dog'),
                ('testapp.feline', 'feline'),
                ('testapp.bigcat', 'big cat'),
                ('testapp.angrybigcat', 'angry big cat')
            ], db_index=True, max_length=255),
        ),
    ]
