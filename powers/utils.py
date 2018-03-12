from powers.models import Powers, SuretyCompany
import datetime
from django.conf import settings
POWERS_TYPES = (('5000.00', '5000.00'), ('15000.00', '15000.00'),
                ('25000.00', '25000.00'), ('50000.00', '50000.00'),
                ('100000.00', '100000.00'), ('150000.00', '150000.00'),
                ('250000.00', '250000.00'), ('500000.00', '500000.00'))


def create_powers_batch():
    surety = SuretyCompany.objects.all()
    future_date = datetime.datetime.now() + datetime.timedelta(getattr(settings, 'POWERS_EXPIRATION'))
    for ptype in POWERS_TYPES:
        p_dict = {'powers_type': ptype[0], 'surety_company': surety[0], 'end_date_field': future_date}
        power = Powers(**p_dict)
        power.save()