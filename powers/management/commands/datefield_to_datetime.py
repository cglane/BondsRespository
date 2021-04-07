from django.core.management.base import BaseCommand
from django.contrib.auth.models import (Group, Permission)
from django.contrib.contenttypes.models import ContentType
from powers.utils import create_powers_batch
from datetime import datetime
from django.core.files import File
import os
from datetime import date
from datetime import datetime

from powers.models import (
    SuretyCompany,
    Defendant,
    User,
    Powers,
    Bond,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    def handle(self, *args, **options):
        bonds = Bond.objects.all()
        for item in bonds:
            date_val = item.issuing_date
            if not date_val is None:
                item.issuing_datetime = datetime.combine(date_val, datetime.min.time())
            # item.save()
