# Generated by Django 5.0.6 on 2024-06-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doacao", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="cpf",
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
