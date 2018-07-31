from rest_framework import serializers
from .models import User, Company, HairProfile
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


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
        fields = ('pk', 'user', 'creator', 'first_name', 'hairstyle_name', 'first_image_url',
                  'second_image_url', 'third_image_url', 'fourth_image_url', 'profile_description',
                  'created', 'is_displayable', 'tags', 'is_approved', 'access_code')
        depth = 1


class UserSerializer(serializers.ModelSerializer):

    hair_profiles = HairProfileSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                  'is_active', 'is_stylist', 'auth_token', 'profile_image_url', 'hair_profiles')
        read_only_fields = ('auth_token', 'pk', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# Remove pk and auth token in production


class CompanySerializer(serializers.ModelSerializer):

    users = serializers.SlugRelatedField(queryset=User.objects.all(), many=True,
                                         slug_field='email', write_only=True, required=False)

    user_set = UserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Company
        fields = ('pk', 'company_name', 'address', 'state', 'city',
                  'zip_code', 'phone_number', 'banner_image_url', 'user_set', 'users')

    def update(self, instance, validated_data):
        users = validated_data.pop('users', None)
        instance = super().update(instance, validated_data)
        if users:
            for user in users:
                instance.user_set.add(user)
            instance.save()
        return instance
