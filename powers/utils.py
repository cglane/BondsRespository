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
            local_warrant_number = None
            if bond.warrant_number:
                if  "\n" in bond.warrant_number:
                    local_warrant_number = bond.warrant_number.split("\n")[0]
                elif "\t" in bond.warrant_number:
                    local_warrant_number = bond.warrant_number.split("\t")[0]
                elif " " in bond.warrant_number:
                    local_warrant_number = bond.warrant_number.split(" ")[0]
            if local_warrant_number:
                status = status_bot.run_bot(bond.county, local_warrant_number)
                # Note: Need to map status to the four options
                if status:
                    lower_status = status.lower()
                    if 'discharged' in lower_status or 'dismissed' in lower_status:
                        bond.status = 'Discharged'
                    elif 'failure to appear' in lower_status:
                        bond.status = 'FLTA'
                    else:
                        bond.status = 'Pending'
        except BotException as e:
            bond.bot_error = str(e)
        except Exception as e:
            bond.bot_error = str(e)
        bond.bot_last_run = datetime.datetime.now()
        bond.save()

    status_bot.quit()