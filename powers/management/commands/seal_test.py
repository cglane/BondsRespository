from django.core.management.base import BaseCommand
from django.contrib.auth.models import (Group, Permission)
from django.contrib.contenttypes.models import ContentType
from powers.utils import create_powers_batch
from datetime import datetime
from django.core.files import File
import os

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
        surety = SuretyCompany.objects.all()[0]
        print (surety.seal, 'print')