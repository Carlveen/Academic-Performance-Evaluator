# Generated by Django 4.1.3 on 2023-04-14 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_question_code_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]