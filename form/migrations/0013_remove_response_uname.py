# Generated by Django 3.2.4 on 2021-11-07 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0012_alter_response_uname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='uname',
        ),
    ]