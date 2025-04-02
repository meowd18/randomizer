from django.contrib import admin
from .models import *

# Register your models here.
class ColJeux(admin.ModelAdmin):
    all_fields = Jeux._meta.get_fields()
    list_display = [field.name for field in all_fields if not (field.auto_created or field.is_relation)]

class ColPartie(admin.ModelAdmin):
    all_fields = Partie._meta.get_fields()
    list_display = [field.name for field in all_fields if not (field.auto_created or field.is_relation)]
    list_display.append('jeu')
    def jeu(self, obj):
        return obj.nom.nom

admin.site.register(Jeux, ColJeux)
admin.site.register(Partie, ColPartie)