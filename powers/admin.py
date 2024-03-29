# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.utils.timezone import now, timedelta
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.conf.urls import include, url
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from powers.forms import (
    BondRequestVoidForm, TransferPowersForm,
    BondPrintForm, AgentForm,
    PowersBatchForm, BondVoidForm)
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from powers.utils import create_powers_batch_custom
import pytz
from django.shortcuts import render
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter
)
from powers.models import (
    SuretyCompany,
    Defendant,
    User,
    Powers,
    Bond,
    BondFile
)
from powers.custom_admin import custom_admin_site
from django.contrib.admin.actions import delete_selected as _delete_selected

local_tz = pytz.timezone('US/Eastern')

custom_admin_site.site_header = 'Shelmore Surety Admin'
custom_admin_site.index_title = 'Shelmore Surety Admin'
custom_admin_site.site_title = 'Shelmore Surety Admin'


class SuretyAdmin(admin.ModelAdmin):
    pass


class BondFileInline(admin.TabularInline):
    model = BondFile


class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super(GroupAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)


class BondInlineAdmin(admin.TabularInline):
    fields = ('amount', 'premium', 'related_court', 'offenses',
              'warrant_number', 'state', 'city', 'county', 'agent', 'powers',
              'has_been_printed')
    readonly_fields = ('amount', 'premium', 'related_court', 'offenses',
                       'warrant_number', 'state', 'city', 'county', 'agent',
                       'powers', 'has_been_printed', 'issuing_datetime')
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
        else:
            self.fieldsets = (
                ('Personal info', {
                    'fields': ('first_name', 'last_name', 'email', 'password',
                               'avatar')
                }),
                ('Important dates', {
                    'fields': ('last_login', 'date_joined')
                }),
                ('Permissions', {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
                }),
                ('Important Dates', {
                    'fields': ('last_login', 'date_joined')
                }),
            )
        return super(AgentAdmin, self).get_form(request, obj, **kwargs)


