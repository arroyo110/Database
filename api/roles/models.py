from django.db import models
from api.base.base import BaseModel


class Modulo(BaseModel):
    """
    Modelo para definir los módulos del sistema
    """
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"


class Accion(BaseModel):
    """
    Modelo para definir las acciones disponibles en el sistema
    """
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"


class Permiso(BaseModel):
    """
    Modelo para definir permisos específicos por módulo y acción
    """
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    accion = models.ForeignKey(Accion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return f"{self.modulo.nombre} - {self.accion.nombre}"
    
    class Meta:
        unique_together = ('modulo', 'accion')
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"


class Rol(BaseModel):
    """
    Modelo para definir roles de usuario
    """
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    permisos = models.ManyToManyField(Permiso, through='RolHasPermiso', blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class RolHasPermiso(BaseModel):
    """
    Modelo intermedio para la relación muchos a muchos entre Rol y Permiso
    """
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('rol', 'permiso')
        verbose_name = "Rol - Permiso"
        verbose_name_plural = "Roles - Permisos"