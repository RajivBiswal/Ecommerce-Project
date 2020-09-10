from django.contrib import admin
from products import models


class ProductAdmin(admin.ModelAdmin):
    """Customize the admin"""
    list_display = ['__str__','slug']
    class Meta:
        model = models.MyProduct

admin.site.register(models.MyProduct,ProductAdmin)
