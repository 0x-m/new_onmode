from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .models import Category, Collection, CreateShopRequest, Option, Photo, Product, ProductOptionValue, ProductStats, ProductType, Shop, Comment
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from import_export.fields import Field
from django.db.models import Count

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
    list_display = ['name', 'meta_title', 'owner_phone', 'active']
    readonly_fields = ['id', 'product_count', 'date_created']
    list_editable = ['active']
    list_filter = ['active']
    search_fields = ['name', 'meta_title', 'owner_phone']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    readonly_fields = ['id']


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ['id','parent', 'name', 'en_name', 'meta_title', 'meta_description', 'meta_keywords']
        export_order = ['id', 'parent', 'name', 'en_name', 'meta_title', 'meta_description', 'meta_keywords']
        

@admin.register(Category)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ['id', 'name', 'parent']
    readonly_fields = ['id', 'slug', 'en_slug']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['id', 'slug', 'en_slug']
    list_filter = ['index_view']
    filter_horizontal = ['products', ]


class ProductStatsInline(admin.StackedInline):
    model = ProductStats


class ProductRateFilter(admin.SimpleListFilter):
    title = 'Rate'
    parameter_name = 'rate'

    def lookups(self, request, model_admin):
        return (
            ('0s', 'below 1 star'),
            ('1s', 'between 1 and 2 stars'),
            ('2s', 'between 2 and 3 star'),
            ('3s', 'between 3 and 4 star'),
            ('4s', 'between 4 and 5 star'),
            ('5s', '5 start')
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == '0s':
            return queryset.filter(stats__rates_avg__lt=1)
        elif value == '1s':
            return queryset.filter(stats__rates_avg__gte=1, stats__rates_avg__lt=2)
        elif value == '2s':
            return queryset.filter(stats__rates_avg__gte=2, stats__rates_avg__lt=3)
        elif value == '3s':
            return queryset.filter(stats__rates_avg__gte=3, stats__rates_avg__lt=4)
        elif value == '4s':
            return queryset.filter(stats__rates_avg__gte=4, stats__rates_avg__lt=5)

        elif value == '5s':
            return queryset.filter(stats__rates_avg=5)

        return queryset


class ProductCommentFilter(admin.SimpleListFilter):
    title = 'comments'
    parameter_name = 'comments'

    def lookups(self, request, model_admin):
        return (
            ('top', 'top most'),
            ('l20', 'less than 20s'),
            ('l50', 'less than 50s'),
            ('b100', 'between 50 and 200'),
            ('b200', 'between 200 and 300'),
            ('b300', 'between 300 and 400'),
            ('b400', 'between 400 and 500'),
            ('b500', 'between 500 and 1000'),
            ('g1000', 'grather tan 1000s'),
        )

    def queryset(self, request, queryset):

        value = self.value()
        if value == 'l20':
            return queryset.filter(stats__comments__lte=20)
        elif value == 'l50':
            return queryset.filter(stats__comments__lte=50)
        elif value == 'b100':
            return queryset.filter(stats__comments__gte=50, stats__comments__lte=200)
        elif value == 'b200':
            return queryset.filter(stats__comments__gte=200, stats__comments__lte=300)
        elif value == 'b300':
            return queryset.filter(stats__comments__gte=300, stats__comments__lte=400)
        elif value == 'b400':
            return queryset.filter(stats__comments__gte=400, stats__comments__lte=500)
        elif value == 'b500':
            return queryset.filter(stats__comments__gte=500, stats__comments__lte=1000)
        elif value == 'g1000':
            return queryset.filter(stats__comments__gte=1000)
        elif value == 'top':
            return queryset.order_by('stats__comments')


class ProductLikesFilter(admin.SimpleListFilter):
    title = 'likes'
    parameter_name = 'likes'

    def lookups(self, request, model_admin):
        return (
            ('top', 'top most'),
            ('l20', 'less than 20s'),
            ('l50', 'less than 50s'),
            ('b100', 'between 50 and 200'),
            ('b200', 'between 200 and 300'),
            ('b300', 'between 300 and 400'),
            ('b400', 'between 400 and 500'),
            ('b500', 'between 500 and 1000'),
            ('g1000', 'grather tan 1000s'),
        )

    def queryset(self, request, queryset):

        value = self.value()
        if value == 'l20':
            return queryset.filter(stats__likes__lte=20)
        elif value == 'l50':
            return queryset.filter(stats__likes__lte=50)
        elif value == 'b100':
            return queryset.filter(stats__likes__gte=50, stats__likes__lte=200)
        elif value == 'b200':
            return queryset.filter(stats__likes__gte=200, stats__likes__lte=300)
        elif value == 'b300':
            return queryset.filter(stats__likes__gte=300, stats__likes__lte=400)
        elif value == 'b400':
            return queryset.filter(stats__likes__gte=400, stats__likes__lte=500)
        elif value == 'b500':
            return queryset.filter(stats__likes__gte=500, stats__likes__lte=1000)
        elif value == 'g1000':
            return queryset.filter(stats__likes__gte=1000)
        elif value == 'top':
            return queryset.order_by('stats__likes')


class ProductSalesFilter(admin.SimpleListFilter):
    title = 'success sails'
    parameter_name = 'sales'

    def lookups(self, request, model_admin):
        return (
            ('top', 'top most'),
            ('l20', 'less than 20s'),
            ('l50', 'less than 50s'),
            ('b100', 'between 50 and 200'),
            ('b200', 'between 200 and 300'),
            ('b300', 'between 300 and 400'),
            ('b400', 'between 400 and 500'),
            ('b500', 'between 500 and 1000'),
            ('g1000', 'grather tan 1000s'),
        )

    def queryset(self, request, queryset):

        value = self.value()
        if value == 'l20':
            return queryset.annotate(c=Count('orders')).filter(c__lte=20)
        elif value == 'l50':
            return queryset.annotate(c=Count('orders')).filter(c__lte=50)
        elif value == 'b100':
            return queryset.annotate(c=Count('orders')).filter(c__gte=50, c__lte=200)
        elif value == 'b200':
            return queryset.annotate(c=Count('orders')).filter(c__gte=201, c__lte=300)
        elif value == 'b300':
            return queryset.annotate(c=Count('orders')).filter(c__gte=301, c__lte=400)
        elif value == 'b400':
            return queryset.annotate(c=Count('orders')).filter(c__gte=401, c__lte=500)
        elif value == 'b500':
            return queryset.annotate(c=Count('orders')).filter(c__gte=500, c__lte=1000)
        elif value == 'g1000':
            return queryset.annotate(c=Count('orders')).filter(c__gte=1000)
        elif value == 'top':
            return queryset.annotate(c=Count('orders')).order_by('c')

# class ProductFailsFilter(admin.SimpleListFilter):
#     title = 'returneds'
#     parameter_name = 'fails'

#     def lookups(self, request, model_admin):
#         return (
#             ('top', 'top most'),
#             ('l20', 'less than 20s'),
#             ('l50', 'less than 50s'),
#             ('b100', 'between 50 and 200'),
#             ('b200', 'between 200 and 300'),
#             ('b300', 'between 300 and 400'),
#             ('b400', 'between 400 and 500'),
#             ('b500', 'between 500 and 1000'),
#             ('g1000', 'grather tan 1000s'),
#         )

#     def queryset(self, request, queryset):

#         value = self.value()
#         if value == 'l20':
#             return queryset.filter(stats__fails__lte=20)
#         elif value == 'l50':
#             return queryset.filter(stats__fails__lte=50)
#         elif value == 'b100':
#             return queryset.filter(stats__fails__gte=50, stats__fails__lte=200)
#         elif value == 'b200':
#             return queryset.filter(stats__fails__gte=200, stats__likes__lte=300)
#         elif value == 'b300':
#             return queryset.filter(stats__fails__gte=300, stats__fails__lte=400)
#         elif value == 'b400':
#             return queryset.filter(stats__fails__gte=400, stats__fails__lte=500)
#         elif value == 'b500':
#             return queryset.filter(stats__fails__gte=500, stats__fails__lte=1000)
#         elif value == 'g1000':
#             return queryset.filter(stats__fails__gte=1000)
#         elif value == 'top':
#             return queryset.order_by('stats__fails')


class ProductResource(ModelResource):
    class Meta:
        model = Product
        fields = ['id','name', 
                  'en_name','price', 
                  'has_sales', 
                  'sales_price','quantity', 
                  'shipping_cost','attributes',
                  'meta_title', 'meta_description',
                  'meta_keywords', 'quantity', 
                  'stock_low_threshold', 
                  'free_shipping', 'published', 
                  'prod_code', 'shop__name', 'category__name', 
                  'date_created', 'last_updated', 'discount__code']
        export_order = ['id','name', 
                  'en_name','price', 
                  'has_sales', 
                  'sales_price','quantity', 
                  'shipping_cost','attributes',
                  'meta_title', 'meta_description',
                  'meta_keywords', 'quantity', 
                  'stock_low_threshold', 
                  'free_shipping', 'published', 
                  'prod_code', 'shop__name', 'category__name', 
                  'date_created', 'last_updated', 'discount__code'
        ]


@admin.register(Product)
class ProductAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = ProductResource
    @admin.action(description='rate')
    def get_rate(instance):
        return instance.stats.rates_avg

    @admin.action(description='sells')
    def get_sells_count(instance):
        return instance.stats.number_of_sells


    list_display = ['name', 'price', 'shop',
                    get_rate,get_sells_count, 'quantity', 'published', 'deleted']
    list_editable = ['published', ]
    
    readonyl_fields = ['id', 'prod_code', 'date_created',
                       'slug', 'en_slug', 'last_updated']
    search_fields = ['shop__name', 'name', 'en_name', 'meta_title']

    list_filter = ['published', 'deleted', 'has_sales', 'date_created',
                   ProductRateFilter, ProductCommentFilter,ProductLikesFilter, 
                   ProductSalesFilter, 
                #    ProductFailsFilter, 
                   'category']
                   
    ordering = ['date_created']
    inlines = [ProductStatsInline, ]
    filter_horizontal = ['relateds']

@admin.register(ProductOptionValue)
class ProductoptionValueAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment)
