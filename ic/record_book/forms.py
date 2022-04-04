from django import forms
from django.db.models import fields
from .models import Exercise


class Record_bookAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_date','exercise_time','callsign','strength','work_position','radio','frequency','net','net_success','crypto',
                'area_1','area_1_from','area_1_to','area_2','area_2_from','area_2_to','e30a','e30b','e31a','e31b','e32','e33','e34','e35a','e35b','e36a',
                'e36b','e37a','e37b','e38','e83','remarks'] 
        


