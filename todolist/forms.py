from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = [
            'task',
            'description',
            'priority',
            'due_date',
            'status',
        ]

        widgets = {
            'task': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your task'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add some details...',
                'rows': 4
            }),

            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
            'class': 'form-select'
            }),
        }