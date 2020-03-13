# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Pictureurl, Analytics, CSV


class PictureUrlAdmin(admin.ModelAdmin):
    list_display = ["file_name", "date_created","title","image_path","auid", "details", "short_link", "hyperlink", "action"]


    class meta:
        model = Pictureurl

class CsvAdmin(admin.ModelAdmin):
    list_display = ["auid", "name","csv_file_name","csv_path","date_created"]

    class meta:
        model = CSV


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('device', 'ip','campaign_url')
    list_filter = ('campaign_url',)

admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(Pictureurl, PictureUrlAdmin)
admin.site.register(CSV, CsvAdmin)