from rest_framework import serializers


class DailyStockMovementSerializer(serializers.Serializer):
    gainers = serializers.DictField()
    losers = serializers.DictField()
    active = serializers.DictField()
