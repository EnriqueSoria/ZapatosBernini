from rest_framework import serializers, viewsets
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """ Serializer to map the Model instance into JSON format."""

    class Meta:
        model = Item
        fields = '__all__'


class ItemsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
