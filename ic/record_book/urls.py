from django.urls import path
from . import views
from profiles import views as profiles_views
from django.views.i18n import JavaScriptCatalog

from django.conf.urls import url


urlpatterns = [
    path("", views.Record_bookListView.as_view(), name="exercise_list"),
    path('jsi18n',JavaScriptCatalog.as_view(), name='js-catalog'),
    path("exercise/<int:pk>", views.Record_bookDetailView.as_view(),name="exercises_detail"),
    path('profile/<int:pk>', profiles_views.profile, name="profile"),
    path("record_book/create",views.Record_bookCreateView.as_view(),name="record_book_create"),
    path("record_book/<int:pk>/update",views.Record_bookUpdateView.as_view(),name="record_book_update"),
    path("record_book/<int:pk>/delete",views.Record_bookDeleteView.as_view(),name="record_book_delete"),
    path("record_book/<int:pk>/pdf",views.record_book_pdf,name="record_book_pdf"),
    path("record_book/<int:pk>/html2pdf",views.record_book_html2pdf,name="record_book_html2pdf")
    ]
