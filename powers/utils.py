from powers.models import Powers, SuretyCompany, Bond
import datetime
from django.conf import settings
from powers.web_bot import BotException, BondStatus


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


def run_bond_status_bot(queryset):
    status_bot = BondStatus()
    for bond in queryset:
        try:
            warrant_bare = bond.warrant_number
            warrant_number = bond.warrant_number.split(' ')
            if warrant_number:
                status = status_bot.run_bot(bond.county, warrant_number)
                if status:
                    bond.status = status
                    bond.save()
        except BotException as e:
            bond.bot_error = str(e)
        except Exception as e:
            bond.bot_error = str(e)
    status_bot.quit()