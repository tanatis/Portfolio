from django.contrib import admin

from portfolio.position.models import Position, PositionHistory


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'count', 'price', 'to_portfolio',)


# @admin.register(PositionHistory)
# class PositionHistoryAdmin(admin.ModelAdmin):
#     list_display = ('to_position', 'count', 'price',)
