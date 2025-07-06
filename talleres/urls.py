from django.urls import path
from .views import talleres_disponibles

urlpatterns = [
    path('', talleres_disponibles, name='talleres_disponibles'),
]
