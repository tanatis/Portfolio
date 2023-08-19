from django.contrib import admin

from portfolio.position.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'count', 'price', 'to_portfolio',)
