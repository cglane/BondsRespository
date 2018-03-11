from powers.models import Powers, SuretyCompany

POWERS_TYPES = (('5000.00', '5000.00'), ('15000.00', '15000.00'),
                ('25000.00', '25000.00'), ('50000.00', '50000.00'),
                ('100000.00', '100000.00'), ('150000.00', '150000.00'),
                ('250000.00', '250000.00'), ('500000.00', '500000.00'))


def create_powers_batch():
    surety = SuretyCompany.objects.all()
    for ptype in POWERS_TYPES:
        p_dict = {'powers_type': ptype[0], 'surety_company': surety[0]}
        power = Powers(**p_dict)
        power.save()