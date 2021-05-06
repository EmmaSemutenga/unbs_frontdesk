from django import forms
from .models import Customer, Feedback

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = "__all__"
        # exclude = ('owner',)

class FeedbackForm(forms.ModelForm):
    
    class Meta:
        model = Feedback
        # fields = "__all__"
        exclude = ('provided_feedback', 'customer',)