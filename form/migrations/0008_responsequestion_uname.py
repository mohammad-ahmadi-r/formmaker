# Generated by Django 3.2.4 on 2021-11-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0007_remove_response_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsequestion',
            name='uname',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
