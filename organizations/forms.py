from django import forms
from .models import Organization, Feedback
from .images import MAX_UPLOAD_BYTES

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
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Shu yerga fikr va mulohazalaringizni yozing...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                # Telefonda darhol kamera va galereya taklif qilinsin
                'accept': 'image/*',
            }),
        }
        labels = {
            'image': "Rasm biriktirish (ixtiyoriy)",
        }

    def clean_image(self):
        """Juda katta fayllarni qayta ishlashdan oldin to'sib qolamiz.

        Pillow bilan ochishdan oldin tekshiramiz, aks holda o'nlab
        megabaytlik fayl serverning xotirasini egallaydi.
        """
        rasm = self.cleaned_data.get('image')
        if rasm and rasm.size > MAX_UPLOAD_BYTES:
            chegara = MAX_UPLOAD_BYTES // (1024 * 1024)
            raise forms.ValidationError(
                f"Rasm hajmi {chegara} MB dan oshmasligi kerak. "
                "Iltimos, kichikroq rasm tanlang."
            )
        return rasm
