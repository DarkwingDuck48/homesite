# Generated by Django 5.0 on 2024-01-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_auto_20240117_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cat_type',
        ),
        migrations.AddField(
            model_name='operation',
            name='operation_type',
            field=models.CharField(choices=[('Dr', 'Доход'), ('Cr', 'Расход')], default='Cr', max_length=2),
        ),
    ]
