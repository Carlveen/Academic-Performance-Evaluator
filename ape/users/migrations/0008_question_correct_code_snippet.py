# Generated by Django 4.1.3 on 2023-04-15 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_choice_code_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_code_snippet',
            field=models.TextField(blank=True, null=True),
        ),
    ]