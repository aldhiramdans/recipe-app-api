from rest_framework import serializers

from core.models import Tag, Ingridient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngridientSerializer(serializers.ModelSerializer):
    """Serializer for ingridient objects"""

    class Meta:
        model = Ingridient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    ingridient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingridient.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingridient', 'tag', 'time_minutes',
                  'price', 'link')
        read_only_fields = ('id',)
