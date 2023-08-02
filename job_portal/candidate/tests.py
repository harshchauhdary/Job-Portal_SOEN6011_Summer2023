from django.test import TestCase
from .forms import CandidateForm
from .models import Candidate
# Create your tests here.


class CandidateFormTestCase(TestCase):
    def test_valid_form(self):
        
        form_data = {
            'firstName': 'Neha',
            'lastName': 'XYZ',
            'phone': '1234567890',
        }
        form = CandidateForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # You can also check if the fields are rendered with the correct widget attributes
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('class="form-control"', form.as_table())
        self.assertIn('class="form-control"', form.as_ul())

    def test_invalid_form(self):
        # Prepare invalid form data (invalid phone number)
        form_data = {
            'firstName': 'Neha',
            'lastName': 'XYZ',
            'phone': 'invalid_phone',
        }
        form = CandidateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['Phone number must be a 10-15 digit number.'])

    def test_invalid_form_too_short_phone(self):
        # Prepare invalid form data (phone number too short)
        form_data = {
            'firstName': 'Neha',
            'lastName': 'XYZ',
            'phone': '123',
        }
        form = CandidateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['Phone number must be a 10-15 digit number.'])

    def test_invalid_form_too_long_phone(self):
        # Prepare invalid form data (phone number too long)
        form_data = {
            'firstName': 'Neha',
            'lastName': 'XYZ',
            'phone': '1234567890123456',
        }
        form = CandidateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['Phone number must be a 10-15 digit number.'])

