from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Sistema de autenticación unificado
    path('auth/', include('api.authentication.urls')),
    
    # Refresh token JWT
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # APIs existentes
    path('usuarios/', include('api.usuarios.urls')),
    path('clientes/', include('api.clientes.urls')),
    path('manicuristas/', include('api.manicuristas.urls')),
    path('roles/', include('api.roles.urls')),
    path('codigorecuperacion/', include('api.codigorecuperacion.urls')),
    
    # Restaurar todas las URLs que faltaban
    path('abastecimientos/', include('api.abastecimientos.urls')),
    path('categoria-insumos/', include('api.categoriainsumos.urls')),
    path('citas/', include('api.citas.urls')),
    path('compras/', include('api.compras.urls')),
    path('compra-insumo/', include('api.comprahasinsumos.urls')),
    path('insumos/', include('api.insumos.urls')),
    path('insumo-abastecimiento/', include('api.insumoshasabastecimientos.urls')),
    path('liquidaciones/', include('api.liquidaciones.urls')),
    path('novedades/', include('api.novedades.urls')),
    path('proveedores/', include('api.proveedores.urls')),
    path('servicios/', include('api.servicios.urls')),
    path('venta-servicios/', include('api.ventaservicios.urls')),
]