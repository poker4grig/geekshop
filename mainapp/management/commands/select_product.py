from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db import connection
from django.db.models import Q
from admins.views import db_profile_by_type




