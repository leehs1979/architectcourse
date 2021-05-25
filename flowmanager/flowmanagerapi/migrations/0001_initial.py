# Generated by Django 3.2.3 on 2021-05-25 03:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('api_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='apiid')),
                ('api_nm', models.CharField(max_length=100)),
                ('api_desc', models.TextField(blank=True, max_length=500, null=True)),
                ('api_type', models.TextField(blank=True, max_length=100, null=True)),
                ('api_result_type', models.TextField(blank=True, max_length=100, null=True)),
                ('api_uri', models.TextField(blank=True, max_length=100, null=True)),
                ('api_provider', models.TextField(blank=True, max_length=100, null=True)),
                ('api_in_format', models.TextField(blank=True, max_length=100, null=True)),
                ('api_out_format', models.TextField(blank=True, max_length=100, null=True)),
                ('creator', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='FLOW',
            fields=[
                ('flow_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='flowpid')),
                ('flow_nm', models.CharField(max_length=100)),
                ('flow_desc', models.TextField(blank=True, max_length=500, null=True)),
                ('creator', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='FLOW_DTL',
            fields=[
                ('flow_dtl_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='flowdtlid')),
                ('api_seq', models.PositiveIntegerField(default=0)),
                ('api_timeout', models.PositiveIntegerField(default=10)),
                ('api_retry', models.PositiveIntegerField(default=3)),
                ('creator', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowmanagerapi.api')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowmanagerapi.flow')),
            ],
            options={
                'ordering': ['created'],
                'unique_together': {('flow', 'api', 'api_seq')},
            },
        ),
        migrations.CreateModel(
            name='FLOW_JOB',
            fields=[
                ('flow_job_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='jobid')),
                ('api_input', models.TextField(blank=True, max_length=1000, null=True)),
                ('api_output', models.TextField(blank=True, max_length=1000, null=True)),
                ('api_status', models.CharField(blank=True, max_length=50, null=True)),
                ('api_start_dt', models.DateTimeField(auto_now=True, verbose_name='start time')),
                ('api_end_dt', models.DateTimeField(auto_now=True, verbose_name='end time')),
                ('creator', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
                ('flow_dtl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowmanagerapi.flow_dtl')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
