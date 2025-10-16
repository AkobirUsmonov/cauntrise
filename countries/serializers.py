from rest_framework import serializers
from .models import Country, Region, Language


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]


class CountrySerializer(serializers.ModelSerializer):
    population_in_millions = serializers.SerializerMethodField()
    flag_url = serializers.SerializerMethodField()

    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source="region", write_only=True
    )
    languages = LanguageSerializer(many=True, read_only=True)
    language_ids = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, source="languages", write_only=True
    )
    neighbors = serializers.StringRelatedField(many=True, read_only=True)
    neighbor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), many=True, source="neighbors", write_only=True
    )

    class Meta:
        model = Country
        fields = [
            "id", "name", "capital", "population", "population_in_millions",
            "area", "flag", "flag_url", #"map_url",
            "region", "region_id",
            "languages", "language_ids",
            "currency", "gdp", "time_zone",
            "neighbors", "neighbor_ids",
        ]

    def get_population_in_millions(self, obj):
        return round(obj.population / 1_000_000, 2)

    def get_flag_url(self, obj):
        request = self.context.get("request")
        if request and obj.flag:
            return request.build_absolute_uri(obj.flag)
        return obj.flag
