from django import forms
from .models import Book,bookTag
from shelf.models import Shelf
from django.templatetags.static import static

from shelf.models import Shelf
from books.models import Book
from books.utils.recommendation import recommend_shelf_for_book  # your helper


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "id": "id_name"}),
            "auther": forms.TextInput(attrs={"autocomplete": "author", "id": "id_auther"}),
            "addr": forms.Select(attrs={"id": "id_addr"}),
            "catagory": forms.SelectMultiple(attrs={"id": "id_catagory"}),
        }



class BookModelForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['addr'].queryset = Shelf.objects.filter(qunt__lt=5)



class BookForm(forms.ModelForm):
    auto_recommend = forms.BooleanField(required=False, label="📦 Auto-recommend shelf")
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('auto_recommend'):
            name = cleaned_data.get('name')
            author = cleaned_data.get('auther')
            categories = cleaned_data.get('catagory')

            shelf = recommend_shelf_for_book(name, categories, author)
            if shelf:
                cleaned_data['addr'] = shelf
        return cleaned_data
    class Meta:
        model = Book
        fields = ['name', 'catagory', 'auther', 'addr', 'discription', 'auto_recommend']
