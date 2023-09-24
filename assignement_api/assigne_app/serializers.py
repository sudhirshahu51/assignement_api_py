from rest_framework import serializers

class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    population = serializers.IntegerField()
    area = serializers.FloatField()
    language = serializers.CharField()
    # Add other fields as needed
