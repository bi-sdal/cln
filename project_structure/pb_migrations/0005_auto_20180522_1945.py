# Generated by Django 2.0.3 on 2018-05-22 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications_bootstrap', '0004_catalog_fk_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications_bootstrap.Type'),
        ),
    ]