from django.shortcuts import redirect, render
from .models import Form, InputField, Response, ResponseQuestion
from django.http import HttpResponse, JsonResponse , HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse

# Create your views here.
@login_required(login_url='/auth/login/')
def create(request):
    if request.method == "POST":
        Form(name=request.POST["form-name"] , user_id = request.user.id).save()
        f = Form.objects.filter(name=request.POST["form-name"])[::-1][0]

        for i in range(int(request.POST["questionCount"])):
            try:
                InputField(label=request.POST[str(i)], form_id=f.id).save()
            except Exception as e:
                print(str(e))
        context = {'message': "Here is your form link"
         , "Your_link" : "link"
         , "form_id" : f.id }
        return HttpResponseRedirect(reverse('myform'))
#        return HttpResponseRedirect(reverse('view-form' , args = (f.id,)))
    else:
        return render(request, "form/create.html")

def delform(request , form_id):
    print('yaali')
    f = Form.objects.filter(user_id = request.user.id)
    Form.objects.filter(id=form_id).delete()
    context = {'message' : 'form has been deleted successfully'}
    return render(request , 'dashbord/my_form.html' , {'forms': f})


def view_form(request, form_id):
    try:
        f = Form.objects.get(id=form_id)
    except:
        return HttpResponse("404 Not Found")
    form = Form.objects.filter(id = form_id)
    inputs = InputField.objects.filter(form_id=f.id)
    formname = form[0].name
    return render(request, "form/view-form.html", {
        "form_id": form_id,
        "inputs": inputs,
        "name":formname
    })


def submit_form(request, form_id):
    res = Response(form_id=form_id)
    res.save()
    r = Response.objects.filter(form_id=form_id)[::-1][0]
    for i in request.POST:
        if i == "csrfmiddlewaretoken":
            continue
        ResponseQuestion(question_id=i, response=request.POST[i], response_id=r.id).save()
    return HttpResponseRedirect(f"/d/{form_id}/{r.id}/")
