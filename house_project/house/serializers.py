from rest_framework import serializers
from .models import (
    Property, Region, City, District, HouseImage,
    LegalDocument, HouseReview, Review, Favorite,
    UserProfile, Rental
)
import joblib
import os
from django.conf import settings

# hhhhhhhhhhhhhhhh
model_path = os.path.join(settings.BASE_DIR, 'model_chek.pkl')
model_predict = joblib.load(model_path)
vec_path = os.path.join(settings.BASE_DIR, 'vec.pkl')
vec = joblib.load(vec_path)



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'role']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['image']


class HouseReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    check_commit = serializers.SerializerMethodField()

    class Meta:
        model = HouseReview
        fields = ['id', 'author', 'text', 'check_commit', 'stars', 'created_date']


    def get_check_commit(self, obj):
        text = obj.text
        if text:
            result = model_predict.predict(vec.transform([text]))[0]
            return result


class PropertySerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)
    documents = LegalDocumentSerializer(many=True, read_only=True)
    image_house = HouseImageSerializer(many=True, read_only=True)
    property_review = HouseReviewSerializer(many=True, read_only=True)
    favorited_by = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'property_type', 'street', 'address', 'area', 'price', 'rooms',
            'year_built', 'floor', 'total_floors', 'condition', 'seller',
            'documents', 'image_house', 'property_review', 'favorited_by'
        ]

    def get_favorited_by(self, obj):
        return [user.id for user in obj.favorited_by.all()]



class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'seller', 'text', 'stars', 'created_date')


class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'property', 'created_at')


class RentalSerializer(serializers.ModelSerializer):
    renter = UserProfileSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Rental
        fields = [
            'id', 'property', 'renter', 'start_date', 'end_date', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']
