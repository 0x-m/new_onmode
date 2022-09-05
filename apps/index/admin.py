from django.contrib import admin

from .models import (
    About,
    BlogPost,
    Certificate,
    ContactUsMessage,
    ContactUsType,
    CreateShopGuide,
    GeoLocation,
    Law,
    ReturnOrderGuide,
    ShopSet,
    SiteInfo,
    SitePage,
    SliderPhoto,
)


@admin.register(SliderPhoto)
class SlidePhotoAdmin(admin.ModelAdmin):
    list_display = ["alt", "precedence"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(ShopSet)
class ShopSet(admin.ModelAdmin):
    list_display = ["title", "slogan"]
    filter_horizontal = ["shops"]


admin.site.register(SiteInfo)
admin.site.register(About)
admin.site.register(Law)
admin.site.register(CreateShopGuide)
admin.site.register(ReturnOrderGuide)

admin.site.register(ContactUsType)
admin.site.register(GeoLocation)


@admin.register(ContactUsMessage)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "type", "title"]
    list_filter = ["type__title"]


admin.site.register(Certificate)


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ["en_name"]
    readonly_fields = ["slug"]
