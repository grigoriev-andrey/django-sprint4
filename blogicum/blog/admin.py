from django.contrib import admin

from .models import PublishedModel, Category, Location, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'text',
        'pub_date',
    )
    list_editable = (
        'text',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_editable = (
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
