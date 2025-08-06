from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 
                'placeholder': 'Tu nombre completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 
                'placeholder': 'tu@empresa.com',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 
                'placeholder': 'Nombre de tu empresa'
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors resize-none', 
                'placeholder': 'Describe tu proyecto, objetivos, timeline estimado y cualquier detalle relevante...',
                'rows': 6,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar opción vacía al inicio
        choices = [('', 'Seleccionar...')] + list(self.fields['subject'].choices)
        self.fields['subject'].choices = choices
        self.fields['subject'].required = True
