from django.db import models
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from django.core.exceptions import ValidationError

class Novedad(models.Model):
    ESTADO_CHOICES = [
        ('normal', 'Normal'),
        ('tardanza', 'Tardanza'),
        ('ausente', 'Ausente'),
        ('vacaciones', 'Vacaciones'),
        ('incapacidad', 'Incapacidad'),
        ('horario', 'Horario'),
        ('anulada', 'Anulada'),
    ]
    
    TURNO_CHOICES = [
        ('apertura', 'Apertura (10:00 - 19:00)'),
        ('cierre', 'Cierre (11:00 - 20:00)'),
    ]

    TIPO_AUSENCIA_CHOICES = [
        ('completa', 'Día Completo'),
        ('por_horas', 'Por Horas'),
    ]

    # Horario base de trabajo (ej. 10 AM - 8 PM)
    HORA_ENTRADA_BASE = time(10, 0)
    HORA_SALIDA_BASE = time(20, 0)
    HORA_MIN_PERMITIDA = time(8, 0) # Para validaciones de entrada/salida
    HORA_MAX_PERMITIDA = time(22, 0) # Para validaciones de entrada/salida

    manicurista = models.ForeignKey('manicuristas.Manicurista', on_delete=models.CASCADE, related_name='novedades')
    fecha = models.DateField(default=timezone.localdate)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='normal')
    
    # Campos para estado 'tardanza'
    hora_entrada = models.TimeField(null=True, blank=True)
    
    # Horarios (para turnos)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, null=True, blank=True)
    
    # Para incapacidad
    archivo_soporte = models.FileField(upload_to="incapacidades/", null=True, blank=True)

    # Para vacaciones
    dias = models.PositiveIntegerField(null=True, blank=True)
    
    # Campos para estado 'ausente'
    tipo_ausencia = models.CharField(max_length=20, choices=TIPO_AUSENCIA_CHOICES, null=True, blank=True)
    hora_inicio_ausencia = models.TimeField(null=True, blank=True)
    hora_fin_ausencia = models.TimeField(null=True, blank=True)
    
    observaciones = models.TextField(blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    
    # Campos para estado 'anulada'
    motivo_anulacion = models.TextField(blank=True, null=True)
    fecha_anulacion = models.DateTimeField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"
        unique_together = [['manicurista', 'fecha']] # Una novedad por manicurista por día
        ordering = ['-fecha', 'manicurista__nombre'] # Corregido a 'manicurista__nombre'

    def __str__(self):
        return f"Novedad de {self.manicurista.nombre} el {self.fecha} - Estado: {self.get_estado_display()}"

    def clean(self):
        # Validaciones adicionales que no dependen de otros modelos
        if self.estado == 'tardanza':
            if not self.hora_entrada:
                raise ValidationError({'hora_entrada': 'La hora de entrada es requerida para el estado "Tardanza".'})
            if self.tipo_ausencia or self.hora_inicio_ausencia or self.hora_fin_ausencia:
                raise ValidationError('Los campos de ausencia no deben especificarse para el estado "Tardanza".')
                
        elif self.estado == 'ausente':
            if not self.tipo_ausencia:
                raise ValidationError({'tipo_ausencia': 'El tipo de ausencia es requerido para el estado "Ausente".'})
            if self.tipo_ausencia == 'por_horas':
                if not self.hora_inicio_ausencia or not self.hora_fin_ausencia:
                    raise ValidationError('Las horas de inicio y fin de ausencia son requeridas para el tipo "Por Horas".')
                if self.hora_inicio_ausencia >= self.hora_fin_ausencia:
                    raise ValidationError('La hora de inicio de ausencia debe ser anterior a la hora de fin.')
            elif self.tipo_ausencia == 'completa':
                if self.hora_inicio_ausencia or self.hora_fin_ausencia:
                    raise ValidationError('Las horas de inicio y fin de ausencia no deben especificarse para el tipo "Día Completo".')
            if self.hora_entrada:
                raise ValidationError('La hora de entrada no debe especificarse para el estado "Ausente".')
                
        elif self.estado == 'vacaciones':
            if not self.dias or self.dias < 7:
                raise ValidationError({'dias': 'Las vacaciones deben ser mínimo de 7 días.'})
            if self.dias % 7 != 0:
                raise ValidationError({'dias': 'Las vacaciones deben tomarse en semanas completas (múltiplos de 7).'})
                
        elif self.estado == 'incapacidad':
            if not self.archivo_soporte:
                raise ValidationError({'archivo_soporte': 'Debes adjuntar el soporte de la incapacidad.'})
                
        elif self.estado == 'horario':
            if not self.turno:
                raise ValidationError({'turno': 'Debes seleccionar un turno (apertura o cierre).'})
            if Novedad.objects.filter(
                manicurista=self.manicurista,
                fecha=self.fecha,
                estado='horario'
            ).exclude(pk=self.pk).exists():
                raise ValidationError({'turno': 'Ya existe un turno asignado a esta manicurista en esa fecha.'})
                
        else: # 'normal' o 'anulada'
            if self.hora_entrada or self.tipo_ausencia or self.hora_inicio_ausencia or self.hora_fin_ausencia:
                raise ValidationError('No se deben especificar campos de tardanza o ausencia para el estado "Normal" o "Anulada".')

        # Validaciones de rango de horas
        if self.hora_entrada and not (self.HORA_MIN_PERMITIDA <= self.hora_entrada <= self.HORA_MAX_PERMITIDA):
            raise ValidationError(
                f"La hora de entrada debe estar entre {self.HORA_MIN_PERMITIDA.strftime('%H:%M')} "
                f"y {self.HORA_MAX_PERMITIDA.strftime('%H:%M')}."
            )
        if self.hora_inicio_ausencia and not (self.HORA_MIN_PERMITIDA <= self.hora_inicio_ausencia <= self.HORA_MAX_PERMITIDA):
            raise ValidationError(
                f"La hora de inicio de ausencia debe estar entre {self.HORA_MIN_PERMITIDA.strftime('%H:%M')} "
                f"y {self.HORA_MAX_PERMITIDA.strftime('%H:%M')}."
            )
        if self.hora_fin_ausencia and not (self.HORA_MIN_PERMITIDA <= self.hora_fin_ausencia <= self.HORA_MAX_PERMITIDA):
            raise ValidationError(
                f"La hora de fin de ausencia debe estar entre {self.HORA_MIN_PERMITIDA.strftime('%H:%M')} "
                f"y {self.HORA_MAX_PERMITIDA.strftime('%H:%M')}."
            )


    def save(self, *args, **kwargs):
        self.full_clean() # Ejecuta las validaciones definidas en clean()
        super().save(*args, **kwargs)
