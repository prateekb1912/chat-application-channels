# Generated by Django 4.1.5 on 2023-02-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_message_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlagQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_url', models.URLField()),
                ('correct_op', models.CharField(max_length=64)),
                ('incorrect_op1', models.CharField(max_length=64)),
                ('incorrect_op2', models.CharField(max_length=64)),
                ('incorrect_op3', models.CharField(max_length=64)),
            ],
        ),
    ]
