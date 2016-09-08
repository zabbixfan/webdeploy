from django.contrib import admin
from .models import appgroup,apphost,auth,tasklog
# Register your models here.
class appgroupAdmin(admin.ModelAdmin):
    list_display = ('appgroup','appname','warpath','deploytype')
    search_fields = ('appgroup','appname','warpath','deploytype') 
    list_filter = ('appgroup','appname','warpath','deploytype')
class apphostAdmin(admin.ModelAdmin):
    list_display = ('hostaddr','username','path','appgroup')
    search_fields = ('hostaddr','username','path','appgroup')
    list_filter = ('hostaddr','username','path','appgroup')
class authAdmin(admin.ModelAdmin):
    list_display = ('user','appgroup')
    search_fields = ('user__username','appgroup__appname')
    list_filter = ('user','appgroup')
    def save_model(self,request,obj,form,change):
        try:
            res = self.model.objects.filter(user=obj.user_id).filter(appgroup=obj.appgroup_id)
            if len(res) == 0:
                obj.save()
        except Exception,e:
            print e
admin.site.register(apphost,apphostAdmin)
admin.site.register(appgroup,appgroupAdmin)
admin.site.register(auth,authAdmin)
admin.site.register(tasklog)
