from rest_framework import serializers


class DailyStockMoversSerializer(serializers.Serializer):
    gainers = serializers.DictField()
    losers = serializers.DictField()
    active = serializers.DictField()
