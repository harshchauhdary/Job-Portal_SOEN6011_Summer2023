from django.test import TestCase, Client
from django.urls import reverse
from employer.models import Employer, Job
from user.models import User
from candidate.models import Candidate, Application, Notification, Resume
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.parse import urljoin

class EmployerViewsTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(email='employer@example.com', password='password', role='employer')
        
        # Create an employer
        self.employer = Employer.objects.create(
            userID=self.user,
            companyName='ABC Inc.',
            companyEmail='company@example.com',
            firstName='John',
            lastName='Doe',
            phone='1234567890'
        )
        
        # Create a job
        self.job = Job.objects.create(
            position='Software Engineer',
            description='Job description',
            applicationDeadline='2023-12-31',
            status='Open',
            employer=self.employer
        )
        
        self.user2 = User.objects.create(email='employer@examplel.com', password='password', role='candidate')

        # Create a candidate
        self.candidate = Candidate.objects.create(
            firstName='Candidate First Name',
            lastName='Candidate Last Name',
            phone='9876543210',
            user=self.user2
        )
        
        # Create an application
        self.application = Application.objects.create(
            candidate=self.candidate,
            job=self.job,
            status='Applied'
        )


    def test_view_candidate_application(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        # Assuming you've defined the URL name 'view_candidate_application'
        url = reverse('employer:view_candidate_application', args=[self.application.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assuming it should return 200
        # Add more assertions as needed
        
    def test_export_resume_pdf_view(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        # Assuming you've defined the URL name 'export_candidate_resume_pdf'
        url = reverse('employer:export_candidate_resume_pdf', args=[self.candidate.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assuming it should return 200
        # Add more assertions as needed

    def test_accept_application(self):
        # ... Simulate session login and other setup
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        # Assuming you've defined the URL name 'accept_application'
        url = reverse('employer:accept_application', args=[self.application.pk])
        response = self.client.post(url)
        
        # Construct the expected full URL
        expected_redirect_url = f'/employer/browseCandidates/{self.job.pk}'
        
        # Check if the response is a redirect and the location matches the expected URL
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, expected_redirect_url, fetch_redirect_response=False)
        
        # Verify other assertions

    def test_reject_application(self):
        # ... Simulate session login and other setup
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        # Assuming you've defined the URL name 'reject_application'
        url = reverse('employer:reject_application', args=[self.application.pk])
        response = self.client.post(url)
        
        # Construct the expected full URL
        expected_redirect_url = f'/employer/browseCandidates/{self.job.pk}'
        
        # Check if the response is a redirect and the location matches the expected URL
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, expected_redirect_url, fetch_redirect_response=False)
        
        # Verify other assertions
        

    def test_browse_candidates(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()

        # Assuming you've defined the URL name 'browse_candidates'
        url = reverse('employer:browse_candidates', args=[self.job.pk])
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

    def test_add_job(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        url = reverse('employer:add_job')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ... Additional assertions
        
    def test_view_job(self):
        # Create a job owned by the employer
        job = Job.objects.create(
            position='Software Engineer',
            description='Job description',
            applicationDeadline='2023-12-31',
            status='Open',
            employer=self.employer
        )
        
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        url = reverse('employer:view_job', args=[job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ... Additional assertions
        
    def test_update_job(self):
        # Create a job owned by the employer
        job = Job.objects.create(
            position='Software Engineer',
            description='Job description',
            applicationDeadline='2023-12-31',
            status='Open',
            employer=self.employer
        )
        
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        url = reverse('employer:update_job', args=[job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_employer_profile(self):
        # Simulate session login
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        
        url = reverse('employer:create_employer_profile')  # Replace with the actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ... Additional assertions
        
    def test_update_employer_profile(self):
        # Create an employer
        employer = Employer.objects.create(
            userID=self.user,
            companyName='ABC Inc.',
            companyEmail='company@example.com',
            firstName='John',
            lastName='Doe',
            phone='1234567890'
        )
        
        # Simulate session login
        session = self.client.session
        session['e_id'] = employer.id
        session.save()
        
        url = reverse('employer:update_employer_profile')  # Replace with the actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ... Additional assertions
        
    def test_view_employee_profile(self):
        # Create an employer
        employer = Employer.objects.create(
            userID=self.user,
            companyName='ABC Inc.',
            companyEmail='company@example.com',
            firstName='John',
            lastName='Doe',
            phone='1234567890'
        )
        
        # Simulate session login
        session = self.client.session
        session['e_id'] = employer.id
        session.save()
        
        url = reverse('employer:view_employee_profile')  # Replace with the actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_view_employer_profile(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()
        
        # Assuming you've defined the URL name 'view_employer_profile'
        url = reverse('employer:view_employer_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assuming it should return 200
        # Add more assertions as needed

    def test_view_jobs(self):
        # Simulate session login
        session = self.client.session
        session['e_id'] = self.employer.id
        session.save()

        # Create jobs associated with the employer
        job1 = Job.objects.create(
            position='Software Engineer',
            description='Job description',
            applicationDeadline='2023-12-31',
            status='Open',
            employer=self.employer
        )
        job2 = Job.objects.create(
            position='Project Manager',
            description='Job description',
            applicationDeadline='2023-12-31',
            status='Open',
            employer=self.employer
        )

        # Assuming you've defined the URL name 'view_jobs'
        url = reverse('employer:view_jobs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Assuming it should return 200
        # Add more assertions as needed
