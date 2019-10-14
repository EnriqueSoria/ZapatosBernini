# Generated by Django 2.2.6 on 2019-10-14 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.PositiveSmallIntegerField(choices=[('36', 36), ('38', 38), ('40', 40), ('42', 42), ('44', 44), ('46', 46), ('48', 48)], default=42),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedidos.Item'),
        ),
    ]