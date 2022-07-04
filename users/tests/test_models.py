from django.test import TestCase
from users.models import User
from django.utils import timezone

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = "George"
        cls.last_name = "Clooney"
        cls.email = "georgeclooney@gmail.com"
        cls.is_seller = False

        cls.user = User.objects.create(
            email=cls.email,
            first_name=cls.first_name, 
            last_name=cls.last_name,
            is_seller=cls.is_seller
        ) 

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length =user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)
    
    def test_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 255)
    
    def test_is_active_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('is_active').default
        self.assertEquals(default, True)

    def test_updated_at_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('updated_at').default
        self.assertEquals(default, timezone.now)
