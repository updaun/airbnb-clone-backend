from rest_framework import serializers


class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.CharField(
        max_length=15,
    )
    created_at = serializers.DateTimeField()
