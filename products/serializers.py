from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import *


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'tags', "reviews"]


class ProductsReviewListSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews']


class ProductsActiveTagsListSerializer(serializers.ModelSerializer):
    activeTags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title activeTags'.split()

    def get_activeTags(self, product):
        tags = Tag.objects.filter(product=product).exclude(is_active=False)
        return TagListSerializer(tags, many=True).data


class ProductCreateValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(min_length=10)
    price = serializers.IntegerField()
    category = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_title(self, title):
        product = Product.objects.filter(title=title)
        if product.count() > 0:
            raise ValidationError("Продукт с таким названием уже существует")
        try:
            int(title)
            raise ValidationError("Название продукта не должно быть числом")
        except:
            return title

        return title

    def validate_price(self, price):
        if price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return price

    def validate_tags(self, tags):
        for i in range(len(tags)):
            print(tags[i])
            try:
                tagExist = Tag.objects.get(id=tags[i])
            except:
                raise ValidationError(f"Тега с id = {tags[i]} в позиции {i} не существует")

    def validate_category(self, category):
        try:
            categoryExist = Category.objects.get(id=category)
        except:
            raise ValidationError("Категории с таким id не существует")
