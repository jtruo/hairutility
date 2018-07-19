from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from nested_admin.nested import *

from .models import User, HairProfile


class HairProfileInline(NestedStackedInline):
    model = HairProfile


class UserAdmin(NestedModelAdmin):

    inlines = [HairProfileInline, ]

    # The fields that are displayed from the User model.

    list_display = ('email', 'id', 'first_name', 'is_admin', 'is_active', 'is_stylist',)

    list_filter = ('is_admin', 'is_stylist')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        # (None, {'fields': ('tags',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class HairProfilesAdmin(NestedModelAdmin):

    list_display = ('hairstyle_name', 'first_image_url', 'profile_description')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(HairProfile, HairProfilesAdmin)
