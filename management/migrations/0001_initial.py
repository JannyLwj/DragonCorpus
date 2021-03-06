# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-12 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rrt_audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_path', models.CharField(max_length=255, verbose_name='audio_path')),
                ('audio_hrl_path', models.CharField(max_length=255, verbose_name='audio_hrl_path')),
                ('speaker', models.CharField(max_length=255, verbose_name='speaker')),
                ('gender', models.CharField(max_length=255, verbose_name='gender')),
                ('age', models.IntegerField(default=18, verbose_name='age')),
                ('format', models.CharField(default=256, max_length=255, verbose_name='format')),
                ('language', models.CharField(default='CMN', max_length=255, verbose_name='language')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_baseline_test_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_priority', models.IntegerField(default=0, verbose_name='baseline_case_priority')),
                ('select_times', models.IntegerField(default=0, verbose_name='baseline_select_times')),
                ('select_flag', models.BooleanField(default=False, verbose_name='baseline_select_flag')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=255, verbose_name='domain_name')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_intent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent_name', models.CharField(max_length=255, verbose_name='intent_name')),
                ('default_select_utterance', models.IntegerField(default=10, verbose_name='max_select_utterance')),
                ('intent_priority', models.IntegerField(default=1, verbose_name='min_select_utterance')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255, verbose_name='project_name')),
                ('project_description', models.TextField(verbose_name='project_description')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create_time')),
                ('modify_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='modify_time')),
                ('creater', models.CharField(default='admin', max_length=255, verbose_name='creater')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_project_running_test_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.UUIDField(verbose_name='log_id')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='running_testcase_create_time')),
                ('baseline_test_case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_baseline_test_case')),
                ('domain_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_domain')),
                ('intent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_intent')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_project')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_project_test_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_priority', models.IntegerField(default=0, verbose_name='case_priority')),
                ('select_times', models.IntegerField(default=0, verbose_name='select_times')),
                ('select_flag', models.BooleanField(default=False, verbose_name='select flag')),
                ('audio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_audio')),
                ('domain_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_domain')),
                ('intent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_intent')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_project')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_names', models.CharField(max_length=255, verbose_name='slot_names')),
                ('slot_values', models.CharField(max_length=255, verbose_name='slot_values')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_testsuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testsuit_name', models.CharField(max_length=255, verbose_name='testsuit_name')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_testsuit_testcase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_project_test_case')),
                ('testsuit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_testsuit')),
            ],
        ),
        migrations.CreateModel(
            name='rrt_utterance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utterance', models.CharField(max_length=255, verbose_name='utterance')),
                ('source', models.CharField(default='QA', max_length=255, verbose_name='source')),
                ('dialog', models.CharField(default='default', max_length=255, verbose_name='dialog')),
                ('gloable_priority', models.IntegerField(default=0, verbose_name='gloable_priority')),
            ],
        ),
        migrations.AddField(
            model_name='rrt_project_test_case',
            name='slot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_slot'),
        ),
        migrations.AddField(
            model_name='rrt_project_test_case',
            name='utterance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_utterance'),
        ),
        migrations.AddField(
            model_name='rrt_project_running_test_case',
            name='testsuit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_testsuit'),
        ),
        migrations.AddField(
            model_name='rrt_project_running_test_case',
            name='utterance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_utterance'),
        ),
        migrations.AddField(
            model_name='rrt_baseline_test_case',
            name='project_test_case_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_project_test_case'),
        ),
        migrations.AddField(
            model_name='rrt_baseline_test_case',
            name='utterance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_utterance'),
        ),
        migrations.AddField(
            model_name='rrt_audio',
            name='utterance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.rrt_utterance'),
        ),
    ]
