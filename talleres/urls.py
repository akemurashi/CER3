from django.urls import path
from .views import talleres_disponibles
from .views import crear_taller_web
urlpatterns = [
    path('', talleres_disponibles, name='talleres_disponibles'),
    path('crear/', crear_taller_web, name='crear_taller_web'),
]

