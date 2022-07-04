from functools import cache
from django.test import TestCase
from products.models import Product
from users.models import User

class PoductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.description = "Test test test test"
        cls.price = 2000.50
        cls.quantity = 2

        cls.product = Product.objects.create(
            description=cls.description, 
            price=cls.price,
            quantity=cls.quantity
        ) 

        cls.products = [Product.objects.create(
            description="Lorem ipsum",
            price=2.50,
            quantity=2
            ) for _ in range(20)
        ]

        cls.seller = User.objects.create(
            email='test@mail.com',
            first_name='test_name',
            last_name='test_name',
            is_seller=True
        )

    def test_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 15)

    def test_price_decimal_places(self):
        product = Product.objects.get(id=1)
        decimal_places = product._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_price_is_active(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field('is_active').default
        self.assertEquals(default, True)

    def test_seller_may_contain_multiple_products(self):
        for product in self.products:
            product.seller = self.seller
            product.save()
        self.assertEquals(
            len(self.products),
            self.seller.products.count()
        )
        for product in self.products:
            self.assertIs(product.seller, self.seller)
        
    def test_product_cannot_belong_more_than_one_seller(self):
        for product in self.products:
            product.seller = self.seller
            product.save()
        seller_two = User.objects.create(
            email='test2@mail.com',
            first_name='test2_name',
            last_name='test2_name',
            is_seller=True
        )
        for product in self.products:
            product.seller = seller_two
            product.save()
        for product in self.products:
            self.assertNotIn(product, self.seller.products.all())
            self.assertIn(product, seller_two.products.all())