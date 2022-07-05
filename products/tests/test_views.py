from rest_framework.test import APITestCase
from users.models import User
from products.models import Product
from rest_framework.views import status
from rest_framework.authtoken.models import Token

class ProductViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product = {"description": "Test test test test", "price": 2000.50, "quantity": 2}

        cls.user = {"email": "test@mail.com", "password": "1234", "first_name": "Testname", "last_name": "Testlastname", "is_seller": False}
        cls.seller = {"email": "test2@mail.com", "password": "1234", "first_name": "DTestname", "last_name": "Testlastname", "is_seller": True}
        cls.new_user = User.objects.create_user(**cls.user)
        cls.new_seller = User.objects.create_user(**cls.seller)

        cls.token_user = Token.objects.create(user=cls.new_user)
        cls.token_seller = Token.objects.create(user=cls.new_seller)

    def test_create_product_without_seller_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)
        res = self.client.post('/api/products/', data=self.product)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_product_with_seller_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)
        res = self.client.post('/api/products/', data=self.product)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", res.data)
        self.assertIn("seller", res.data)
        self.assertIn("id", res.data["seller"])
        self.assertIn("email", res.data["seller"])
        self.assertIn("first_name", res.data["seller"])
        self.assertIn("last_name", res.data["seller"])
        self.assertIn("is_seller", res.data["seller"])
        self.assertIn("date_joined", res.data["seller"])
        self.assertIn("description", res.data)
        self.assertIn("price", res.data)
        self.assertIn("quantity", res.data)
        self.assertIn("is_active", res.data)

    def test_create_product_with_seller_token_missing_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)
        res = self.client.post('/api/products/', data={})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_seller_token_with_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)
        data = self.product
        data["quantity"] = -1
        res = self.client.post('/api/products/', data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_with_owner_seller_token(self):
        product = Product.objects.create(**self.product)
        product.seller = self.new_seller
        product.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_seller.key)
        data = {"description": "Test update"}
        res = self.client.patch(f'/api/products/{product.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("id", res.data)
        self.assertIn("seller", res.data)
        self.assertIn("id", res.data["seller"])
        self.assertIn("email", res.data["seller"])
        self.assertIn("first_name", res.data["seller"])
        self.assertIn("last_name", res.data["seller"])
        self.assertIn("is_seller", res.data["seller"])
        self.assertIn("date_joined", res.data["seller"])
        self.assertIn("description", res.data)
        self.assertIn("price", res.data)
        self.assertIn("quantity", res.data)
        self.assertIn("is_active", res.data)

    
    def test_update_product_with_other_seller_token(self): 
        product = Product.objects.create(**self.product)
        product.seller = self.new_seller
        product.save()
        seller2 = self.seller
        seller2["email"] = "test3@mail.com"
        new_seller2 = User.objects.create_user(**seller2)
        token_seller2 = Token.objects.create(user=new_seller2)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_seller2.key)
        data = {"description": "Test update"}
        res = self.client.patch(f'/api/products/{product.id}/', data=data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_list_products(self):
        data = self.product
        products = []
        for i in range(3):
            product = Product.objects.create(**data)
            data["description"] = data["description"] + " test"
            products.append(product)
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        i = 0
        for p in products:
            self.assertEqual(p.description, res.data[i]["description"])
            self.assertIn("description", res.data[i])
            self.assertIn("price", res.data[i])
            self.assertIn("quantity", res.data[i])
            self.assertIn("is_active", res.data[i])
            self.assertIn("seller_id", res.data[i])
            self.assertNotIn("id", res.data[i])
            self.assertNotIn("seller", res.data[i])
            i = i+1

    def test_filter_product(self):
        product = Product.objects.create(**self.product)
        res = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(product.description, res.data["description"])
        self.assertIn("description", res.data)
        self.assertIn("price", res.data)
        self.assertIn("quantity", res.data)
        self.assertIn("is_active", res.data)
        self.assertIn("seller_id", res.data)
        self.assertNotIn("id", res.data)
        self.assertNotIn("seller", res.data)
