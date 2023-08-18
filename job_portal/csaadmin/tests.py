from django.test import TestCase
from django.urls import reverse
from .models import User, Job, Candidate, Employer
from candidate.models import Resume
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual('The lion says "roar"', 'The lion says "roar"')


class CSAAdminViewsTests(TestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_user = User.objects.create(email='admin@example.com', role='A', password = 'adminpassword')
        self.admin_user.save()

        # Create a test non-admin user
        self.non_admin_user = User.objects.create(email='user@example.com', role='C', password = 'userpassword')
        self.non_admin_user.save()

    def test_home_view(self):
        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csaadmin/home.html')

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:home'))
        self.assertRedirects(response, '/')

    def test_list_candidates_view(self):
        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_candidates'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csaadmin/list_candidates.html')

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_candidates'))
        self.assertRedirects(response, '/')

    def test_list_employers_view(self):
        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_employers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csaadmin/list_employers.html')

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_employers'))
        self.assertRedirects(response, '/')

    def test_list_jobs_view(self):
        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csaadmin/list_jobs.html')

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:list_jobs'))
        self.assertRedirects(response, '/')

    def test_delete_job_view(self):
        # Create a test job
        employer_user = User.objects.create(email='employer@example.com', role='E')
        employer = Employer.objects.create(userID=employer_user, companyName='Test Company')

        # Create a test job with an application deadline and employer
        job_application_deadline = date.today()
        job = Job.objects.create(
            position='Test Position',
            description='Test Description',
            status='Open',
            applicationDeadline=job_application_deadline,
            employer=employer
        )
        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_job', kwargs={'job_id': job.id}))
        self.assertRedirects(response, '/csaadmin/list_jobs/')
        self.assertRaises(Job.DoesNotExist, Job.objects.get, pk=job.id)

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_job', kwargs={'job_id': job.id}))
        self.assertRedirects(response, '/')

    def test_delete_employer_view(self):
        # Create a test employer
        employer_user = User.objects.create(email='employer@example.com', role='E')
        employer = Employer.objects.create(userID=employer_user, companyName='Test Company')

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_employer', kwargs={'employer_id': employer.id}))
        self.assertRedirects(response, '/csaadmin/list_employers/')
        self.assertRaises(Employer.DoesNotExist, Employer.objects.get, pk=employer.id)

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_employer', kwargs={'employer_id': employer.id}))
        self.assertRedirects(response, '/')

    def test_delete_candidate_view(self):
        # Create a test candidate
        candidate_user = User.objects.create(email='candidate@example.com', role='C')
        candidate = Candidate.objects.create(user=candidate_user, firstName='Test', lastName='Candidate')

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_candidate', kwargs={'candidate_id': candidate.id}))
        self.assertRedirects(response, '/csaadmin/list_candidates/')
        self.assertRaises(Candidate.DoesNotExist, Candidate.objects.get, pk=candidate.id)

        # Log in as a non-admin user
        session['a_id'] = self.non_admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:delete_candidate', kwargs={'candidate_id': candidate.id}))
        self.assertRedirects(response, '/')
        
    def test_candidate_profile_view(self):
        # Create a test candidate
        candidate_user = User.objects.create(email='candidate@example.com', role='C')
        candidate = Candidate.objects.create(user=candidate_user, firstName='Test', lastName='Candidate')

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:candidate_profile', kwargs={'pk': candidate.id}))
        self.assertEqual(response.status_code, 200)

    def test_employer_profile_view(self):
        # Create a test employer
        employer_user = User.objects.create(email='employer@example.com', role='E')
        employer = Employer.objects.create(userID=employer_user, companyName='Test Company')

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:employer_profile', kwargs={'pk': employer.id}))
        self.assertEqual(response.status_code, 200)

    def test_download_view(self):
        # Create a test resume file
        resume_file = SimpleUploadedFile("resume.txt", b"Resume content")
        resume = Resume.objects.create(summary='Test Resume', file=resume_file)

        # Create a test candidate with the resume
        candidate_user = User.objects.create(email='candidate@example.com', role='C')
        candidate = Candidate.objects.create(user=candidate_user, firstName='Test', lastName='Candidate', resume=resume)

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:download', kwargs={'pk': candidate.id}))
        self.assertEqual(response.status_code, 200)
        file_content = b''.join(response.streaming_content)
        self.assertEqual(file_content, b"Resume content")

    def test_view_resume_view(self):
        # Create a test resume file
        resume_file = SimpleUploadedFile("resume.txt", b"Resume content")
        resume = Resume.objects.create(summary='Test Resume', file=resume_file)

        # Create a test candidate with the resume
        candidate_user = User.objects.create(email='candidate@example.com', role='C')
        candidate = Candidate.objects.create(user=candidate_user, firstName='Test', lastName='Candidate', resume=resume)

        # Log in as an admin user
        session = self.client.session
        session['a_id'] = self.admin_user.id
        session.save()

        response = self.client.get(reverse('csaadmin:view_resume', kwargs={'pk': candidate.id}))
        self.assertEqual(response.status_code, 200)





# Add more test methods to cover other views and scenarios
