# Generated by Django 3.2.4 on 2021-11-07 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0011_alter_response_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='uname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
