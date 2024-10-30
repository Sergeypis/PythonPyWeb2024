from rest_framework import serializers
from apps.devdb2024.models import Route


class RouteSerializer(serializers.Serializer):
    route_id = serializers.IntegerField(read_only=True)
    depart = serializers.CharField(max_length=30)
    arrive = serializers.CharField(max_length=30)
    distance = serializers.IntegerField()
    trip_time = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Создать и вернуть новый объект Author на основе предоставленных проверенных данных.
        """
        return Route.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Обновить и вернуть существующий объект Author на основе предоставленных проверенных данных.
        """
        instance.depart = validated_data.get('depart', instance.depart)
        instance.arrive = validated_data.get('arrive', instance.arrive)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.trip_time = validated_data.get('trip_time', instance.trip_time)

        instance.save()
        return instance

class RouteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['depart']  # или можно прописать '__all__' если нужны все поля


