from rest_framework import serializers
from ..models.library_models import *
from ..models.user import *


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class BooksInputSerializer(serializers.Serializer):
    Title = serializers.CharField(max_length=50, source='title')
    Author = serializers.CharField(max_length=50)

    def create(self, validated_data):
        author_name = validated_data.pop('Author')
        author, created = Author.objects.get_or_create(name=author_name)
        return Books.objects.create(author=author, **validated_data)


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ReservataionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationQueue
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = '__all__'


class BookCheckoutsSerializer(serializers.ModelSerializer):
    num_checkouts = serializers.SerializerMethodField()

    def get_num_checkouts(self, obj):
        return obj.num_checkouts if obj.num_checkouts else None
    class Meta:
        model = Books
        fields = ['title', 'num_checkouts']

class MemberCheckoutSerializer(serializers.ModelSerializer):
    num_checkouts = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_num_checkouts(self, obj):
        return obj.num_checkouts

    def get_name(self, obj):
        return obj.user.name
    class Meta:
        model = Members
        fields = ['name', 'num_checkouts']