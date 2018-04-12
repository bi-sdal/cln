# Generated by Django 2.0.3 on 2018-04-03 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_structure', '0003_auto_20180403_0235'),
        ('projects', '0004_projectcoderepositoriespage_projectdashboardpage_projectmeetingpage_projectpeoplepage_projectupdates'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpeoplepage',
            name='project_structure',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectsindexpage',
            name='project_structure',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
            preserve_default=False,
        ),
    ]
