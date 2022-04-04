from django.contrib import admin

# Register your models here.
from .models import Exercise
from .forms import Record_bookAdminForm

# Register your models here.

class Record_bookCreateAdmin(admin.ModelAdmin):
    list_display = ('exercise_date','exercise_time','callsign','strength','work_position','radio','frequency','net','net_success','crypto',
                'area_1','area_1_from','area_1_to','area_2','area_2_from','area_2_to','e30a','e30b','e31a','e31b','e32','e33','e34','e35a','e35b','e36a',
                'e36b','e37a','e37b','e38','e83','remarks') 
    form = Record_bookAdminForm
    list_filter = ['exercise_date']
    date_hierarchy = 'exercise_date'

admin.site.register(Exercise,Record_bookCreateAdmin)