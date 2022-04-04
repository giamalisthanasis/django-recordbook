

# Create your views here.

from os import name
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.admin import widgets
from .models import Exercise
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget ,AdminSplitDateTime
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.staticfiles import finders






# Generate a pdf file

def record_book_pdf(request,pk):
    # Create Bytestream Buffer
    buf= io.BytesIO()
    #Create.Canvas
    c = canvas.Canvas(buf,pagesize=A4,bottomup=0)
    width , height = A4
    #create a text object
    textobject= c.beginText()
    textobject.setTextOrigin(inch,inch)
    textobject.setFont("Helvetica", 14, leading=None)


    #add some line of text
    lines = [
        "ΑΘΑΝΑΣΙΟΣ",
        "Α/ΦΗ",
        "ΚΕΡΑΥΝΟΣ BLACK"
        ]

    for line in lines:
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buf.seek(0)

    #return something

    return FileResponse(buf, filename='record.pdf')

def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    
                    if uri.startswith(mUrl):
                            path = os.path.join( uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join ( uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path




def record_book_html2pdf(request,pk):
    exercise=get_object_or_404(Exercise,pk=pk)

    template_path = 'record_book/pdf.html'
    context = {'exercise':exercise}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response,link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html +   '</pre>')
    return response




class Record_bookListView(generic.ListView):
    model=Exercise
    ordering = ['-date_published']
    paginate_by = 4
    #queryset = model.objects.filter(ic = request.user)
    def get_queryset(self):
        query = self.request.GET.get('exercise_date')
       # query2 = self.request.GET.get('ic')
        #object_list = Exercise.objects.all()
        if self.request.user.is_authenticated and query:
            object_list = Exercise.objects.filter(ic=self.request.user,exercise_date=query)
        elif self.request.user.is_authenticated:
            object_list = Exercise.objects.filter(ic=self.request.user)
        elif query:
            object_list = Exercise.objects.filter(exercise_date=query)
        else:
            object_list = Exercise.objects.all()       
        return object_list.order_by('-exercise_date','-exercise_time')
     


#def list_exercises(request):
#    exercises=Exercise.objects.all()
#    return render(request, "record_book/list.html", {"exercises":exercises})

class Record_bookDetailView(generic.DetailView):
    model=Exercise

#def detail_exercise(request, pk):
#    exercise=get_object_or_404(Exercise,pk=pk)
#    return render(request,"record_book/detail.html",{"exercise":exercise})


class Record_bookCreateView(LoginRequiredMixin,SuccessMessageMixin, generic.edit.CreateView):
    model = Exercise
    fields = ['exercise_date','exercise_time','callsign','strength','work_position','radio','frequency','net','net_success','crypto',
                'area_1','area_1_from','area_1_to','area_2','area_2_from','area_2_to','e30a','e30b','e31a','e31b','e32','e33','e34','e35a','e35b','e36a',
                'e36b','e37a','e37b','e38','e83','remarks'] 
    success_message="Record Created Successfully!"
    def get_form(self):
        form = super().get_form()
        form.fields['exercise_date'].widget = DatePickerInput()
        form.fields['exercise_time'].widget = TimePickerInput()
        return form

    

    def form_valid(self, form):
        form.instance.ic=self.request.user
        return super().form_valid(form)


class Record_bookUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,generic.UpdateView):
    model = Exercise
    fields = ['callsign','remarks']
    success_message = "Record Updated Successfully!"

    def form_valid(self, form):
        form.instance.ic = self.request.user
        return super().form_valid(form)

    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.ic:
            return True
        else:
            return False
#he SuccessMessageMixin works by hooking itself on the form_valid

class Record_bookDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model = Exercise
    success_message = "Record deleted Successfully!"
    success_url="/"

    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.ic:
            return True
        else:
            return False

# we are overriding BlogDeleteView’s delete method and sending a flash message of type success.
    def delete(self,request,*args,**kwargs):
        messages.success(self.request, self.success_message)
        return super(Record_bookDeleteView, self).delete(request, *args, **kwargs)











