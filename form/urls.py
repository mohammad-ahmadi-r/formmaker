from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create , name = 'create'),
    path("v/<str:form_id>/", views.view_form , name = 'view-form'),
    path("del/<str:form_id>/" , views.delform , name = 'delform'),
    path("s/<str:form_id>/", views.submit_form , name = 'submit-form'),
]
