from django.contrib import admin

# Register your models here.
from .models import Building, Street, POI

admin.site.register(Building)
admin.site.register(Street)
admin.site.register(POI)
