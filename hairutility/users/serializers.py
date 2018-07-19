from rest_framework import serializers
from .models import User, CompanyProfile, HairProfile
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

# Primary keys aren't created in time to save after signup


class HairProfileSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Serializers the object of hairprofiles
    """

    user = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    creator = serializers.CharField(required=False, allow_blank=True)
    access_code = serializers.CharField(required=False, allow_blank=True, read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = HairProfile
        fields = ('pk', 'user', 'creator', 'first_name', 'hairstyle_name', 'first_image_url', 'second_image_url', 'third_image_url',
                  'fourth_image_url', 'profile_description', 'created', 'is_displayable', 'is_approved', 'tags', 'access_code')
        depth = 1


class UserSerializer(serializers.ModelSerializer):

    hair_profiles = HairProfileSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                  'is_active', 'is_stylist', 'auth_token', 'hair_profiles')
        read_only_fields = ('auth_token', 'pk', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# Remove pk and auth token in production
