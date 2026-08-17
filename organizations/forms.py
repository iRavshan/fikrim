from django import forms
from .models import Organization, Feedback

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'org_type', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tashkilot nomi'}),
            'org_type': forms.Select(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Manzili'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        # Rasmlar formadan tashqarida, request.FILES.getlist('images')
        # orqali qabul qilinadi — ularning soni o'zgaruvchan.
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Shu yerga fikr va mulohazalaringizni yozing...'
            }),
        }
