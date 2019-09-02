from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Profile, InterestGroup, GroupPost, EventPost, DiscussionPost


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'picture', 'year','phonenumber', 'tagline', 'bio']})
    ]
    list_display = ('name', 'registration_date', 'year', 'bio')


class DiscussionPostInline(admin.TabularInline):
    model = DiscussionPost
    extra = 1


class EventPostInLine(admin.TabularInline):
    model = EventPost
    extra = 1


class InterestGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'thumbnail']})
    ]
    list_display = ('name',)
    inlines = [DiscussionPostInline, EventPostInLine]


class GroupPostMPTTModelAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(InterestGroup, InterestGroupAdmin)
admin.site.register(GroupPost, GroupPostMPTTModelAdmin)
