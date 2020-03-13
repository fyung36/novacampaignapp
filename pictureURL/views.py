# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, ListView, TemplateView
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from scannerr.config import pagination
import uuid
from django.contrib.auth import authenticate, login, get_user_model
from pictureURL.forms.auth import UploadphotoForm,PublishForm,EditphotoForm,\
    EditphotoFormset, ContactForm, UploadCsvForm
from .message import sendPostRequest
from .models import Pictureurl, Analytics, CSV
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from . import bitly_api
import csv
import json
import requests

# Create your views here.


@login_required
def dashboard(request):
    '''
        Dashboard View
    '''

    template = 'home.html'

    context = {'title':'Dashboard',
               'user': request.user,
               }
    return render(request, template, context)

class Upload_Campaign(View):
    form_class = UploadphotoForm
    template = 'campaign.html'
    success_url = reverse_lazy('campaign_list')

    def get(self, request):
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'Upload Campaign'
                   }
        return render(request, self.template, context)

    def post(self, request):
        image_ext = [".jpeg", ".jpg", ".gif", ".png"]
        video_ext = [".avi", ".mp4", ".flv", ".mpeg", ".swf", ".mpg", ".mpe", ".mov", ".wmv", ".ogg", "3gp"]
        print ("form is valid")
        picture = Pictureurl()
        picture.title = request.POST.get('title')
        picture.details = request.POST.get('details')
        picture.hyperlink = request.POST.get('hyperlink')
        picture.action = request.POST.get('action').upper()
        picture.date_created = datetime.utcnow()
        picture.auid = str(uuid.uuid4())
        new_file_name = picture.auid
        file_url = 'http://{hostname}/campaign/{filename}'.format(
            hostname=settings.HOSTNAME,
            filename =new_file_name)
        print(file_url)
        try:
            bitly_client = bitly_api.Connection(access_token='41e1370eaa1d74350310ef25a91fa05793015dc5')
            call = bitly_client.shorten(uri=file_url)
            short_link = call.get('url')
            print(short_link)
            picture.short_link = short_link if short_link else file_url
        except Exception:
            picture.short_link = file_url
        _file = request.FILES['file']
        file_extension = os.path.splitext(_file.name)[1]
        picture.file_name = _file.name
        media_type = None
        if file_extension in image_ext:
            media_type = 'image'
        elif file_extension in video_ext:
            media_type = 'video'
        if not media_type:
            messages.add_message(request, messages.ERROR, "Invalid Media Uploaded - Only Image | Video Supported")
            return redirect('/NewCampaign')
        if _file.size == 0:
            messages.add_message(request, messages.ERROR, "Empty File Upload")
            return redirect('/new_directory')
        if _file.size > 2.621e+7:
            messages.add_message(request, messages.ERROR, "File Uploaded Too Large ")
            return redirect('/new_directory')

        new_file_path = os.path.join(settings.MEDIA_URL, "%s" % new_file_name) + file_extension
        print ("starting to upload file ")
        with open(new_file_path, 'wb+') as destination:
            for chunk in _file.chunks():
                destination.write(chunk)
        picture.image_path = new_file_name + file_extension



        print("saving to db")
        picture.save()
        request.user.campaign.add(picture)
        print('file uploaded')
        return redirect("campaign_list")


class UploadCSV(View):
    form_class = UploadCsvForm
    template = 'Uploadcsv.html'
    success_url = reverse_lazy('campaign_list')

    def get(self, request):
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'Upload Campaign'
                   }
        return render(request, self.template, context)

    def post(self, request):
        file_ext = [".txt", ".csv"]
        print("form is valid")
        csv = CSV()
        csv.name = request.POST.get('title')
        csv.date_created = datetime.utcnow()
        csv.auid = str(uuid.uuid4())
        new_file_name = csv.auid
        print(new_file_name)
        _file = request.FILES['file']

        file_extension = os.path.splitext(_file.name)[1]
        csv.csv_file_name = _file.name
        print(csv.csv_file_name)
        if file_extension not in file_ext:
            messages.add_message(request, messages.ERROR, "Invalid File Uploaded - Only .csv | .txt Supported")
            return redirect('/new_directory')
        if _file.size == 0:
            messages.add_message(request, messages.ERROR, "Empty File Upload")
            return redirect('/new_directory')
        if _file.size > 2.621e+7:
            messages.add_message(request, messages.ERROR, "File Uploaded Too Large ")
            return redirect('/new_directory')

        new_file_path = os.path.join(settings.FILE_URL, new_file_name) + file_extension
        print("starting to upload file ")
        with open(new_file_path, 'wb+') as destination:
            for chunk in _file.chunks():
                destination.write(chunk)
        csv.csv_path = new_file_name + file_extension
        print(csv.csv_path)

        print("saving to db")
        csv.save()
        print('file uploaded')
        return redirect("campaign_list")


