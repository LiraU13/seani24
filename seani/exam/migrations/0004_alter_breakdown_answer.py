# Generated by Django 5.0.2 on 2024-03-13 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_alter_exam_options_exam_created_exam_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breakdown',
            name='answer',
            field=models.CharField(default=True, max_length=5, verbose_name='Respuesta'),
        ),
    ]