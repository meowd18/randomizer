# Generated by Django 5.1.6 on 2025-02-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0003_alter_jeux_coop'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeux',
            name='favori',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='jeux',
            name='jamais_joué',
            field=models.BooleanField(null=True),
        ),
    ]
