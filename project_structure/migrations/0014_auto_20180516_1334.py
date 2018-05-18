# Generated by Django 2.0.3 on 2018-05-16 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_structure', '0013_auto_20180515_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Misc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='researcher',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publication',
            name='prepared_by',
            field=models.ManyToManyField(related_name='publication_prepared_by', to='project_structure.Researcher'),
        ),
        migrations.AddField(
            model_name='publication',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
        ),
        migrations.AddField(
            model_name='misc',
            name='prepared_by',
            field=models.ManyToManyField(related_name='misc_prepared_by', to='project_structure.Researcher'),
        ),
        migrations.AddField(
            model_name='misc',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
        ),
        migrations.AddField(
            model_name='data',
            name='prepared_by',
            field=models.ManyToManyField(related_name='data_prepared_by', to='project_structure.Researcher'),
        ),
        migrations.AddField(
            model_name='data',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='prepared_by',
            field=models.ManyToManyField(related_name='analysis_prepared_by', to='project_structure.Researcher'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_structure.Project'),
        ),
    ]