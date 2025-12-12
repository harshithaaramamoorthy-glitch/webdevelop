from django.contrib import admin

from.models import germy

@admin.register(germy)
class germyAdmin(admin.ModelAdmin):
    List_display = ('id','title','completed','created_at')
    List_filter = ('completed')
    Search_fields = ('title')
