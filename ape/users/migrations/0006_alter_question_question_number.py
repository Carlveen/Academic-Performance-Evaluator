# Generated by Django 4.1.3 on 2023-04-14 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230414_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_number',
            field=models.IntegerField(default=0),
        ),
    ]