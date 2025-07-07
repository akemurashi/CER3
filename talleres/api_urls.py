from django.urls import path
from .views import ListaTalleresJuntaView, CrearTallerJuntaView

urlpatterns = [
    path('talleres/', ListaTalleresJuntaView.as_view()),
    path('talleres/crear/', CrearTallerJuntaView.as_view()),
    path('talleres/', ListaTalleresJuntaView.as_view(), name='api_talleres'),
]
