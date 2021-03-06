# Generated by Django 2.1.4 on 2019-02-15 15:09

from django.db import migrations, models
import django.utils.timezone


def convert_drives_to_int_bytes(apps, schema_editor):
    """Convert existing drive numbers from kbytes to bytes.

    This uses the binary system to scale, since that is what was used
    by machine checkin to convert from bytes initially.
    """
    Machine = apps.get_model('server', 'Machine')
    for machine in Machine.objects.all():
        # Django already converted str to int for us, but we cast back
        # to int just to be safe.
        if machine.hd_total:
            machine.hd_total = int(machine.hd_total * 1024.0)

        if machine.hd_space:
            machine.hd_space = int(machine.hd_space * 1024.0)

        machine.save()


def convert_drives_to_str_kbytes(apps, schema_editor):
    """Convert existing drive numbers from bytes kibibytes.

    This uses the binary system to scale, since that is what was used
    by machine checkin prior to this migration.
    """
    Machine = apps.get_model('server', 'Machine')
    for machine in Machine.objects.all():
        machine.hd_total = str(machine.hd_total / 1024.0)
        machine.hd_space = str(machine.hd_space / 1024.0)
        machine.save()


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0082_auto_20190204_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingupdate',
            name='machine',
        ),
        migrations.AlterModelOptions(
            name='manageditem',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='machine',
            name='hd_space',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hd_total',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.RunPython(convert_drives_to_int_bytes, convert_drives_to_str_kbytes),
        migrations.AlterField(
            model_name='manageditem',
            name='date_managed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='PendingUpdate',
        ),
    ]
