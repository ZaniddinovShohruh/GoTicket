from django.db import migrations, models


def normalize_ticket_category(apps, schema_editor):
    Ticket = apps.get_model('goticket', 'Ticket')
    for ticket in Ticket.objects.all():
        value = (ticket.category or '').strip().lower()
        if value in ('vip',):
            ticket.category = 'VIP'
        else:
            ticket.category = 'Standart'
        ticket.save(update_fields=['category'])


class Migration(migrations.Migration):

    dependencies = [
        ('goticket', '0009_ticket_integrity'),
    ]

    operations = [
        migrations.RunPython(normalize_ticket_category, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(
                choices=[('VIP', 'VIP'), ('Standart', 'Standart')],
                default='Standart',
                max_length=20,
                verbose_name='category',
            ),
        ),
    ]
