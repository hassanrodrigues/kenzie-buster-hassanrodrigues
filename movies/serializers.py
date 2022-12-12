from rest_framework import serializers
from .models import Movie, MovieOrder
from .models import RatingChoice


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(
        choices=RatingChoice.choices, default=RatingChoice.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, obj) -> str:
        user = obj.user.email
        return user

    def create(self, validated_data) -> Movie:
        movie = Movie.objects.create(**validated_data)
        return movie


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(read_only=True)
    buyed_by = serializers.SerializerMethodField(read_only=True)

    def get_buyed_by(self, obj) -> str:
        return obj.user_order.email

    def get_title(self, obj) -> str:
        return obj.movie_order.title

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)
