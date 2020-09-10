from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.
from accounts.models import GuestModel
from accounts.forms import UserAdminChangeForm,UserAdminCreationForm

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ( 'full_name',)}),
        ('Permissions', {'fields': ('admin', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class GuestModelAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestModel

admin.site.register(GuestModel, GuestModelAdmin)
admin.site.register(User,UserAdmin)
