from django import forms
from django.contrib.auth import ( authenticate, get_user_model )
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import requests
from django.forms import modelformset_factory

from pictureURL.models import Pictureurl, CSV



class UploadCsvForm(forms.Form):
    class Meta:
        model = CSV
        fields = ["name","csv_path"]


class UploadphotoForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ["title", "details", "hyperlink", "image_path", "action"]


class EditphotoForm(forms.ModelForm):
    class Meta:
        model = Pictureurl
        fields = ['title', "details", "image_path", "hyperlink", "action"

                  ]
EditphotoFormset = modelformset_factory(Pictureurl, form=EditphotoForm, extra=0)

class PublishForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ['phonenumber', 'message']



class ContactForm(forms.Form):
    #
    # class Meta:
    #     model = Pictureurl

        # fields  = ['email', 'subject', 'message',  ]
        email = forms.EmailField()
        subject = forms.CharField(max_length=100)
        attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        message = forms.CharField(widget = forms.Textarea)