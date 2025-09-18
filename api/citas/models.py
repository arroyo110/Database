from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from api.base.base import BaseModel
from api.clientes.models import Cliente
from api.servicios.models import Servicio
from api.manicuristas.models import Manicurista
from api.novedades.models import Novedad # Importar el modelo Novedad
from datetime import datetime, time


class Cita(BaseModel):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
        ('cancelada_por_novedad', 'Cancelada por Novedad'), # Nuevo estado
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        verbose_name="Cliente"
    )
    
    manicurista = models.ForeignKey(
        Manicurista,
        on_delete=models.CASCADE,
        verbose_name="Manicurista"
    )
    
    # CAMBIADO: Ahora soporta múltiples servicios
    servicios = models.ManyToManyField(
        Servicio,
        verbose_name="Servicios",
        help_text="Servicios incluidos en la cita",
        blank=True  # Permitir vacío inicialmente
    )
    
    # MANTENER para compatibilidad con código existente
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        verbose_name="Servicio Principal",
        help_text="Servicio principal (para compatibilidad)",
        related_name="citas_principal"
    )
    
    fecha_cita = models.DateField(
        verbose_name="Fecha de la cita"
    )
    
    hora_cita = models.TimeField(
        verbose_name="Hora de la cita"
    )
    
    estado = models.CharField(
        max_length=30, # Aumentado de 20 a 30
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )

    motivo_cancelacion = models.TextField( # Nuevo campo
        blank=True,
        null=True,
        verbose_name="Motivo de Cancelación"
    )

    novedad_relacionada = models.ForeignKey( # Nuevo campo
        Novedad,
        on_delete=models.SET_NULL, # Si la novedad se elimina, no se elimina la cita
        null=True,
        blank=True,
        related_name='citas_afectadas',
        verbose_name="Novedad Relacionada"
    )
    
    # NUEVO: Precio total con valor por defecto
    precio_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio total de la cita",
        help_text="Precio total de todos los servicios",
        default=0  # Valor por defecto para evitar problemas de migración
    )
    
    # MANTENER para compatibilidad
    precio_servicio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio del servicio principal",
        help_text="Precio del servicio principal (para compatibilidad)"
    )
    
    # NUEVO: Duración total con valor por defecto
    duracion_total = models.PositiveIntegerField(
        verbose_name="Duración total (minutos)",
        help_text="Duración total de todos los servicios en minutos",
        default=0  # Valor por defecto para evitar problemas de migración
    )
    
    # MANTENER para compatibilidad
    duracion_estimada = models.PositiveIntegerField(
        verbose_name="Duración estimada (minutos)",
        help_text="Duración del servicio principal (para compatibilidad)"
    )
    
    fecha_finalizacion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de finalización"
    )

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha_cita', '-hora_cita']
        unique_together = ['manicurista', 'fecha_cita', 'hora_cita']

    def __str__(self):
        return f"Cita {self.cliente.nombre} - {self.fecha_cita} {self.hora_cita}"

    def clean(self):
        """Validaciones personalizadas"""
        # Validar que la fecha no sea en el pasado
        if self.fecha_cita and self.fecha_cita < datetime.now().date():
            raise ValidationError({'fecha_cita': 'La fecha de la cita no puede ser en el pasado'})
        
        # Validar horario de trabajo (10:00 AM - 8:00 PM)
        if self.hora_cita:
            # --- CAMBIO AQUÍ: Horario de 10:00 AM a 8:00 PM ---
            if self.hora_cita < time(10, 0) or self.hora_cita >= time(20, 0):
                raise ValidationError({'hora_cita': 'La hora debe estar entre 10:00 AM y 8:00 PM'})
        
        # Validar que la manicurista esté disponible
        if self.manicurista and self.manicurista.estado != 'activo':
            raise ValidationError({'manicurista': 'La manicurista seleccionada no está activa'})
        
        # Validar que el servicio principal esté activo
        if self.servicio and self.servicio.estado != 'activo':
            raise ValidationError({'servicio': 'El servicio seleccionado no está activo'})

    def save(self, *args, **kwargs):
        # Establecer precio y duración del servicio principal para compatibilidad
        if self.servicio:
            self.precio_servicio = self.servicio.precio
            self.duracion_estimada = self.servicio.duracion
            
            # Si no hay precio_total, usar el del servicio principal
            if self.precio_total == 0:
                self.precio_total = self.servicio.precio
            
            # Si no hay duracion_total, usar la del servicio principal
            if self.duracion_total == 0:
                self.duracion_total = self.servicio.duracion
        
        # Establecer fecha de finalización cuando se marca como finalizada
        if self.estado == 'finalizada' and not self.fecha_finalizacion:
            self.fecha_finalizacion = datetime.now()
        
        super().save(*args, **kwargs)

    def calcular_totales(self):
        """Calcular precio y duración total de todos los servicios"""
        servicios = self.servicios.all()
        if servicios.exists():
            self.precio_total = sum(servicio.precio for servicio in servicios)
            self.duracion_total = sum(servicio.duracion for servicio in servicios)
            
            # Mantener compatibilidad con campos individuales
            primer_servicio = servicios.first()
            if not self.servicio:
                self.servicio = primer_servicio
            self.precio_servicio = primer_servicio.precio
            self.duracion_estimada = primer_servicio.duracion
            
            self.save()
    
    def crear_ventas_automaticas(self):
        """Crear ventas automáticamente para todos los servicios cuando se finaliza una cita"""
        try:
            # Importar aquí para evitar importación circular
            from api.ventaservicios.models import VentaServicio, DetalleVentaServicio

            # Verificar que no exista ya una venta para esta cita
            if hasattr(VentaServicio, 'cita') and VentaServicio.objects.filter(
                cita=self
            ).exists():
                print(f"Ya existe una venta para la cita {self.id}")
                return

            # Crear una sola venta para toda la cita
            venta_data = {
                'cliente': self.cliente,
                'manicurista': self.manicurista,
                'cita': self,
                'cantidad': 1,
                'precio_unitario': self.precio_total,  # Usar precio total de la cita
                'total': self.precio_total,
                'fecha_venta': self.fecha_finalizacion or timezone.now(),
                'observaciones': f"Venta generada automáticamente desde cita #{self.id}",
                'estado': 'pendiente',
                'metodo_pago': 'efectivo'  # Método por defecto
            }

            # Crear la venta principal
            venta = VentaServicio.objects.create(**venta_data)
            
            # Crear detalles para cada servicio
            for servicio in self.servicios.all():
                detalle_data = {
                    'venta': venta,
                    'servicio': servicio,
                    'cantidad': 1,
                    'precio_unitario': servicio.precio,
                    'descuento_linea': 0,
                    'subtotal': servicio.precio
                }
                DetalleVentaServicio.objects.create(**detalle_data)
                print(f"Detalle creado para servicio {servicio.nombre} en venta {venta.id}")

            print(f"Venta {venta.id} creada automáticamente para cita {self.id} con {self.servicios.count()} servicios")

        except ImportError:
            print("Módulo de ventas no disponible")
        except Exception as e:
            print(f"Error creando ventas automáticas: {e}")
            raise

    @property
    def duracion_formateada(self):
        """Retorna la duración total en formato legible"""
        duracion = self.duracion_total if self.duracion_total > 0 else self.duracion_estimada
        if duracion < 60:
            return f"{duracion} min"
        else:
            horas = duracion // 60
            minutos = duracion % 60
            if minutos == 0:
                return f"{horas}h"
            else:
                return f"{horas}h {minutos}min"

    @property
    def puede_finalizar(self):
        """Verifica si la cita puede ser finalizada"""
        return self.estado in ['pendiente', 'en_proceso']

    @property
    def puede_cancelar(self):
        """Verifica si la cita puede ser cancelada"""
        return self.estado in ['pendiente', 'en_proceso']

    def get_servicios_info(self):
        """Obtener información de todos los servicios"""
        return self.servicios.all()
