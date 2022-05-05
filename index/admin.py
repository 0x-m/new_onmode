import site
from django.contrib import admin
from .models import About, BlogPost, Law, ShopSet, SiteInfo, SliderPhoto

@admin.register(SliderPhoto)
class SlidePhotoAdmin(admin.ModelAdmin):
    list_display = ['alt', 'precedence']
    
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title']
    
    
    
@admin.register(ShopSet)
class ShopSet(admin.ModelAdmin):
    list_display = ['title', 'slogan']
    filter_horizontal = ['shops']

admin.site.register(SiteInfo)
admin.site.register(About)
admin.site.register(Law)