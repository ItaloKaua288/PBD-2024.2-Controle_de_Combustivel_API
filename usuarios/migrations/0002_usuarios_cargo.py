# Generated by Django 5.1.3 on 2024-11-12 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='cargo',
            field=models.CharField(choices=[('A', 'Admnistrador'), ('M', 'Motorista')], default='M', max_length=1),
        ),
    ]
