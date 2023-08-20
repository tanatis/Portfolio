from django.contrib import admin

from portfolio.common.models import Ticker


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company_name']
