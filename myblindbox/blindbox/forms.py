from django import forms
from .models import BlindBox, Message

class BlindBoxForm(forms.ModelForm):
    class Meta:
        model = BlindBox
        fields = ['content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
