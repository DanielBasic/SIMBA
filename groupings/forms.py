from django.forms import ModelForm
from .models import Group_by_ad

class GroupByAd_form(ModelForm):
    class Meta:
        model = Group_by_ad
        fields = ['image', 'title']