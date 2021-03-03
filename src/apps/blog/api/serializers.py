from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify

from apps.blog.models import Category, Post, PostImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {'slug': {'required': False}}
    
    def validate(self, data):
        slug = data.get('slug')
        slug = slug if slug else slugify(data.get('name'))
        
        if Category.objects.filter(slug__iexact=slug).exists():
            raise serializers.ValidationError(
                {'name': ['Category with similar name already exists.']}
            )
        
        return data | {'slug': slug}


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['post', 'large']
    
    def to_representation(self, value):
        request = self.context.get('request')
        return {
            'small': request.build_absolute_uri(value.small.url),
            'large': request.build_absolute_uri(value.large.url)
        }


class PostSerializer(serializers.ModelSerializer):

    owner = UserSerializer(required=False)
    categories = CategorySerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'slug': {'required': False}}
    
    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        categories_pk = data.getlist('categories')
        try:
            internal_data['categories'] = [
                Category.objects.get(pk=pk) for pk in categories_pk
            ]
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                {'categories': ['Invalid category\'s primary key']}
            )
        return internal_data

    def validate(self, data):
        slug = data.get('slug')
        slug = slug if slug else slugify(data.get('title'))
        
        if Post.objects.filter(slug__iexact=slug).exists():
            raise serializers.ValidationError(
                {'title': ['Post with similar title already exists.']}
            )
        
        return data | {'slug': slug}
