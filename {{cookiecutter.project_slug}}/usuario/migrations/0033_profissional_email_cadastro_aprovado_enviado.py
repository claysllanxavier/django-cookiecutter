# Generated by Django 3.1.2 on 2021-02-14 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0032_auto_20210212_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='email_cadastro_aprovado_enviado',
            field=models.BooleanField(default=False),
        ),
    ]
