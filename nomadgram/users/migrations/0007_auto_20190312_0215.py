# Generated by Django 2.0.13 on 2019-03-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190311_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('not-specified', 'Not specified')], max_length=80, null=True),
        ),
    ]