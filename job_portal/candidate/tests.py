from django.test import TestCase
from .forms import CandidateForm
from django.urls import reverse
from .models import User, Job, Candidate, Application, Notification, Employer, Resume


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
        self.resume = Resume.objects.create(summary='Test summary')
        self.user = User.objects.create(email='e@e.eeee', password='password123', role='candidate')
        self.candidate = Candidate.objects.create(user=self.user, firstName='Neha', lastName='XYZ')
        self.employer_user = User.objects.create(email='employer@e.eeee', password='password123', role='employer')
        self.employer = Employer.objects.create(
            userID=self.employer_user, companyName='Test Company', companyEmail='test@test.com',
            firstName='Test', lastName='Employer', phone='9876543210'
        )
        self.job = Job.objects.create(
            position='Test Job', status='OPEN', description='Test Job Description', 
            applicationDeadline='2023-12-31', employer=self.employer
        )        
        self.notification = Notification.objects.create(candidate=self.candidate, read=False)

    def test_view_notifications(self):
        # Simulate login by setting the session variable
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()

        # Correct URL name according to your urls.py
        url = reverse('view notifications')  # Make sure this name matches your urls.py

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/notifications.html')
        self.assertContains(response, self.notification.message)  # Check for the message, not the title

    def test_close_notification(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()
        url = reverse('close_notification', args=[self.notification.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/candidates/notifications')
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)

    def test_view_jobs(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()
        url = reverse('view jobs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/viewJobsTemplate.html')

    def test_apply_job_success(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()

        url = reverse('apply_Job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/appliedSuccessTemplate.html')
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

    def test_apply_job_already_applied(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()
        # Apply for the job once
        url = reverse('apply_Job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/appliedSuccessTemplate.html')
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

        # Try applying again for the same job
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view job', args=[self.job.id]))

    def test_view_job(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()

        url = reverse('view job', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/viewJobTemplate.html')
        self.assertContains(response, self.job.position)

    def test_view_resume_without_resume(self):
        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()

        url = reverse('View_Resume')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/candidates/createResume')

    def test_view_resume_with_resume(self):
        self.candidate.resume = self.resume
        self.candidate.save()

        session = self.client.session
        session['c_id'] = self.candidate.id
        session.save()

        url = reverse('View_Resume')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'candidates/resumeDetailTemplate.html')




