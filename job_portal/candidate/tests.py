from django.test import TestCase
from .forms import CandidateForm
from .models import Candidate
from django.urls import reverse
from .models import User, Job, Candidate, Application, Notification


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





class CandidateViewsTestCase(TestCase):

    def setUp(self):
        # Set up any data needed for the test cases
        self.user = User.objects.create(username='test_user')
        self.candidate = Candidate.objects.create(user=self.user, firstName='Neha', lastName='XYZ')
        self.job = Job.objects.create(title='Test Job', status='OPEN')
        self.application = Application.objects.create(candidate=self.candidate, job=self.job, status='Applied')
        self.notification = Notification.objects.create(candidate=self.candidate, read=False)

    def test_view_notifications(self):
        url = reverse('view_notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/notifications.html')
        self.assertContains(response, self.notification.title)

    def test_close_notification(self):
        url = reverse('close_notification', args=[self.notification.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/candidates/notifications')
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)

    def test_view_jobs(self):
        url = reverse('view_jobs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/viewJobsTemplate.html')

    def test_apply_job_success(self):
        url = reverse('apply_job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/appliedSuccessTemplate.html')
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

    def test_apply_job_already_applied(self):
        # Apply for the job once
        url = reverse('apply_job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/appliedSuccessTemplate.html')
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

        # Try applying again for the same job
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/candidates/viewJobTemplate.html')

    def test_view_job(self):
        url = reverse('view_job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/viewJobTemplate.html')
        self.assertContains(response, self.job.title)

    def test_view_resume_without_resume(self):
        url = reverse('view_resume')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/candidates/createResume')

    def test_view_resume_with_resume(self):
        self.candidate.resume = 'path/to/resume.pdf'
        self.candidate.save()
        url = reverse('view_resume')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/resumeDetailTemplate.html')



