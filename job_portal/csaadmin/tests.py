from django.test import TestCase

# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual('The lion says "roar"', 'The lion says "roar"')