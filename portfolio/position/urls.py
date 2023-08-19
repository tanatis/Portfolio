from django.urls import path

from portfolio.position.views import add_position

urlpatterns = [
    path('add/<int:pk>/', add_position, name='add_position')
]
