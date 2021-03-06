from django.contrib import admin

from .models import Category, Collection, CreateShopRequest, Option, Photo, Product, ProductOptionValue, ProductStats, ProductType, Shop


@admin.register(CreateShopRequest)
class CreateShopRequestAdmin(admin.ModelAdmin):

    @admin.action(description="Accept request")
    def accept_request(modeladmin, request, qs):
        for a in qs:
            a.accept()

    @admin.action(description='user')
    def get_user(instance):
        return instance.user.phone_num

    fields = [get_user, 'user', 'title', 'name',
              'date_created', 'accepted', 'rejected', 'reject_status']
    list_display = [get_user, 'name', 'title', 'accepted', 'rejected']
    readonly_fields = [get_user, 'accepted', 'date_created']
    actions = [accept_request]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['owner_phone', 'meta_title', 'name', 'active']
    readonly_fields = ['product_count', 'date_created']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductStatsInline(admin.StackedInline):
    model = ProductStats


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['shop', 'id', 'prod_code', 'name', 'quantity', 'published']
    readonyl_fields = ['prod_code', 'date_created']
    inlines = [ProductStatsInline,]


@admin.register(ProductOptionValue)
class ProductoptionValueAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
