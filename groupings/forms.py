from django import forms
from .models import Group_by_ad

class GroupByAd_form(forms.ModelForm):
    class Meta:
        model = Group_by_ad
        fields = ['image', 'title']

    title = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'title_field'})
    )

    image = forms.ImageField(
        widget=forms.FileInput(attrs={'id': 'image_field'})
    )