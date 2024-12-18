# Generated by Django 5.1.3 on 2024-12-01 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('two_factor_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to='', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(null=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=199, null=True, verbose_name='Name'),
        ),
    ]
