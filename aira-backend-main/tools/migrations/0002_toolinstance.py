# Generated by Django 5.0.6 on 2024-07-04 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.JSONField(blank=True, default=dict)),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.tool')),
            ],
        ),
    ]
