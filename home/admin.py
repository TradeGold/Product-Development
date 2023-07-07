from django.contrib import admin
from home.models import *
from home.views import manageemailfromadmin
from django.contrib.admin import AdminSite
#from django.utils.translation import ugettext_lazy
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(New)
admin.site.register(login_register)
admin.site.register(email_verification)

@admin.register(Youtube_Link)
class YoutubeLinK(admin.ModelAdmin):

    def has_add_permission(self, request):
        check = len(Youtube_Link.objects.all())
        if check == 1:
            return False
        else:
            return True
    def has_delete_permission(self, request, obj=None):
        return False




admin.site.site_header = 'Fun Olympics Games'