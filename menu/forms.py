from django import forms
from django.utils import timezone
from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    '''Menu form'''
    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']
        widgets = {
            'season': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Please enter the name of a season',
                    'title': 'Season'
                    }),
            'items': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                     'title': 'Items'
                     }),
            'expiration_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Example: 2029-10-17', 
                    'title': 'Expiration Date'
                    })
        }

    def clean_season(self):
        '''Clean season'''
        season = self.cleaned_data.get('season')

        if not season:
            raise forms.ValidationError('Please enter a season')

        return season

    def clean(self):
        '''Clean form data'''
        cleaned_data = super(MenuForm, self).clean()
        items = cleaned_data.get('items')
        expiration_date = cleaned_data.get('expiration_date')

        if items and expiration_date < timezone.now():
            self.add_error('expiration_date', 'A new menu should not be expired')
            raise forms.ValidationError('Please check the expiration date again')
 