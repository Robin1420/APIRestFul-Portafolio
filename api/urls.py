from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'datos-personales', views.DatosPersonalesViewSet, basename='datos-personales')
router.register(r'experiencias', views.ExperienciasViewSet, basename='experiencias')
router.register(r'certificados', views.CertificadosViewSet, basename='certificados')
router.register(r'proyectos', views.ProyectosViewSet, basename='proyectos')
router.register(r'redes-sociales', views.RedesSocialesViewSet, basename='redes-sociales')
router.register(r'skills', views.SkillsViewSet, basename='skills')
router.register(r'usuarios-admin', views.UsuariosAdminViewSet, basename='usuarios-admin')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # Add login URLs for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]