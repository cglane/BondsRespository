from powers.models import Powers, SuretyCompany
import datetime
from django.conf import settings


def create_powers_batch():
    surety = SuretyCompany.objects.all()
    future_date = datetime.datetime.now() + datetime.timedelta(getattr(settings, 'POWERS_EXPIRATION'))
    for ptype in getattr(settings, 'POWERS_TYPES'):
        p_dict = {'powers_type': ptype[0], 'surety_company': surety[0], 'end_date_field': future_date}
        power = Powers(**p_dict)
        power.save()

def create_powers_batch_custom(number, type):
    surety = SuretyCompany.objects.all()
    future_date = datetime.datetime.now() + datetime.timedelta(getattr(settings, 'POWERS_EXPIRATION'))

    for iter in range(int(number)):
        p_dict = {'powers_type': type, 'surety_company': surety[0], 'end_date_field': future_date}
        power = Powers(**p_dict)
        power.save()