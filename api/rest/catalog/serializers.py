from rest_framework import serializers

from apps.catalogue.models import (
    Category,
    Collection,
    Comment,
    Discount,
    Favourite,
    Product,
    ProductStats,
    Shop,
)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "en_name")


class CategorySerializer(serializers.ModelSerializer):
    childs = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "en_name",
            "slug",
            "en_slug",
            "meta_keywords",
            "parent",
            "childs",
        ]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "owner",
            "name",
            "meta_title",
            "meta_description",
            "banner",
            "logo",
            "address_description",
            "phone",
            "product_capacity",
            "product_count",
            "fee",
            "active",
            "deleted",
            "date_created",
        ]
        extra_kwargs = {"id": {"read_only": True}, "owner": {"read_only": True}}


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "id",
            "percent",
            "start_date",
            "end_date",
            "max_amount",
            "max_sales_allowed",
            "sales",
            "is_valid",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "prod_code",
            "shop",
            "category",
            "name",
            "en_name",
            "slug",
            "en_slug",
            "meta_keywords",
            "sku",
            "quantity",
            "stock_low_threshold",
            "free_shipping",
            "published",
            "deleted",
            "sold_individually",
            "price",
            "has_sales",
            "sales_price",
            "shipping_cost",
            "description",
            "attributes",
            "date_created",
            "preview",
            "discounts",
            "relateds",
        ]


class ProductStatsSerializer(serializers.Serializer):
    class Meta:
        model = ProductStats
        field = ["views", "comments", "likes", "rates_avg"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "en_name",
            "slug",
            "en_slug",
            "sloan",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "description",
            "page_poster_url",
            "page_poster",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["product", "body", "published", "rate", "date_created"]


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ["id", "product"]
