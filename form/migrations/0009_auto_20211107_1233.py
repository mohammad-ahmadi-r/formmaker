# Generated by Django 3.2.4 on 2021-11-07 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0008_responsequestion_uname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsequestion',
            name='uname',
        ),
        migrations.AddField(
            model_name='response',
            name='uname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]