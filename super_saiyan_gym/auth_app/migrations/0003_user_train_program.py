# Generated by Django 4.1 on 2022-08-24 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('auth_app', '0002_alter_user_options_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='train_program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user', to='main.trainingprogram', verbose_name='Тренировочная программа'),
        ),
    ]