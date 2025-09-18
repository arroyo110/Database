# EJEMPLOS DE VISTAS CON NUEVO SISTEMA DE PERMISOS
# Este archivo muestra cómo implementar el nuevo sistema de permisos en las vistas

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.authentication.decorators import require_permission, require_any_permission, require_all_permissions
from .models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSetConPermisos(viewsets.ModelViewSet):
    """
    Ejemplo de ViewSet con el nuevo sistema de permisos por acciones
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # LISTAR usuarios - requiere permiso 'usuarios_listar'
    @require_permission('usuarios_listar')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # CREAR usuario - requiere permiso 'usuarios_crear'
    @require_permission('usuarios_crear')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # VER DETALLES de usuario - requiere permiso 'usuarios_ver_detalles'
    @require_permission('usuarios_ver_detalles')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # EDITAR usuario - requiere permiso 'usuarios_editar'
    @require_permission('usuarios_editar')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # EDITAR usuario (parcial) - requiere permiso 'usuarios_editar'
    @require_permission('usuarios_editar')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ELIMINAR usuario - requiere permiso 'usuarios_eliminar'
    @require_permission('usuarios_eliminar')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ACCIÓN PERSONALIZADA - requiere cualquiera de los permisos especificados
    @action(detail=True, methods=['post'])
    @require_any_permission('usuarios_editar', 'usuarios_eliminar')
    def activar_desactivar(self, request, pk=None):
        """
        Activar o desactivar un usuario
        Requiere permiso de editar O eliminar
        """
        usuario = self.get_object()
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        return Response({
            'mensaje': f'Usuario {"activado" if usuario.is_active else "desactivado"} correctamente',
            'is_active': usuario.is_active
        })

    # ACCIÓN PERSONALIZADA - requiere todos los permisos especificados
    @action(detail=False, methods=['get'])
    @require_all_permissions('usuarios_listar', 'usuarios_ver_detalles')
    def estadisticas(self, request):
        """
        Obtener estadísticas de usuarios
        Requiere permisos de listar Y ver detalles
        """
        total_usuarios = self.get_queryset().count()
        usuarios_activos = self.get_queryset().filter(is_active=True).count()
        usuarios_inactivos = total_usuarios - usuarios_activos
        
        return Response({
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'usuarios_inactivos': usuarios_inactivos
        })

    # ACCIÓN PERSONALIZADA - sin decorador (usa middleware)
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """
        Buscar usuarios por nombre
        El middleware verificará automáticamente el permiso 'usuarios_listar'
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Se requiere el parámetro q'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        usuarios = self.get_queryset().filter(nombre__icontains=query)
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)


# EJEMPLO DE IMPLEMENTACIÓN EN VISTAS EXISTENTES
# Para actualizar tus vistas existentes, simplemente agrega los decoradores:

"""
# ANTES (sistema anterior):
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def list(self, request, *args, **kwargs):
        # El middleware verificaba 'gestionar_usuarios'
        return super().list(request, *args, **kwargs)

# DESPUÉS (nuevo sistema):
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    @require_permission('usuarios_listar')
    def list(self, request, *args, **kwargs):
        # Ahora verifica específicamente 'usuarios_listar'
        return super().list(request, *args, **kwargs)
    
    @require_permission('usuarios_crear')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @require_permission('usuarios_ver_detalles')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @require_permission('usuarios_editar')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @require_permission('usuarios_eliminar')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
"""

# EJEMPLO DE USO EN ACCIONES PERSONALIZADAS
"""
@action(detail=True, methods=['post'])
@require_permission('citas_crear')
def reprogramar_cita(self, request, pk=None):
    # Solo usuarios con permiso 'citas_crear' pueden reprogramar
    pass

@action(detail=False, methods=['get'])
@require_any_permission('citas_listar', 'citas_ver_detalles')
def citas_por_fecha(self, request):
    # Usuarios con permiso de listar O ver detalles pueden acceder
    pass

@action(detail=False, methods=['post'])
@require_all_permissions('usuarios_crear', 'usuarios_editar')
def crear_y_asignar_rol(self, request):
    # Requiere ambos permisos: crear Y editar usuarios
    pass
"""
