# Generated by Django 2.0.3 on 2018-04-06 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_structure', '0008_auto_20180406_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
        ),
    ]
