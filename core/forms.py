from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 'placeholder': 'tu@empresa.com'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors', 'placeholder': 'Nombre de tu empresa'}),
            'subject': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-900 text-white rounded-lg border border-gray-700 focus:border-cyan-500 focus:outline-none transition-colors resize-none', 'placeholder': 'Describe tu proyecto, objetivos, timeline estimado y cualquier detalle relevante...', 'rows': 6}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].choices = [
            ('', 'Seleccionar...'),
            ('web-app', 'Aplicación Web'),
            ('mobile-app', 'Aplicación Móvil'),
            ('enterprise', 'Sistema Empresarial'),
            ('api', 'API/Backend'),
            ('consulting', 'Consultoría Técnica'),
            ('other', 'Otro'),
        ]
