# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from django.contrib.admin.apps import AdminConfig


class CustomAdminConfig(AdminConfig):
    default_site = 'custom_admin.CustomAdminSite'

class AppConfig(AppConfig):
    name = 'powers'
