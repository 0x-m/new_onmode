from django import forms
from .models import ContactUsMessages
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsMessages
        fields = ['full_name', 'email', 'title', 'body']
        