from django.db import models
from  django.contrib.auth.models import User
from career.models import Career
from library.models import Module, Question
# Create your models here.


class Stage (models.Model):
    stage = models.IntegerField(
        verbose_name = "Etapa",)
    application_date = models.DateField(
        verbose_name = "Fecha de aplicacion",
    )

    @property
    def year(self):
        return self.application_date.year
    @property
    def month(self):
        months = ['enero', 'febrero', 'marzo',
                 'abril', 'mayo', 'junio', 'julio',
                 'agosto', 'septiembre', 'octubre',
                 'noviembre', 'diciembre']
        return months[self.application_date.month -1 ]
    
    def _str_(self):
        return f"{self.stage} - {self.month }-{self.year}"
    
    class Meta:
        verbose_name = "etapa"
        verbose_name_plural = "etapas"

class Exam(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        verbose_name = "Usuario"
    )

    stage = models.ForeignKey(
        Stage, 
        on_delete = models.CASCADE,
        verbose_name = 'Etapa'

    )
    career = models.ForeignKey(
        Career,
        on_delete = models.CASCADE,
        verbose_name ='Carera'
        )
    
    modules  = models.ManyToManyField(
        Module,
        through='ExamModule',
        verbose_name ="Módulos"
        )
    
    questions = models.ManyToManyField(
        Question,
        through='Breakdown',
        verbose_name='Preguntas'
    )
    
    score = models.FloatField(
        verbose_name ="Calificacion",
        default = 0.0
    )
    created = models.DateTimeField(
        verbose_name = 'Fecha de creacion',
        auto_now_add =True
    )
    updated = models.DateTimeField(
        verbose_name = 'Fecha de actualizacion',
        auto_now =True
        )

    def set_modules(self):
        for module in Module.objects.all():
            self.modules.add(module)

    def set_questions(self):
        for module in self.modules.all():
            for question in Question.objects.filter(module=module):
             Breakdown.objects.create(
                 exam = self,
                 question = question,
                 correct = question.correct, 
            )  
        
    def compute_score(self):
        score = 0.0
        for exammodule in self.exammodule_set.all():
            score += exammodule.score
        if self.exammodule_set.all().count() != 0:
            self.score = score / self.exammodule_set.count()
        else:
            self.score = 0.0 
        self.save()
        
    def compute_score_by_module(self, m_id):
        score = 0.0
        questions = self.breakdown_set.filter(question__module_id=m_id)
        question_count = questions.count()

        if question_count > 0:
            for question in questions:
                if question.answer == question.correct:
                    score += 10
            total = score / question_count
            module = self.exammodule_set.get(module_id=m_id)
            module.score = total
            module.save()
        else:
            # Manejar el caso cuando no hay preguntas asociadas al módulo
            module = self.exammodule_set.get(module_id=m_id)
            module.score = 0.0
            module.save()

    def _str_(self):
        return f"{self.user} - {self.career}: {self.score}"
    
    class Meta:
        verbose_name = "examen"
        verbose_name_plural = "examenes"

class ExamModule(models.Model):


    exam = models.ForeignKey(
        Exam,
        on_delete= models.CASCADE,
        verbose_name= "Examen"
        )
    module = models.ForeignKey(
        Module,
        on_delete= models.CASCADE,
        verbose_name= "Módulo"
        )
    active = models.BooleanField(
        verbose_name= "Activo",
        default= True,
        )
    score = models.FloatField(
        verbose_name= "Calificación",
        default= 0.0
        )
    
    def _str_(self):
        return f"{self.module} - {self.score}"
    
class Breakdown(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete = models.CASCADE,
        verbose_name = "Examen"
    )
    question = models.ForeignKey(
        Question,
        on_delete =models.CASCADE,
        verbose_name='Pregunta'
    )
        
    answer = models.CharField(
        verbose_name =' Respuesta',
        max_length = 5,
        default = '-'
    )
    
    correct = models.CharField(


        verbose_name = 'Respuesta correcta',
        max_length = 5,
        default = '-'
    )

    def _str_(self):
        return f"{self.question} - {self.answer}: {self.correct}"