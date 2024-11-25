# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# UserModel = get_user_model()
#
#
# class ProfileViewTest(APITestCase):
#
#     def setUp(self):
#         """Create a test user and authenticate them."""
#         self.user = UserModel.objects.create_user(
#             username='admin',
#             password='admin',
#             email='admin@gmail.com'
#         )
#
#         login_url = reverse('accounts:login')
#         login_data = {'username': 'admin', 'password': 'admin'}
#         response = self.client.post(login_url, login_data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check login success
#         self.url = reverse('accounts:profile')
#
#     def test_get_user_profile(self):
#         """Test that the profile can be retrieved."""
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['username'], self.user.username)
#         self.assertEqual(response.data['email'], self.user.email)
#         self.assertNotIn('password', response.data)  # Ensure password is not in response
