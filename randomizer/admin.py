from django.contrib import admin
from .models import Jeux

# Register your models here.
class ColJeux(admin.ModelAdmin):
    all_fields = Jeux._meta.get_fields()
    list_display = [field.name for field in all_fields if not (field.auto_created or field.is_relation)]

admin.site.register(Jeux, ColJeux)