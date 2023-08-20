from django.urls import path

from portfolio.position.views import create_position, add_to_position

urlpatterns = [
    path('<int:pk>/create/', create_position, name='create_position'),
    path('<int:pk>/add/', add_to_position, name='add_to_position'),
]
