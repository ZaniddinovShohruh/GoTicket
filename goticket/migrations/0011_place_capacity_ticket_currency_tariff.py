from django.db import migrations, models
import django.db.models.deletion
import goticket.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('goticket', '0010_ticket_category_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='capacity',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Arenadagi jami o‘rindiq soni, masalan 10000',
                verbose_name='Seat capacity',
            ),
        ),
        migrations.AddField(
            model_name='ticket',
            name='currency',
            field=models.CharField(
                choices=[('USD', 'Dollar ($)'), ('EUR', 'Euro (€)'), ('UZS', "So'm")],
                default='UZS',
                max_length=3,
                verbose_name='Currency',
            ),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price'),
        ),
        migrations.CreateModel(
            name='TicketTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('VIP', 'VIP'), ('Standart', 'Standart')], default='Standart', max_length=20, verbose_name='category')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price')),
                ('currency', models.CharField(choices=[('USD', 'Dollar ($)'), ('EUR', 'Euro (€)'), ('UZS', "So'm")], default='UZS', max_length=3, verbose_name='Currency')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to=goticket.models.limit_ticket_content_type, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Ticket tariff',
                'verbose_name_plural': 'Ticket tariffs',
            },
        ),
        migrations.AddConstraint(
            model_name='tickettariff',
            constraint=models.UniqueConstraint(fields=('content_type', 'object_id', 'category'), name='unique_event_tariff'),
        ),
    ]
