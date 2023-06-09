# Generated by Django 4.1.7 on 2023-02-21 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('Amount', models.IntegerField()),
                ('Currency', models.CharField(max_length=3)),
                ('CustomerEmail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='SplitInfo',
            fields=[
                ('SplitType', models.CharField(choices=[('FLAT', 'FLAT'), ('PERCENTAGE', 'PERCENTAGE'), ('RATIO', 'RATIO')], max_length=50)),
                ('SplitValue', models.IntegerField()),
                ('SplitEntityId', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SplitInfo', to='app.transaction')),
            ],
        ),
    ]
