# from django.test import TestCase
# from django.forms.models import model_to_dict
# # from nose.tools import eq_, ok_
# from nose.tools import ok_
# from .factories import UserFactory
# from ..serializers import UserSerializer


# class TestUserSerializer(TestCase):
#     """ The test case won't work if authentication details are necessary.
#     This is only a problem in beta where the website is locked."""

#     def setUp(self):
#         self.user_data = model_to_dict(UserFactory.build())

#     # def test_serializer_with_empty_data(self):
#     #     serializer = UserSerializer(data={})
#     #     eq_(serializer.is_valid(), False)

#     def test_serializer_with_valid_data(self):
#         serializer = UserSerializer(data=self.user_data)
#         ok_(serializer.is_valid())

# def test_serializer_hashes_password(self):
#     serializer = UserSerializer(data=self.user_data)
#     ok_(serializer.is_valid())

#     user = serializer.save()
#     ok_(check_password(self.user_data.get('password'), user.password))
# Hashing is done after the serialization in the models
