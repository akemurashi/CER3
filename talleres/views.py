from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .models import Taller, Profesor, Lugar, Categoria
from .utils import es_feriado_irrenunciable
from datetime import datetime
from django.views.generic import ListView
from rest_framework import generics, permissions
from .models import Taller, Categoria
from .serializers import TallerSerializer, CrearTallerSerializer
from .utils import es_feriado_irrenunciable
from datetime import date
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class ListaTalleresJuntaView(generics.ListAPIView):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required
def crear_taller_web(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        fecha = datetime.strptime(request.POST['fecha'], '%Y-%m-%d').date()
        duracion = float(request.POST['duracion_horas'])
        profesor = Profesor.objects.get(id=request.POST['profesor'])
        lugar = Lugar.objects.get(id=request.POST['lugar'])
        categoria = Categoria.objects.get(id=request.POST['categoria'])

        taller = Taller(
            titulo=titulo,
            fecha=fecha,
            duracion_horas=duracion,
            profesor=profesor,
            lugar=lugar,
            categoria=categoria,
            creado_por=request.user,
        )

        # Validación feriado
        if es_feriado_irrenunciable(fecha):
            taller.estado = 'rechazado'
            taller.observacion = "No se programan talleres en feriados irrenunciables"
        elif fecha.weekday() == 6:
            taller.estado = 'rechazado'
            taller.observacion = "No se programan talleres en domingo"
        else:
            if categoria.nombre != "Aire Libre":
                taller.estado = 'rechazado'
                taller.observacion = "Sólo se programan talleres al aire libre en feriados"
            else:
                taller.estado = 'pendiente'

        taller.save()

        return render(request, 'talleres/crear_taller.html', {
            'mensaje': 'Propuesta enviada correctamente',
            'profesores': Profesor.objects.all(),
            'lugares': Lugar.objects.all(),
            'categorias': Categoria.objects.all(),
        })

    return render(request, 'talleres/crear_taller.html', {
        'profesores': Profesor.objects.all(),
        'lugares': Lugar.objects.all(),
        'categorias': Categoria.objects.all(),
    })


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
            else:
                taller.estado = 'pendiente'
        taller.save()
    


def talleres_disponibles(request):
    categoria_id = request.GET.get('categoria')

    talleres = Taller.objects.filter(
        estado='aceptado',
        fecha__gt=date.today()
    )

    if categoria_id:
        talleres = talleres.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    
    return render(request, 'talleres/listado.html', {
        'talleres': talleres,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # opcional: iniciar sesión después de registrar
            return redirect('talleres_disponibles')
    else:
        form = UserCreationForm()
    
    return render(request, 'talleres/register.html', {'form': form})