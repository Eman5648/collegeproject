from django.contrib import admin

from  .models import Category, Product, Variation,Subscriber, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price']

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Subscriber)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['email']

def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"

@admin.register(Newsletter)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    actions = [send_newsletter]