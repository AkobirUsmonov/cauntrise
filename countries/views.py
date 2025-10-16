from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Country
from .serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):

    # Davlatlar API:
    # - Filtrlash: region, languages, neighbors
    # - Qidiruv: name, capital, region__name, languages__name
    # - Saralash: population, area, gdp, name


    queryset = Country.objects.all().select_related("region").prefetch_related("languages", "neighbors")
    serializer_class = CountrySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'languages', 'neighbors']
    search_fields = ['name', 'capital', 'region__name', 'languages__name']
    ordering_fields = ['population', 'area', 'gdp', 'name']
    ordering = ['name']
