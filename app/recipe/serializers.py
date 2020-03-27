from rest_framework import serializers

from core.models import Tag, Ingridient


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
