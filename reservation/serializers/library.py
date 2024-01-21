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