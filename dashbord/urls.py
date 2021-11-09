from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("<str:form_id>/<str:submission_id>/submissions/", views.view_all_submission , name='all_submission'),
    path("<str:form_id>/<str:submission_id>/", views.view_submission , name ='view_submission'),
    path("" , views.main_dashbord , name = 'index'),
    path("<str:form_id>/" , views.view_form , name = 'view_form'),
    path("/myform/" , views.my_form , name = 'myform'),
]
