from django.urls import path
from .views import talleres_disponibles
from .views import crear_taller_web
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import registro
urlpatterns = [
    path('', talleres_disponibles, name='talleres_disponibles'),
    path('crear/', crear_taller_web, name='crear_taller_web'),
    path('listado/', talleres_disponibles, name = 'listado'),
    path('login/', auth_views.LoginView.as_view(template_name='talleres/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='talleres_disponibles'), name='logout'),
    path('register/', registro, name='register'),
]

