from django import forms
from .models import ContactUsMessage, ContactUsType
class ContactUsForm(forms.ModelForm):
    type = forms.ModelChoiceField(ContactUsType.objects.all())
    class Meta:
        model = ContactUsMessage
        fields = ['full_name', 'email', 'title', 'body']
        