''' all  campaigns view  '''
# def campaign_list(request):
#     template = 'Manage-Campaigns.html'
#     campaign_list = Pictureurl.objects.all()
#     c
#     page = request.GET.get('page', 1)
#     paginator = Paginator(campaign_list, 5)
#     try:
#         items = paginator.page(page)
#     except PageNotAnInteger:
#         items = paginator.page(1)
#     except EmptyPage:
#         items = paginator.page(paginator.num_pages)
#
#     context = {
#         'title': 'All Campaigns',
#         "items": items
#     }
#     return render(request, template, context)

class CampaignView(TemplateView):
    template_name = 'Manage-Campaigns.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
         context = super(CampaignView, self).get_context_data(**kwargs)
         context['campaign'] = Pictureurl.objects.all()
         context['csv'] = CSV.objects.all()
         return context
#
# def index(response, id):
#     ls = ToDoList.objects.get(id=id)
#
#     if ls in response.user.todolist.all():
#
# 	if response.method == "POST":
# 	    if response.POST.get("save"):
# 		for item in ls.item_set.all():
# 		    if response.POST.get("c" + str(item.id)) == "clicked":
# 		        item.complete = True
# 		    else:
# 		        item.complete = False
#
# 		    item.save()
#
# 	    elif response.POST.get("newItem"):
# 		txt = response.POST.get("new")
#
# 		if len(txt) > 2:
# 		    ls.item_set.create(text=txt, complete=False)
# 		else:
# 		    print("invalid")
#
#
# 	return render(response, "main/list.html", {"ls":ls})
#
#     return render(response, "main/home.html", {})

def campaigndetail(request, auid,):
    template = 'campaign-detail.html'
    details = Pictureurl.objects.get(auid=auid)
    context = {

        'details': details,
        'title': ' Details',
    }
    return render(request, template, context)



def directorydetail(request, auid):
    template = 'directoty-detail.html'
    details = CSV.objects.get(auid=auid)
    print(details.csv_path)
    with open(os.path.join(settings.FILE_URL, details.csv_path),'r+') as csv:
        csv_data = csv.reader(csv, delimiter=',')



    context = {

        'details': details,
        'title': ' Details',
    }
    return render(request, template, context)

def search(request):
    template = "AllCampaigns.html"
    query = request.GET.get('q')
    result = Pictureurl.objects.filter(Q(title__icontains=query))
    context = {
        "allphoto": result
    }
    print(context)
    return render(request, template, context)

#
# class EditCampaign(UpdateView):
#     template = "campaign-edit.html"
#     form_class = EditphotoForm
#     queryset = Pictureurl.objects.all()
#
#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         campaign =get_object_or_404(Pictureurl, id=id_)
#         queryset = Pictureurl.objects.filter(item=item)
#
#
#     def form_valid(self, form):
# #         print(form.cleaned_data)
#         return super().form_valid(form)

class EditListView(View):
    model = Pictureurl
    fields = ['title']
    template_name = 'campaign.html'
    def get(self,request,id):
        item = get_object_or_404(Pictureurl,pk=id)
        context = dict()
        context['data'] = item
        return render(request,self.template_name,context)

    def post(self,request,id):
        formset = EditphotoFormset(request.POST, request.FILES)
        print(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                item_pk = self.kwargs.get("id")
                item = get_object_or_404(Pictureurl, pk=item_pk)
                new_item.item = item
                new_item.save()
            messages.success(request, "Your Campaign has been updated.")
            return redirect("campaign_list")
        raise Http404


#
# def edit(request, id):
#     template = "campaign-edit.html"
#     post = get_object_or_404(Pictureurl, id=id)
#     if request.method == "POST":
#         form = UploadphotoForm(request.POST, instance=g )
#         try:
#             if form.is_valid():
#                 form.save()
#                 messages.SUCCESS(request, "Your Campaign Was Edited")
#                 # return redirect('campaigndetail')
#         except Exception as e:
#             messages.warning(request, "Your Campaign Was Not Edited")
#     else:
#         form = EditphotoForm(instance=post)
#
#     context = {
#           'form': form,
#             'post': post,
#         }
#
#     return render(request, template, context)




def delete_campaign(request,pk):
    if request.method == 'GET':
        photo = Pictureurl.objects.get(pk=pk)
        print(photo)
        print("the delete")
        photo.delete()
    return redirect('campaign_list')

# loaders
def campaign(request, auid):
    template = 'ads.html'
    if Pictureurl.objects.filter(auid=auid).exists():
        model = Pictureurl.objects.get(auid=auid)
        # request.COOKIES.get()
        context = dict()
        context['model'] = model
        return render(request, template ,context)
    else:
        return Http404


class Publish(View):
    form_class = PublishForm
    template = "smsform.html"
    def get(self, request, id):
        details = Pictureurl.objects.get(id=id)
        csv = CSV.objects.all()
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'Publish',
                   'details': details,
                   'csv': csv
                   }
        return render(request, self.template, context)

    def post(self, request, id):
        url = "https://www.bulksmsnigeria.com/api/v1/sms/create"
        phone = request.POST.get('phonenumber')
        auid = request.POST.get('auid')
        if phone == "":
            if CSV.objects.filter(auid=auid).exists():
                file = CSV.objects.get(auid=auid)
                numbers = []
                with open(os.path.join(settings.FILE_URL, file.csv_path),'r+') as csv_file:
                    phone_numbers = csv.reader(csv_file, delimiter=',')
                    next(phone_numbers)
                    for row in phone_numbers:
                        numbers.append(row[0])
                phone = ",".join(numbers)
        message = request.POST.get('message')
        print(message)
        to = f"{phone}"
        body = f"{message}"
        print(to)
        print(body)

        response = sendPostRequest(url, "P0KpZxWPZwOIT6JIKEBCFOFE6Q12ztUrsbCoxdE2ppfsXRwqAUyx3kEvTYFy", "Nova360", to, body)
        print(response)
        if response == "ok":
            messages.add_message(request, messages.SUCCESS, "Message Sent")
            return redirect("campaign_list")

        messages.add_message(request, messages.ERROR, "Could Not Send Message, Please Try Again Later")
        return redirect("campaign_list")

