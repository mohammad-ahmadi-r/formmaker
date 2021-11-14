from django.shortcuts import render
from form.models import InputField , Form , Response , ResponseQuestion
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from form.models import models
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
import datetime
from django.utils.translation import get_language , activate , gettext

def view_submission(request , form_id , submission_id):
    form = Form.objects.get(id=form_id)
    rs = Response.objects.filter(form_id=form_id)[::-1]
    rs2 = []
    i = 1
    for r in rs:
        rs2.append([r , i])
        i+=1

    resp_qs = ResponseQuestion.objects.filter(response_id = submission_id)
    data = []
    for r in resp_qs:
        i = InputField.objects.get(id = r.question_id)
        data.append([i.label , r.response])

    return render(request , 'dashbord/user-response.html' , {'data':data , 'rs':rs2 , 'f':form})


def main_dashbord(request):
    return render(request , 'dashbord/index.html')

@login_required(login_url='/auth/login/')
def my_form(request):
    f = Form.objects.filter(user_id = request.user.id)
    print('fuck')
    return render(request , 'dashbord/my_form.html' , {'forms': f})


def view_form(request , form_id):
    rs = Response.objects.filter(form_id=form_id)
    rs2 = []
    i = 1
    for r in rs:
        rs2.append([r , i])
        i+=1
    i=[1]
    f = Form.objects.get(user_id = request.user.id , id = form_id)
    q = InputField.objects.filter(form_id = form_id)
    ln = len(rs2)
    return render(request , "dashbord/form.html" , {'q': q,'f': f , 'form_id':form_id ,
     'rs2':rs2 , 'len':ln , 'rs':rs , 'i':i})

def view_all_submission(request, form_id , submission_id):
    try:
        form = Form.objects.get(id=form_id)
        rs = Response.objects.filter(form_id=form_id)[::-1]

        print(rs)
        rs2 = []
        i = 1
        for r in rs:
            rs2.append([r , i])
            i+=1

        rss = ResponseQuestion.objects.filter(response_id = submission_id)
        data = []
        print(rss)
        for r in rss:
            i = InputField.objects.get(id = r.question_id)
            data.append([i.label , r.response])

    except:
        return HttpResponse('yeah')
    #    content = '{message:there is no response yet!}'
    #    return render(request , 'dashbord/view-response.html' , content)
    return render(request , 'dashbord/view-response.html' , {'data':data , 'rs':rs2 , 'f':form})


from django.http import HttpResponse
from django.views.generic import View

from dev.utils import render_to_pdf #created in step 4

def GeneratePDF(self, request, *args, **kwargs):
    template = get_template('form/view_form.html.html')
    context = {'q': q,'f': f , 'form_id':form_id ,
     'rs2':rs2 , 'len':ln , 'rs':rs}

    html = template.render(context)
#        return HttpResponse(html)
    pdf = render_to_pdf('form/view_form.html.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("123")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

'''
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
'''
