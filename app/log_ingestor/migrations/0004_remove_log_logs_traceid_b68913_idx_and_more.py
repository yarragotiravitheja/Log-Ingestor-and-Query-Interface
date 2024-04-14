# Generated by Django 4.2.7 on 2023-11-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_ingestor', '0003_alter_loglevel_level_alter_logresource_resource'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='log',
            name='logs_traceId_b68913_idx',
        ),
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['traceId'], name='logs_traceId_f55bd4_idx'),
        ),
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['spanId'], name='logs_spanId_bdf9b0_idx'),
        ),
        migrations.AddIndex(
            model_name='log',
            index=models.Index(fields=['commit'], name='logs_commit_1d4f29_idx'),
        ),
    ]