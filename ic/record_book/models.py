# Create your models here.
from datetime import date
from django.contrib.messages.api import success
from django.db import models
from django.template.defaultfilters import default
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinLengthValidator

remarks_validator = MinLengthValidator(
    limit_value=2, message="Content should be at least 2 characters long!")


class Net(models.TextChoices):
    NET = 'NO', 'NO'
    NET0 = 'A00.025', 'Net 0'
    NET1 = 'A00.125', 'Net 1'
    NET2 = 'A00.225', 'Net 2'
    NET3 = 'A00.325', 'Net 3'
    NET4 = 'A00.425', 'Net 4'
    NET5 = 'A00.525', 'Net 5'


class Exercise(models.Model):
    WORK_POSITION_CHOICES = (
        ('ic1', 'ic1'), 
        ('ci2', 'ic2'), 
        ('ic3', 'ic3'), 
        ('ic4', 'ic4'), 
        ('ic5', 'ic5'), 
        ('ic6', 'ic6'), 
        ('ic7', 'ic7'), 
        ('ic8', 'ic8'), 
        ('ic9', 'ic9'), 
        ('ic10', 'ic10'),
        )


    date_published = models.DateTimeField(default=timezone.now)
    exercise_date=models.DateField()
    exercise_time=models.TimeField(default=timezone.now)
    ic = models.ForeignKey(User, on_delete=models.CASCADE)
    callsign = models.CharField(max_length=20)
    strength = models.PositiveSmallIntegerField()
    work_position = models.CharField(choices=WORK_POSITION_CHOICES, max_length=20,null=True)
    radio =  models.CharField(max_length=50,verbose_name="R/S",help_text='FXXX or xxx.xxx',)
    frequency = models.CharField(max_length=20,verbose_name="Fxxx")
    net = models.CharField(max_length=20,verbose_name="NET",choices=Net.choices,null=True)
    net_success = models.BooleanField(default=False)
    crypto = models.BooleanField(default=False)
    area_1 = models.CharField(max_length=20)
    area_1_from = models.CharField(max_length=20)
    area_1_to = models.CharField(max_length=20)
    area_2 = models.CharField(max_length=20,blank=True)
    area_2_from = models.CharField(max_length=20,blank=True)
    area_2_to = models.CharField(max_length=20,blank=True)
    e30a = models.IntegerField(verbose_name="E-30a",help_text="BFM")
    e30b = models.IntegerField(verbose_name="E-30b",blank=True,null=True)
    e31a = models.IntegerField(verbose_name="E-31a",blank=True,null=True)
    e31b = models.IntegerField(verbose_name="E-31b",blank=True,null=True)
    e32 = models.IntegerField(verbose_name="E-32",blank=True,null=True)
    e33 = models.IntegerField(verbose_name="E-33",blank=True,null=True)
    e34 = models.IntegerField(verbose_name="E-34",blank=True,null=True)
    e35a = models.IntegerField(verbose_name="E-35a",blank=True,null=True)
    e35b = models.IntegerField(verbose_name="E-35b",blank=True,null=True)
    e36a = models.IntegerField(verbose_name="E-36a",blank=True,null=True)
    e36b = models.IntegerField(verbose_name="E-36b",blank=True,null=True)
    e37a = models.IntegerField(verbose_name="E-37a",blank=True,null=True)
    e37b = models.IntegerField(verbose_name="E-37b",blank=True,null=True)
    e38 = models.IntegerField(verbose_name="E-38",blank=True,null=True)
    e83 = models.IntegerField(verbose_name="E-83",blank=True,null=True)
    remarks = models.TextField(validators=[remarks_validator])


    

    def __str__(self):
        return self.callsign

    def get_absolute_url(self):
        return reverse("exercises_detail", kwargs={'pk': self.pk})


# The generic CreateView will try to redirect us to the newly created model
# instance on success, but it doesn’t know it’s URL path. It will look for a
# method called get_absolute_url on the model, which will generate a URL
# for the detailed view of the newly created instance.
