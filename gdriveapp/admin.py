from django.contrib import admin
from .models import Content
class ContentAdmin(admin.ModelAdmin):
    list_display=['id','fileName','link','content']

admin.site.register(Content,ContentAdmin)