class PowersAdmin(admin.ModelAdmin):
    readonly_fields = ('date_of_transmission', 'surety_company', 'powers_type')
    list_filter = ('end_date_field', 'powers_type', 'agent')

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        self.list_display = ()
        extra_context = extra_context or {}
        allow_bulk_create = False

        if request.user.username in getattr(settings, 'VOID_WHITELIST') \
                or request.user.email in getattr(settings, 'VOID_WHITELIST'):
            allow_bulk_create = True
        extra_context['allow_bulk_create'] = allow_bulk_create
        if request.user.is_superuser:
            self.list_display = (
                '__str__',
                'agent_name',
                'date_of_transmission',
                'end_date_field',
                'powers_actions',
                'currently_used',
            )
        else:
            ##Don't want to give actions to agents
            self.list_display = (
                '__str__',
                'end_date_field',
                'date_of_transmission',
                'powers_type',
                'powers_actions'
            )
            self.readonly_fields = ('date_of_transmission', 'surety_company',
                                    'agent', 'powers_type', 'end_date_field', )
        return super(PowersAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """
        Only want powers that have end date in future to appear
        """
        qs = super(PowersAdmin, self).get_queryset(request)
        # There seems to be a bug with list display where it isn't updated
        # without refreshing page
        if request.user.is_superuser:
            return qs.filter(end_date_field__gte=now())
        else:
            return qs.filter(agent_id=request.user.id, end_date_field__gte=now())

    def currently_used(self, instance):
        bond = Bond.objects.get(powers=instance.id)
        if bond:
            return bond
        return False

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
        if 'do_action' in request.POST:
            form = PowersBatchForm(request.POST)
            if form.is_valid():
                create_powers_batch_custom(request.POST['number'], request.POST['type'])
                self.message_user(request, 'Success')
                return redirect('/admin/powers/powers')
        else:
            form = PowersBatchForm()

        return render(request, 'admin/account/create_batch_form.html',
                      {'title': u'Create a Batch',
                       'form': form})

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
                    form.save(powers)
                except Exception as e:
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

    def transfer_group(self, request, queryset):
        if 'do_action' in request.POST:
            form = AgentForm(request.POST)
            if form.is_valid():
                agent = form.cleaned_data['agent']
                future_date = now() + timedelta(
                    getattr(settings, 'POWERS_EXPIRATION_TRANSFER'))
                updated = queryset.update(agent=agent,
                                          end_date_field=future_date,
                                          start_date_transmission = now()
                                          )
                self.message_user(request, 'Success')
                return
        else:
            form = AgentForm()

        return render(request, 'admin/account/powers_action_bulk.html',
            {'title': u'Choose an Agent',
             'objects': queryset,
             'form': form})

    actions = [transfer_group, ]


class BondAdmin(admin.ModelAdmin):
    inlines = [ BondFileInline,]
    search_fields = ('powers__powers_type',  'agent__first_name',
                     'agent__last_name', 'defendant__last_name', 'powers__id')
    list_filter = (
        ('status', DropdownFilter),
        ('has_been_printed', DropdownFilter),
    )

    class Media:
        js = ('js/base.js', )

    def save_model(self, request, obj, form, change):
        original_discharged_date = obj._original_discharged_date
        if change and obj.discharged_date and \
                (not original_discharged_date or original_discharged_date != obj.discharged_date):
            obj.discharged_user = request.user
        super().save_model(request, obj, form, change)

    # Hide delete button on edit
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context={})

    # Make sure it is a soft delete for bond
    def delete_selected(self, request, queryset):
        def delete():
            for obj in queryset:
                self.delete_model(request, obj)

        queryset.delete = delete
        return _delete_selected(self, request, queryset)

    # Set deleted at date
    def delete_model(self, request, obj):
        obj.delete()

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if request.user.username not in getattr(settings, 'VOID_WHITELIST'):
            readonly_fields.append('voided')
        if not request.user.is_superuser:
            readonly_fields.append('has_been_printed')
            readonly_fields.append('discharged_user')
        return readonly_fields

    def changelist_view(self, request, **kwargs):
        self.list_display = ()
        if request.user.username in getattr(settings, 'VOID_WHITELIST'):
            self.list_display = ('__str__', 'agent', 'issuing_datetime', 'voided', 'status','has_been_printed',
                                 'bond_actions_one', 'make_voided', 'deleted_at', 'times_printed')
        elif request.user.is_superuser:
            self.list_display = ('__str__', 'agent', 'issuing_datetime', 'voided', 'status', 'has_been_printed',
                                 'bond_actions_one')
        else:
            self.list_display = ('__str__', 'issuing_datetime',
                                 'has_been_printed', 'status', 'bond_actions_one', 'bond_actions_two')
        return super(BondAdmin, self).changelist_view(request, **kwargs)

    def get_queryset(self, request):
        qs = super(BondAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(agent_id=request.user.id, deleted_at=None)
        else:
            return qs

    def get_form(self, request, obj=None, **kwargs):
        """
        Only want powers that have end date in future to appear
        """
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
                agent_id=request.user.id, bond__isnull=True, end_date_field__gte=now())
            form.base_fields['powers'].queryset = current_power | allowed_powers

            self.readonly_fields = ('has_been_printed', )
        else:

            current_power = Powers.objects.filter(id=powers_id)
            allowed_powers = Powers.objects.filter(
                bond__isnull=True, end_date_field__gte=now()
            )
            form.base_fields['powers'].queryset = current_power | allowed_powers
            self.readonly_fields = ('premium', )
        return form

    def get_urls(self):
        urls = super(BondAdmin, self).get_urls()

        custom_urls = [
            url(r'^(?P<bond_id>.+)/print/$',
                self.admin_site.admin_view(self.bond_print),
                name='bond_print'),
            url(r'^(?P<bond_id>.+)/bond_void_view/$',
                self.admin_site.admin_view(self.bond_void_view),
                name='bond_void_view'),
            url(r'^(?P<bond_id>.+)/request_void_bond/$',
                self.admin_site.admin_view(self.request_void_bond),
                name='request_void_bond'),
        ]

        return custom_urls + urls

    def make_voided(self, obj):
        if not obj.voided:
            return format_html('<a class="button" href="{}">Make Voided</a>',
                               reverse('admin:bond_void_view', args=[obj.pk]))

    def bond_void_view(self, request, bond_id, *args, **kwargs):
        bond = self.get_object(request, bond_id)
        if request.method != 'POST':
            form = BondVoidForm()
        else:
            form = BondVoidForm(request.POST)
            if form.is_valid():
                try:
                    form.save(bond, request.user)
                except Exception as e:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse('admin:powers_bond_changelist', )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['bond'] = bond
        context['title'] = 'Void Bond'

        return TemplateResponse(
            request,
            'admin/account/void_bond_action.html',
            context,
        )

    def bond_actions_one(self, obj):
        if not obj.has_been_printed or (obj.created_on > (now() - timedelta(hours=24)) and
                                        obj.times_printed < 3):
            return format_html('<a class="button" href="{}">Print Bond</a>',
                               reverse('admin:bond_print', args=[obj.pk]))

    bond_actions_one.short_description = 'Bond Print'
    bond_actions_one.all_tags = True

    def bond_actions_two(self, obj):
        if not obj.has_been_printed or (obj.created_on > (now() - timedelta(hours=24)) and
                                        obj.times_printed < 3):
            return format_html('<a class="button" href="{}">Request Void Bond</a>',
                               reverse('admin:request_void_bond', args=[obj.pk]))
    bond_actions_two.short_description = 'Request Void Bond'
    bond_actions_two.all_tags = True

    def request_void_bond(self, request, bond_id):
        bond = self.get_object(request, bond_id)
        if request.method != 'POST':
            form = BondRequestVoidForm()
        else:
            form = BondRequestVoidForm(request.POST)
            if form.is_valid():
                try:
                    form.save(bond, request.user)
                except Exception as e:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse('admin:powers_bond_changelist', )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['bond'] = bond
        context['title'] = 'Request Void Bond'

        return TemplateResponse(
            request,
            'admin/account/void_bond_action.html',
            context,
        )

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

    actions = [make_voided, delete_selected ]


custom_admin_site.register(SuretyCompany, SuretyAdmin)
custom_admin_site.register(Defendant, DefendantAdmin)
custom_admin_site.register(User, AgentAdmin)
custom_admin_site.register(Powers, PowersAdmin)
custom_admin_site.register(Bond, BondAdmin)
custom_admin_site.register(Group, GroupAdmin)