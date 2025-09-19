from django import forms
from django.contrib import admin
from .models import Book
from django.templatetags.static import static


class BookModelForm(forms.ModelForm):
    check = forms.BooleanField(label=" : ",required=False)
    catagory_display = forms.CharField(label="Predictided Subjects",required=False,disabled=True)
    DEPARTMENT_CHOICES = [
        ('---', '---'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('ME', 'ME'),
        ('CE', 'CE'),
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label="Department")
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
        }
    def clean_name(self):
                quantity = self.cleaned_data['name']
                if quantity is None:
                    raise forms.ValidationError("Name field should not be None...!")
                return quantity
    class Media:
        js = [static("js/main.js")]