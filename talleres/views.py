from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Taller
from .serializers import TallerSerializer, CrearTallerSerializer
from .utils import es_feriado_irrenunciable
from datetime import date
from rest_framework.response import Response

class ListaTalleresJuntaView(generics.ListAPIView):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CrearTallerJuntaView(generics.CreateAPIView):
    queryset = Taller.objects.all()
    serializer_class = CrearTallerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        taller = serializer.save(creado_por=self.request.user)
        
        if es_feriado_irrenunciable(taller.fecha):
            taller.estado = 'rechazado'
            taller.observacion = "No se programan talleres en feriados irrenunciables"
        elif taller.fecha.weekday() == 6:
            taller.estado = 'rechazado'
            taller.observacion = "No se programan talleres en domingo"
        else:
            if taller.categoria.nombre != "Aire Libre":
                taller.estado = 'rechazado'
                taller.observacion = "Sólo se programan talleres al aire libre en feriados"
        taller.save()