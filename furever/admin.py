from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Pet, UserProfile, AdoptionRequest, Favourite, Comment


@admin.register(Pet)
class PetAdmin(SummernoteModelAdmin):
    list_display = ('name', 'species', 'breed', 'user', 'status', 'authorised', 'featured', 'date_added')
    search_fields = ['name', 'breed', 'description', 'user__username']
    list_filter = ('authorised', 'status', 'species', 'featured', 'date_added')
    summernote_fields = ('description',)
    list_editable = ('authorised', 'featured', 'status')
    ordering = ('-date_added',)
    
    actions = ['approve_pets', 'unapprove_pets', 'mark_as_featured']
    
    def approve_pets(self, request, queryset):
        updated = queryset.update(authorised=True)
        self.message_user(request, f'{updated} pet(s) successfully approved.')
    approve_pets.short_description = "Approve selected pets"
    
    def unapprove_pets(self, request, queryset):
        updated = queryset.update(authorised=False)
        self.message_user(request, f'{updated} pet(s) successfully unapproved.')
    unapprove_pets.short_description = "Unapprove selected pets"
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} pet(s) marked as featured.')
    mark_as_featured.short_description = "Mark selected pets as featured"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'created_on')
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ('created_on',)


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'status', 'request_date')
    search_fields = ['user__username', 'pet__name', 'message']
    list_filter = ('status', 'request_date')
    list_editable = ('status',)
    ordering = ('-request_date',)


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'save_date', 'notes')
    search_fields = ['user__username', 'pet__name', 'notes']
    list_filter = ('save_date',)
    ordering = ('-save_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_on', 'updated_on')
    search_fields = ['user__username', 'pet__name', 'content']
    list_filter = ('created_on', 'updated_on')
    ordering = ('-created_on',)