from django import forms
from powers.models import User, Powers, Bond
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class TransferPowersForm(forms.Form):
    agent = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True))
    end_date = forms.DateField(initial=datetime.datetime.today())

    def save(self, powers, user):
        try:
            self.form_action(powers, user)
        except:
            raise forms.ValidationError("Failed to save form.")

    def form_action(self, powers, user):
        power = Powers.objects.get(id=powers.id)
        power.agent_id = self.cleaned_data['agent']
        power.end_date_field = self.cleaned_data['end_date']
        power.start_date_transmission = datetime.datetime.now()
        power.save()


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