#error logging
# def contactus(request):
#     template = 'support.html'
#     form = ContactForm(request.POS or None)
#     if form.is_valid():
#
#         email = form.cleaned_data.get('emaiL')
#         subject = form.cleaned_data.get('subject')
#         message = form.cleaned_data.get('message')
#
#         send_mail(subject, message, email,
#             ['damilola@novathreesixty.com',
#              'tosin@novathreesixty,com'],
#             fail_silently=False,
#         )
#     context = {'title': 'Support',
#                }
#
#     return render(request, template, context)


class EmailAttachementView(View):
    form_class = ContactForm
    template_name = 'support.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print("form working")
        return render(request, self.template_name, {'email_form': form})

    # Multiple Files Attachements
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print(form)

        if form.is_valid():
            print ("form is valid ")

            subject = request.POST.get('subject')#form.cleaned_data['subject']
            message = request.POST.get('message')#form.cleaned_data['message']
            email  =  request.POST.get('email') # form.cleaned_data['email']

            print(subject)
            files = request.FILES.getlist('attach')
            print(files)

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                context = {
                    'email_form': form,
                    'error_message': 'Sent email to %s' % email
                }
                return render(request, self.template_name,
                              )
            except:
                print('not valid')
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        print('no form')
        return render(request, self.template_name,
                      {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

    # # Single File Attachment
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #
    #         subject = form.cleaned_data['subject']
    #         message = form.cleaned_data['message']
    #         email = form.cleaned_data['email']
    #         attach = request.FILES['attach']
    #
    #         try:
    #             mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
    #             mail.attach(attach.name, attach.read(), attach.content_type)
    #             mail.send()
    #             return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
    #         except:
    #             return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})
    #
    #     return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})



class Analytic(View):

    def get(self, requests, short_link=None,*args, **kwargs):
        qs = Pictureurl.objects.filter(short_link__iexact=short_link)
        if qs.count() == 1 and qs.exists():
            obj = qs.first()
            click = Analytics.objects.create_event(obj)
            print(click)
        obj = get_object_or_404()

        ip = requests.META.get('HTTP_X_FORWARDED_FOR')
        x_forwarded_for = Analytics.ip
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = requests.META.get('REMOTE_ADDR')

        ua = requests.META['HTTP_USER_AGENT']
        device = ""
        if requests.Windows or requests.Linux:
            device = "Windows"
        if requests.Android:
            device = "Android"
        if requests.iPhone  or requests.iPad:
            device = "iOS"
        if requests.iMac :
            device = "Mac"
        influencer = requests.GET['anchor']
        decoded_info = "Airtel"
        return HttpResponseRedirect(device)



def set_cookie(request):
    userid = str(uuid.uuid4())

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hit_count(request):
    if not request.session.session_key:
        request.session.save()
    s_key = request.session.session_key

    ip = get_client_ip(request)
    device = requests.META['HTTP_USER_AGENT']
    url, url_created = Pictureurl.objects.get_or_create(url=request.path)

    if url_created:
        track, created = Analytic.objects.get_or_create(campaign_url=url, ip=ip, session=s_key, device=device)
        if created:
            url.increase()
            request.session[ip] = ip
            request.session[request.path] = request.path
    else:
        if ip and request.path not in request.session:
            track, created = Analytics.objects.get_or_create(url_hit=url, ip=ip, session=s_key, device=device )
            if created:
                url.increase()
                request.session[ip] = ip
                request.session[request.path] = request.path
    return url.hits