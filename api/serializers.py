from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from blog.models import Category, Post, Comment
from django.contrib.auth.models import User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'categoryserializer'


class CommentSerializer(ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'author_name', 'post', 'created_at']
        read_only_fields = ['author', 'post']
        ref_name = 'commentserializer'

        # second method of saving files (custom)

    def create(self, validated_data):
        post_id = self.context['post_id']
        author = self.context['author']
        return Comment.objects.create(post_id=post_id, author=author, **validated_data)


class AddPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'categories', 'image']


class UpdatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'categories', 'image', 'updated_at']


class PostSerializer(ModelSerializer):
    last_updated = SerializerMethodField(method_name='if_updated')
    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    author_name = SerializerMethodField(method_name='get_author_name')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'comments', 'categories', 'author', 'author_name', 'image', 'last_updated',
                  'created_at']
        ref_name = 'Postserializer'

    def if_updated(self, item: Post):
        if item.created_at != item.updated_at:
            return item.updated_at

    def get_author_name(self, obj):
        author = obj.author
        return f"{author.first_name} {author.last_name}"
