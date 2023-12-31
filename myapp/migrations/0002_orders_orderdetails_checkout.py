# Generated by Django 4.2.3 on 2023-12-16 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users')),
            ],
        ),
        migrations.CreateModel(
            name='orderdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.item')),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.orders')),
            ],
        ),
        migrations.CreateModel(
            name='checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.users')),
            ],
        ),
    ]
