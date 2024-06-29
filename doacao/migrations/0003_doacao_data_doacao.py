# Generated by Django 5.0.6 on 2024-06-29 16:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doacao", "0002_alter_customuser_cpf"),
    ]

    operations = [
        migrations.AddField(
            model_name="doacao",
            name="data_doacao",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]