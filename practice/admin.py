from django.contrib import admin

from .models import Publisher,Book,Author,Post,Project,API

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('headshot', 'name', 'email' , 'salutation')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date')
    search_fields = ['title']

class APIAdmin(admin.ModelAdmin):
    list_display = ('path', 'project')
    search_fields = ['path','project']

admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Post, PostAdmin)
admin.site.register(API, APIAdmin)
admin.site.register(Project)
