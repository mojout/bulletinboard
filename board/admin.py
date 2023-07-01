from django.contrib import admin
from board.models import Announcement, Comment


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'author', 'publish']
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'announcement', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'text']
