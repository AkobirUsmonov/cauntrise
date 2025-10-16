from django.db import models


class Region(models.Model):
    """Masalan: Asia, Europe, Africa"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    """Davlatlarda ishlatiladigan tillar"""
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)      # davlat nomi
    capital = models.CharField(max_length=100)   # poytaxti
    population = models.IntegerField()           # aholi soni
    area = models.BigIntegerField()              # yer maydoni (km2)
    flag = models.URLField()                     # bayroq rasmi

    # qo‘shimcha fieldlar
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, related_name="countries"
    )
    languages = models.ManyToManyField(Language, related_name="countries")
    currency = models.CharField(max_length=50, null=True, blank=True)  # valyuta
    gdp = models.BigIntegerField(null=True, blank=True)  # yalpi ichki mahsulot
    time_zone = models.CharField(max_length=50, null=True, blank=True)  # vaqt zonasi
    neighbors = models.ManyToManyField('self', blank=True)  # qo‘shni davlatlar


    # #  Yangi maydon — GeoJSON formatda saqlanadigan xarita ma’lumotlari
    # map_data = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.name
