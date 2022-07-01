from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = "George"
        cls.last_name = "Clooney"

        cls.user = User.objects.create(
            first_name=cls.first_name, 
            last_name=cls.last_name,
        ) 

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length =user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)
    
    # def test_user_has_information_fields(self):              
    #     self.assertEqual(self.actor.first_name, self.first_name)
    #     self.assertEqual(self.actor.last_name, self.last_name)
    #     self.assertIsNone(self.actor.date_of_birth)
    #     self.assertIsNone(self.actor.date_of_death)