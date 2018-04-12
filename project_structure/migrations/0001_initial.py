# Generated by Django 2.0.3 on 2018-04-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('degree', models.CharField(choices=[('Ph.D.', 'Ph.D.'), ('M.S.', 'M.S.'), ('M.A.', 'M.A.'), ('B.S.', 'B.S.'), ('B.A.', 'B.A.')], max_length=100)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='researchers',
            field=models.ManyToManyField(to='project_structure.Researcher'),
        ),
    ]
