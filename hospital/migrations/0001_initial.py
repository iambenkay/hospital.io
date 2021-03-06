# Generated by Django 2.2.4 on 2019-09-06 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DrugStat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total', models.PositiveIntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drug_records', to='hospital.Drug')),
            ],
        ),
        migrations.CreateModel(
            name='LabStat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total', models.PositiveIntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('fee', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceStat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total', models.PositiveIntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_records', to='hospital.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ward_cost', models.PositiveIntegerField()),
                ('days_in_ward', models.PositiveSmallIntegerField()),
                ('consumables', models.PositiveIntegerField()),
                ('pharmacy_bag', models.BooleanField(default=True)),
                ('total', models.PositiveIntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('consultations', models.ManyToManyField(related_name='receipts', to='hospital.Consultation')),
                ('drugs', models.ManyToManyField(related_name='receipts', to='hospital.DrugStat')),
                ('services', models.ManyToManyField(related_name='receipts', to='hospital.ServiceStat')),
                ('tests', models.ManyToManyField(related_name='receipts', to='hospital.LabStat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='labstat',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_records', to='hospital.Test'),
        ),
    ]
