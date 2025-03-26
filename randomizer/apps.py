from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os


class RandomizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'randomizer'

    def ready(self):
        # Insérer des données dans la bdd après les migrations
        post_migrate.connect(insert_initial_data, sender=self)

def insert_initial_data(sender, **kwargs):
    print("📌 Signal post_migrate déclenché !")

    from .models import Jeux
    from djangomizer.utils import insert_data

    file = "randomizer_jeux.ods"

    if Jeux.objects.count() == 0:
        insert_data(file)

    print(Jeux.objects.count())

    from django.contrib.auth.models import User
    if User.objects.count() == 0:
        #User.objects.create_superuser(username=os.getenv(config["SU_username"], "test"), password=os.getenv(config["SU_password"], "test"))
        User.objects.create_superuser(username="admin", password="admin")
        print("Superuser créé avec succès")
