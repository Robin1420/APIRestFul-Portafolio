from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Certificados, DatosPersonales, Experiencias,
    Proyectos, RedesSociales, Skills, UsuariosAdmin
)
from .serializers import (
    CertificadosSerializer, DatosPersonalesSerializer, ExperienciasSerializer,
    ProyectosSerializer, RedesSocialesSerializer, SkillsSerializer, UsuariosAdminSerializer
)

class DatosPersonalesViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite gestionar los datos personales (CRUD completo).
    - Usuarios no autenticados: Solo lectura
    - Usuarios autenticados: CRUD completo
    """
    queryset = DatosPersonales.objects.all()
    serializer_class = DatosPersonalesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['nombre', 'profesion', 'email']
    
    def get_serializer_context(self):
        # Asegurarse de que el contexto de la solicitud esté disponible en el serializador
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class ExperienciasViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar las experiencias laborales.
    """
    queryset = Experiencias.objects.all()
    serializer_class = ExperienciasSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-fecha_inicio']


class CertificadosViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar los certificados.
    """
    queryset = Certificados.objects.all()
    serializer_class = CertificadosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-fecha']


class ProyectosViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar los proyectos.
    Filtra por defecto solo los proyectos visibles.
    """
    serializer_class = ProyectosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-fecha']
    search_fields = ['titulo', 'tecnologias']

    def get_queryset(self):
        queryset = Proyectos.objects.all()
        # Si no es un usuario autenticado, mostrar solo los visibles
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(visible=True)
        return queryset


class RedesSocialesViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar las redes sociales.
    Filtra por defecto solo las redes sociales visibles.
    """
    serializer_class = RedesSocialesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['plataforma']

    def get_queryset(self):
        queryset = RedesSociales.objects.all()
        # Si no es un usuario autenticado, mostrar solo los visibles
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(visible=True)
        return queryset


class SkillsViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar las habilidades.
    """
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['categoria', 'nombre']
    search_fields = ['nombre', 'categoria']


class UsuariosAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y gestionar los usuarios administradores.
    Solo accesible para usuarios autenticados.
    """
    queryset = UsuariosAdmin.objects.all()
    serializer_class = UsuariosAdminSerializer
    permission_classes = [permissions.IsAdminUser]  # Solo administradores pueden acceder
    http_method_names = ['get', 'post', 'head', 'options']  # No permitir eliminación ni actualización

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint para obtener los datos del usuario autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)