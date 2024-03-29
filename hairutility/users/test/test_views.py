# from django.urls import reverse
# from django.forms.models import model_to_dict
# from nose.tools import eq_
# from rest_framework.test import APITestCase
# from rest_framework import status
# from faker import Faker
# from ..models import User
# from .factories import UserFactory

# fake = Faker()


# class TestUserListTestCase(APITestCase):
#     """
#     Tests /users list operations.
#     """

#     def setUp(self):
#         self.url = reverse('user-list')
#         self.user_data = model_to_dict(UserFactory.build())
#         # self.user_data = {'email': 'cideral02@gmail.com', 'password': 'Jamest02'}

#     def test_post_request_with_no_data_fails(self):
#         response = self.client.post(self.url, {})
#         eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_post_request_with_valid_data_succeeds(self):
#         response = self.client.post(self.url, self.user_data)
#         eq_(response.status_code, status.HTTP_201_CREATED)

#         # user = User.objects.get(pk=response.data.get('pk'))
#         # eq_(user.email, self.user_data.get('email'))
#         # ok_(check_password(self.user_data.get('password'), user.password))


# class TestUserDetailTestCase(APITestCase):
#     """
#     Tests /users detail operations.
#     """

#     def setUp(self):
#         self.user = UserFactory()
#         self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

#     def test_get_request_returns_a_given_user(self):
#         response = self.client.get(self.url)
#         eq_(response.status_code, status.HTTP_200_OK)

#     def test_patch_request_updates_a_user(self):
#         new_first_name = fake.first_name()
#         payload = {'first_name': new_first_name}
#         response = self.client.patch(self.url, payload)
#         eq_(response.status_code, status.HTTP_200_OK)

#         user = User.objects.get(pk=self.user.pk)
#         eq_(user.first_name, new_first_name)
