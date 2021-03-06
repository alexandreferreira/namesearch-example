from django.forms import Textarea, NumberInput
from django.forms.models import ModelForm
from core.models import Log, Entry
from core.tasks import register_log_entry_update, register_log_entry_create, register_log_entry_viewed
__author__ = 'alexandreferreira'

class EntryForm(ModelForm):
    created = True

    def __init__(self, instance=None, **kwargs):
        if instance:
            self.created = False
            register_log_entry_viewed.delay(instance.number, instance.text)
            kwargs['instance'] = instance
        super(EntryForm, self).__init__(**kwargs)

    def save(self, commit=True):
        if self.created:
            register_log_entry_create.delay(self.instance.number, self.instance.text)
        else:
            old_entry = Entry.objects.get(number=self.instance.number)
            register_log_entry_update.delay(old_entry.number, old_entry.text)
        return super(EntryForm, self).save(commit=commit)

    class Meta:
        model = Entry
        fields = ['number', 'text']
        widgets = {
            'number': NumberInput(attrs={'class': 'form-control', 'min_value': -9223372036854775808,
                                          'max_value': 9223372036854775807}),
            'text': Textarea(attrs={'class': 'form-control'})
        }
