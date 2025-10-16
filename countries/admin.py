from django.contrib import admin
from .models import Country, Region, Language

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "capital", "population", "area", "region")
    search_fields = ("name", "capital")

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
