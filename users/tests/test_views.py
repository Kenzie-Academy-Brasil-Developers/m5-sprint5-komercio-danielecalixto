import ipdb
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.views import status

class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {"email": "test@mail.com", "password": "1234", "first_name": "Dani", "last_name": "Dani", "is_seller": False}
        cls.login =  {"email": "test@mail.com", "password": "1234"}

        cls.email = 'dani@mail.com'
        cls.password = '1234'
        cls.first_name = 'Dani'
        cls.last_name = 'Barros'
        cls.is_seller = False

        cls.user_created = User.objects.create(
            email=cls.email,
            first_name=cls.first_name, 
            last_name=cls.last_name,
            is_seller=cls.is_seller
        ) 

    def test_register_user_success(self):
        res = self.client.post('/api/accounts/', data=self.user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)
        self.assertIn('date_joined', res.data)

    def test_register_user_missing_keys(self):
        res = self.client.post('/api/accounts/')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
        self.assertIn('email', res.data)
        self.assertIn('password', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('is_seller', res.data)
    
    def test_register_user_with_already_used_email(self):
        self.client.post('/api/accounts/', data=self.user)
        res = self.client.post('/api/accounts/', data=self.user)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertIn("already exists", str(res.data["email"]))

    def test_register_user_defining_is_active(self):
        self.user["is_active"] = False
        res = self.client.post('/api/accounts/', data=self.user)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_login_success(self):
    #     user = User.objects.get(id=1)
    #     print(user)
    #     self.client.post('/api/accounts/', data=self.user)
    #     res = self.client.post('/api/login/', {'email': 'dani@mail.com', 'password': '1234'}, format='json')
    #     print(res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(new_user.auth_token.key, res.data["token"])
    
    
