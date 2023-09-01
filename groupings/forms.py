from django.forms import ModelForm
<<<<<<< HEAD

from .models import Group_by_ad


=======
from .models import Group_by_ad

>>>>>>> 0756234d2b9661617960bf49e3dea4f4f70531cb
class GroupByAd_form(ModelForm):
    class Meta:
        model = Group_by_ad
        fields = ['image', 'title']