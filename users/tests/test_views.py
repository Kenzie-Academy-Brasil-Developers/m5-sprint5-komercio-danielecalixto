import ipdb
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from rest_framework.views import status
from rest_framework.authtoken.models import Token

class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {"email": "test@mail.com", "password": "1234", "first_name": "Testname", "last_name": "Testlastname", "is_seller": False}
        cls.seller = {"email": "test2@mail.com", "password": "1234", "first_name": "DTestname", "last_name": "Testlastname", "is_seller": True}

    def test_register_user_success(self):
        res = self.client.post('/api/accounts/', data=self.user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)
        self.assertIn('date_joined', res.data)
    
    def test_register_seller_success(self):
        res = self.client.post('/api/accounts/', data=self.seller)
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

    def test_login_user_success(self):
        new_user = User.objects.create_user(**self.user)
        res = self.client.post('/api/login/', data=self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(new_user.auth_token.key, res.data["token"])
    
    def test_login_seller_success(self):
        new_seller = User.objects.create_user(**self.seller)
        res = self.client.post('/api/login/', data=self.seller)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(new_seller.auth_token.key, res.data["token"])
    
    def test_login_invalid_credentials(self):
        res = self.client.post('/api/login/', data=self.user)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_missing_fields(self):
        res = self.client.post("/api/login/", data={})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)
        self.assertIn("password", res.data)
    
    def test_update_user_all_properties_success(self):
        new_user = User.objects.create_user(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)        
        data = {"email": "test12@mail.com", "password": "12345", "first_name": "Testnameupdate", "last_name": "Testlastnameupdate", "is_seller": True}
        res = self.client.patch(f'/api/accounts/{new_user.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_one_property_success(self):
        new_user = User.objects.create_user(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"first_name": "Testnameupdate"}
        res = self.client.patch(f'/api/accounts/{new_user.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_without_token(self):
        new_user = User.objects.create_user(**self.user)
        data = {"first_name": "Testnameupdate"}
        res = self.client.patch(f'/api/accounts/{new_user.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_using_other_user_key(self):
        new_user = User.objects.create_user(**self.user)
        new_user2 = User.objects.create_user(**self.seller)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"first_name": "Testnameupdate"}
        res = self.client.patch(f'/api/accounts/{new_user2.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_user_is_active(self):
        new_user = User.objects.create_user(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"is_active": False}
        res = self.client.patch(f'/api/accounts/{new_user.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_and_reactivate_user_without_admin_token(self):
        new_user = User.objects.create_user(**self.user)
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        # DEACTIVATE
        data = {"is_active": False}
        res = self.client.patch(f'/api/accounts/{new_user.id}/management/', data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        # REACTIVATE
        data = {"is_active": True}
        res = self.client.patch(f'/api/accounts/{new_user.id}/management/', data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_deactivate_and_reactivate_user_with_admin_token(self):
        new_user = User.objects.create_user(**self.user)
        data = {"email": "boss@mail.com", "password": "abcdf", "is_seller": False}
        new_superuser = User.objects.create_superuser(**data)
        token = Token.objects.create(user=new_superuser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        # DEACTIVATE
        data = {"is_active": False}
        res = self.client.patch(f'/api/accounts/{new_user.id}/management/', data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # REACTIVATE
        data = {"is_active": True}
        res = self.client.patch(f'/api/accounts/{new_user.id}/management/', data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_users(self):
        new_user = User.objects.create_user(**self.user)
        new_user2 = User.objects.create_user(**self.seller)
        res = self.client.get('/api/accounts/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(new_user.email, res.data[0]["email"])
        self.assertIn(new_user2.email, res.data[1]["email"])

    def test_list_newest_users(self):
        new_user = User.objects.create_user(**self.user)
        new_user2 = User.objects.create_user(**self.seller)
        res = self.client.get('/api/accounts/newest/2/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(new_user.email, res.data[1]["email"])
        self.assertEqual(new_user2.email, res.data[0]["email"])
