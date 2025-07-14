from django.contrib import admin
from .models import Item, UserDetails

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone_number', 'age', 'bank_account_name')
    search_fields = ('user_id', 'name', 'phone_number')
    readonly_fields = ('user_id',)
