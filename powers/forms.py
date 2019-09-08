from django import forms
from powers.models import User, Powers, Bond
import datetime
from django.conf import settings


class DateInput(forms.DateInput):
    input_type = 'date'

class PowersBatchForm(forms.Form):
    number = forms.IntegerField()
    type = forms.ChoiceField(choices=getattr(settings, 'POWERS_TYPES'))

class AgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=User.objects.all())


class TransferPowersForm(forms.Form):
    agent = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True))

    def __init__(self, agent=None, *args, **kwargs):
        # For testing
        print(agent, 'agent')
        super(TransferPowersForm, self).__init__(*args, **kwargs)
        if agent:
            self.cleaned_data = {'agent': agent.id}


    def save(self, powers):
        try:
            self.form_action(powers)
            # Clear out low powers message
            agent_id = self.cleaned_data['agent']
            agent = User.objects.get(id=agent_id)
            agent.powers_low_message = ''
            agent.save()
        except:
            raise forms.ValidationError("Failed to save form.")

    def form_action(self, powers):
        power = Powers.objects.get(id=powers.id)
        power.agent_id = self.cleaned_data['agent']

        future_date = datetime.datetime.now() + datetime.timedelta(getattr(settings, 'POWERS_EXPIRATION_TRANSFER'))
        power.end_date_field = future_date

        power.start_date_transmission = datetime.datetime.now()
        power.save()


class BondVoidForm(forms.Form):
    def save(self, bond, user):
        try:
            self.form_action(bond, user)
        except:
            raise forms.ValidationError("Failed to save form.")


class BondPrintForm(forms.Form):
    def save(self, bond, user):
        try:
            self.form_action(bond, user)
        except:
            raise forms.ValidationError("Failed to save form.")

    def form_action(self, bond, user):
        bond = Bond.objects.get(id=bond.id)
        bond.has_been_printed = True
        bond.save()


