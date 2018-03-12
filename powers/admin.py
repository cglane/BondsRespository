# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.conf.urls import include, url
from django.shortcuts import redirect
from itertools import chain

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from powers.forms import TransferPowersForm, BondPrintForm
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from powers.utils import create_powers_batch
import pytz

from powers.models import (
    SuretyCompany,
    Defendant,
    User,
    Powers,
    Bond,
)

local_tz = pytz.timezone('US/Eastern')

admin.site.site_header = 'Sinkler Bonding Admin'


class SuretyAdmin(admin.ModelAdmin):
    pass


class BondInlineAdmin(admin.TabularInline):
    fields = ('amount', 'premium', 'related_court', 'offences',
              'warrant_number', 'state', 'city', 'county', 'agent', 'powers',
              'has_been_printed')
    readonly_fields = ('amount', 'premium', 'related_court', 'offences',
                       'warrant_number', 'state', 'city', 'county', 'agent',
                       'powers', 'has_been_printed', 'issuing_date')
    model = Bond

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(BondInlineAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(agent_id=request.user.id)
        return qs


class DefendantAdmin(admin.ModelAdmin):
    inlines = [
        BondInlineAdmin,
    ]
    readonly_fields = ('created_on', )
    search_fields = ('first_name', 'last_name', 'id', )

    def get_queryset(self, request):
        qs = super(DefendantAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            agent = User.objects.filter(id=request.user.id)
            return qs.filter(agents__in=agent)


class AgentAdmin(UserAdmin):
    readonly_fields = [
        'last_login',
    ]

    def get_queryset(self, request):
        qs = super(AgentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(id=request.user.id)

    def get_form(self, request, obj=None, **kwargs):
        # Exclude fields from form creation
        if not request.user.is_superuser:
            self.fieldsets = (
                ('Personal info', {
                    'fields': ('first_name', 'last_name', 'email', 'password',
                               'avatar')
                }),
                ('Important dates', {
                    'fields': ('last_login', 'date_joined')
                }),
            )
        return super(AgentAdmin, self).get_form(request, obj, **kwargs)


class PowersAdmin(admin.ModelAdmin):
    readonly_fields = ('date_of_transmission', 'surety_company', 'powers_type')

    def get_queryset(self, request):
        qs = super(PowersAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            self.list_display = (
                '__str__',
                'agent_name',
                'date_of_transmission',
                'end_date_field',
                'powers_actions',
            )
            return qs.filter(end_date_field__gte=datetime.now())
        else:
            ##Don't want to give actions to agents
            self.list_display = (
                '__str__',
                'end_date_field',
            )
            self.readonly_fields = ('date_of_transmission', 'surety_company',
                                    'agent', 'powers_type', 'end_date_field')
        return qs.filter(agent_id=request.user.id, end_date_field__gte=datetime.now())

    def date_of_transmission(self, instance):
        if instance.start_date_transmission :
            local_dt = instance.start_date_transmission .replace(
                tzinfo=pytz.utc).astimezone(local_tz)
            return local_tz.normalize(local_dt).strftime(
                "%A %d. %B %Y %I:%M%p")

        return ''

    def agent_name(self, instance):
        if instance.agent:
            return instance.agent.first_name + ' ' + instance.agent.last_name
        return 'Not Defined'

    def get_urls(self):
        urls = super(PowersAdmin, self).get_urls()

        custom_urls = [
            url(r'^(?P<powers_id>.+)/transfer/$',
                self.admin_site.admin_view(self.powers_transfer),
                name='powers_transfer'),
            url(r'^create_batch/',
                self.admin_site.admin_view(self.create_batch),
                name="powers_batch")
        ]

        return custom_urls + urls

    def create_batch(self, request, *args, **kwargs):
        create_powers_batch()
        url = reverse('admin:powers_powers_changelist', )
        return HttpResponseRedirect(url)

    def powers_actions(self, obj):
        return format_html('<a class="button" href="{}">Transfer</a>',
                           reverse('admin:powers_transfer', args=[obj.pk]))

    powers_actions.short_description = 'Transfer Actions'
    powers_actions.all_tags = True

    def powers_transfer(self, request, powers_id, *args, **kwargs):
        powers = self.get_object(request, powers_id)
        if request.method != 'POST':
            form = TransferPowersForm()
        else:
            form = TransferPowersForm(request.POST)
            if form.is_valid():
                try:
                    form.save(powers, request.user)
                except:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse('admin:powers_powers_changelist', )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['powers'] = powers
        context['title'] = 'Powers Transfer'

        return TemplateResponse(
            request,
            'admin/account/powers_action.html',
            context,
        )





class BondAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'agent', 'issuing_date', 'has_been_printed',
                    'bond_actions')
    search_fields = ( 'powers__powers_type',  'agent__first_name')

    def get_queryset(self, request):
        qs = super(BondAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            self.list_display = ('__str__', 'issuing_date',
                                 'has_been_printed', 'bond_actions')
            return qs.filter(agent_id=request.user.id)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        # Exclude fields from form creation
        form = super(BondAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.powers:
            powers_id = obj.powers.id
        else:
            powers_id = None

        if not request.user.is_superuser:
            form.base_fields['agent'].queryset = User.objects.filter(
                id=request.user.id)
            current_power = Powers.objects.filter(id=powers_id)
            allowed_powers = Powers.objects.filter(
                agent_id=request.user.id, bond__isnull=True, end_date_field__gte=datetime.now())            
            form.base_fields['powers'].queryset = current_power | allowed_powers

            self.readonly_fields = ('has_been_printed', )
        else:
            current_power = Powers.objects.filter(id=powers_id)
            allowed_powers = Powers.objects.filter(
                bond__isnull=True, end_date_field__gte=datetime.now()
            )
            form.base_fields['powers'].queryset = current_power | allowed_powers

        return form


    def get_urls(self):
        urls = super(BondAdmin, self).get_urls()

        custom_urls = [
            url(r'^(?P<bond_id>.+)/print/$',
                self.admin_site.admin_view(self.bond_print),
                name='bond_print')
        ]

        return custom_urls + urls

    def bond_actions(self, obj):
        if not obj.has_been_printed:
            return format_html('<a class="button" href="{}">Print Bond</a>',
                               reverse('admin:bond_print', args=[obj.pk]))

    bond_actions.short_description = 'Bond Actions'
    bond_actions.all_tags = True

    def bond_print(self, request, bond_id, *args, **kwargs):
        bond = self.get_object(request, bond_id)
        if request.method != 'POST':
            form = BondPrintForm()
        else:
            form = BondPrintForm(request.POST)
            if form.is_valid():
                try:
                    form.save(bond, request.user)
                except:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse('admin:powers_bond_changelist', )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['bond'] = bond
        context['power'] = Powers.objects.get(id=bond.powers.id)
        context['surety_company'] = SuretyCompany.objects.all()[0]
        context['title'] = 'Print Bond'
        return TemplateResponse(
            request,
            'print/bond_print.html',
            context,
        )


admin.site.register(SuretyCompany, SuretyAdmin)
admin.site.register(Defendant, DefendantAdmin)
admin.site.register(User, AgentAdmin)
admin.site.register(Powers, PowersAdmin)
admin.site.register(Bond, BondAdmin)
