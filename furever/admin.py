from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# @admin.register(MyModelWhichDoesntExistYet) # Replace with your actual model
# class MyModelAdmin(SummernoteModelAdmin):
#     list_display = ('title', 'slug','created_on')
#     search_fields = ['title', 'content']
#     list_filter = ('status', 'created_on')
#     prepopulated_fields = {'slug': ('title',)}
#     summernote_fields = ('content',)

# Register your models here.