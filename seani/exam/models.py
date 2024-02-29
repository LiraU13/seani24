from django.db import models
from django.contrib.auth.models import User
from  career.models import Career
from library.models import Module

class Stage(models.Model):

    stage = models.IntegerField(
        verbose_name= "Etapa",)
    
    application_date = models.DateField(
        verbose_name= "Fecha de aplicación",)

    @property
    def year(self):
        return self.application_date.year

    @property
    def month(self):
        months = ['enero', 'febrero', 'marzo', 'abril','mayo', 
            'junio','julio','agosto','septiembre',
            'ocutubre','noviembre','diciembre']
        return months[self.application_date.month - 1]

    def __str__(self):
        return f"{ self.stage } - { self.month } - { self.year }"
    
    class Meta:
        verbose_name = "etapa"
        verbose_name_plural = "etapas"
        
class Exam(models.Model):
    user = models.OneToOneField(
            User,
            on_delete = models.CASCADE,
            verbose_name = 'Usuario'
        )
    stage = models.ForeignKey(
            Stage,
            on_delete = models.CASCADE,
            verbose_name = 'Etapa'        
        )
    career = models.ForeignKey(
            Career,
            on_delete = models.CASCADE,
            verbose_name = 'Carrera'
        )
    modules = models.ManyToManyField(
            Module,
            through = 'ExamModule',
            verbose_name = 'Módulos'
        )
    score = models.FloatField(
            verbose_name = 'Calificación',
            default = 0.0
        )

class ExamModule(models.Model):
    exam = models.ForeignKey(
            Exam,
            on_delete = models.CASCADE,
            verbose_name = 'Examen'
        )
    module = models.ForeignKey(
            Module,
            on_delete = models.CASCADE,
            verbose_name = 'Módulo'
        )
    active = models.BooleanField(
            verbose_name = 'Activo',
            default = True
        )
    score = models.FloatField(
            verbose_name = 'Calificación',
            default = 0.0
        )        