import re
import pytest, pytest_django
import datetime
from allauth.account.models import EmailAddress
from rest_framework import status, serializers
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken
from users.factories import UserFactory
from factory import PostGenerationMethodCall
from django.core import mail
from django.contrib.auth import get_user_model


class UserauthTests(APITestCase):


    def setUp(self):
        #since the factories haven't been re-written, we're hardcoding here
        self.user = {
                "username": 'PetuniaPiglet',
                "email": 'Petunia@thepiggyfarm.net',
                "password1":  'codebuddies',
                "password2": 'codebuddies'
                }

    def test_registration_get(self):
        """Ensure that a GET request is not accepted for the endpoint."""

        url = '/api/v1/auth/registration/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], "Method \"GET\" not allowed.")

    def test_registration_post(self):
        """Ensure that a user is created  in the db and a validation email message is returned upon user registering."""

        url = '/api/v1/auth/registration/'
        data = {
                "username": self.user['username'],
                "email": self.user['email'],
                "password1":  self.user['password1'],
                "password2": self.user['password2']
                }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "Verification e-mail sent.")

    def test_registered_user_creation(self):
        """Test that a registration POST creates a user in the DB."""

        url = '/api/v1/auth/registration/'
        data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        response = self.client.post(url, data, format='json')
        model = get_user_model()
        new_user = model.objects.get(username=self.user['username'])

        assert new_user.username == self.user['username']
        assert new_user.email == self.user['email']

    def test_registration_emailaddress_validation_email(self):
        """Ensure that a validation email is sent upon user registering."""

        url = '/api/v1/auth/registration/'
        data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "Verification e-mail sent.")

        # did Django actually send an email?
        assert len(mail.outbox) == 1, "Inbox is not empty"

    def test_validation_email_content(self):
        # start by registering a user
        url = '/api/v1/auth/registration/'
        data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }
        response = self.client.post(url, data, format='json')

        #is the email subject what we expect it to be?
        verify_email_message = mail.outbox[0]
        self.assertEqual(verify_email_message.subject, 'Codebuddies: Please Confirm Your E-mail Address')

        #extracting what we need for the verification link
        uri_regex = re.compile(r"(\/api\/v1\/auth\/registration\/verify-email\/)(\?key=)([\w:-]+)")
        confirmation_uri = re.search(uri_regex, verify_email_message.body)

        # is the uri for the verification link correct?
        verification_path = "/api/v1/auth/registration/verify-email/"
        self.assertEqual(confirmation_uri[1], verification_path)

    def test_verify_email_path_get(self):
        """Ensure that a GET request is not accepted for the endpoint."""

        url = '/api/v1/auth/registration/verify-email/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], "Method \"GET\" not allowed.")


    @pytest.mark.django_db(transaction=True)
    def test_verify_email_path_post(self):

        # start by registering a user
        new_user_reg_url = '/api/v1/auth/registration/'
        new_user_reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }
        response = self.client.post(new_user_reg_url, new_user_reg_data, format='json')

        # grab email from outbox so we can extract the verification link
        email_message = mail.outbox[0]
        verify_email_message = email_message.body

        # extracting what we need for the verification post action
        uri_regex = re.compile(r"(\/api\/v1\/auth\/registration\/verify-email\/)(\?key=)([\w:-]+)")
        confirmation_uri = re.search(uri_regex, verify_email_message)

        # now, let's post the key to trigger validation
        validate_email_url = f'{confirmation_uri[0]}'
        validate_key_data = {"key": confirmation_uri[3]}
        validation_response = self.client.post(validate_email_url, validate_key_data, format='json')
        print(validation_response)

        # did the post result in the correct status messages?
        self.assertEqual(validation_response.status_code, status.HTTP_200_OK)
        self.assertEqual(validation_response.data["detail"], "ok")


    @pytest.mark.django_db(transaction=True)
    def test_verify_email_marked_valid_after_post(self):

        #start by registering a user
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }
        response = self.client.post(reg_url, reg_data, format='json')

        #grab email from outbox so we can extract the verification link
        verify_email_message = mail.outbox[0]

        #extracting what we need for the verification post action
        uri_regex = re.compile(r"(\/api\/v1\/auth\/registration\/verify-email\/)(\?key=)([\w:-]+)")
        confirmation_uri = re.search(uri_regex, verify_email_message.body)


        #now, let's post the key to trigger validation
        email_url = '/api/v1/auth/registration/verify-email/'
        key_data = {"key": confirmation_uri[3]}
        response = self.client.post(email_url, key_data, format='json')


        #did the post succeed in marking the email as valid in the DB?
        model = get_user_model()
        email_to_verify = EmailAddress.objects.get(email=reg_data['email'])
        user = model.objects.get(pk=email_to_verify.user_id)

        self.assertEqual(email_to_verify.verified, True)

    def test_login_with_unverified_email(self):

        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        reg_response = self.client.post(reg_url, reg_data, format='json')

        login_url = '/api/v1/auth/login/'
        login_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password": self.user['password1']
        }

        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ["E-mail is not verified."])


    @pytest.mark.django_db(transaction=True)
    def test_login_with_verified_email(self):

        #first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        email_to_verify = EmailAddress.objects.get(email=reg_data['email'])

        #we set the verified flag to True for the account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        #we grab the user object based on the updated email for use in logging in
        user = model.objects.get(pk=email_to_verify.user_id)

        #we login via the login endpoint
        login_url = '/api/v1/auth/login/'
        login_data = {
            "username": user.username,
            "email": user.email,
            "password": "codebuddies",
        }
        response = self.client.post(login_url, login_data, format='json')

        #we validate that the user we posted is logged in, and an access_token and refresh_token are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], user.email)
        self.assertEqual(response.data['user']['username'], user.username)
        self.assertContains(response, "access_token")
        self.assertContains(response, "refresh_token")


    @pytest.mark.django_db(transaction=True)
    def test_login_bad_password(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        # next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        email_to_verify = EmailAddress.objects.get(email=reg_data['email'])

        # we set the verified flag to True for the account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        # we grab the user object based on the updated email for use in logging in
        user = model.objects.get(pk=email_to_verify.user_id)

        #we attempt a login via the login endpoint, but with a bad password
        login_url = '/api/v1/auth/login/'
        login_data = {
            "username": user.username,
            "email": user.email,
            "password": "bad_password",
        }
        response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ["Unable to log in with provided credentials."])


    @pytest.mark.django_db(transaction=True)
    def test_logout_get(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        # next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        email_to_verify = EmailAddress.objects.get(email=reg_data['email'])

        # we set the verified flag to True for the account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        # we grab the user object based on the updated email for use in logging in
        user = model.objects.get(pk=email_to_verify.user_id)

        #we login via the login endpoint
        login_url = '/api/v1/auth/login/'
        login_data = {
            "username": user.username,
            "email": user.email,
            "password": "codebuddies",
        }
        response = self.client.post(login_url, login_data, format='json')

        #next, we try to logout using GET
        logout_url = '/api/v1/auth/logout/'

        response = self.client.get(logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], "Method \"GET\" not allowed.")


    @pytest.mark.django_db(transaction=True)
    def test_logout_post(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        # next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        email_to_verify = EmailAddress.objects.get(email=reg_data['email'])

        # we set the verified flag to True for the account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        # we grab the user object based on the updated email for use in logging in
        user = model.objects.get(pk=email_to_verify.user_id)

        #we login via the login endpoint
        login_url = '/api/v1/auth/login/'
        login_data = {
            "username": user.username,
            "email": user.email,
            "password": "codebuddies",
        }
        response = self.client.post(login_url, login_data, format='json')

        #next, we trigger logout and verify
        logout_url = '/api/v1/auth/logout/'

        response = self.client.post(logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Successfully logged out.")

    def test_password_reset_request_get(self):
        """Ensure that a GET request is not accepted for the endpoint."""

        url = '/api/v1/auth/password/reset/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], "Method \"GET\" not allowed.")


    def test_password_reset_request_post(self):
        """Ensure that a password reset email is sent upon POST to reset endpoint."""

        reset_url = '/api/v1/auth/password/reset/'
        reset_data = {"email": self.user['email']}

        response = self.client.post(reset_url, reset_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Password reset e-mail has been sent.")


    @pytest.mark.django_db(transaction=True)
    def test_password_reset_email_sent(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_data = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_data, format='json')

        # did Django actually send an email?
        assert len(mail.outbox) == 1, "Inbox is not empty"


    @pytest.mark.django_db(transaction=True)
    def test_passowrd_reset_email_content(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_data = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_data, format='json')

        # is the email subject and addressee what we expect them to be?
        reset_email_message = mail.outbox[0]
        self.assertEqual(reset_email_message.subject, 'Password reset on CBV3 Django Prototype')
        self.assertEqual(reset_email_message.to[0], user_to_reset.email)

        # extracting what we need for the reset link
        reset_uri_regex = re.compile(r"(\/api\/v1\/auth\/password\/reset\/confirm\/)([A-Z]+)([\w:-]+)")
        reset_uri = re.search(reset_uri_regex, reset_email_message.body)

        # is the uri for the verification link correct?
        reset_path = "/api/v1/auth/password/reset/confirm/"
        self.assertEqual(reset_uri[1], reset_path)


    @pytest.mark.django_db(transaction=True)
    def test_password_reset_path_get(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_data = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_data, format='json')

        # extracting what we need for the reset link
        reset_email_message = mail.outbox[0]
        reset_uri_regex = re.compile(r"(\/api\/v1\/auth\/password\/reset\/confirm\/)([\w]+)\/([\w:-]+)\/")
        reset_uri = re.search(reset_uri_regex, reset_email_message.body)

        # now we hit the uri with the info, but as a GET
        password_reset_confirm_uri = f"/api/v1/auth/password/reset/confirm/{reset_uri[2]}/{reset_uri[3]}/"
        reset_response = self.client.get(password_reset_confirm_uri)

        self.assertEqual(reset_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(reset_response.data['detail'], "Method \"GET\" not allowed.")


    @pytest.mark.django_db(transaction=True)
    def test_password_reset_post(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_email_address = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_email_address, format='json')

        # extracting what we need for the reset link
        reset_email_message = mail.outbox[0]
        reset_uri_regex = re.compile(r"(\/api\/v1\/auth\/password\/reset\/confirm\/)([\w]+)\/([\w:-]+)\/")
        reset_uri = re.search(reset_uri_regex, reset_email_message.body)
        reset_uid = reset_uri[2]
        reset_token = reset_uri[3]

        # now we POST to the uri with the UID, TOKEN and the reset data
        password_reset_confirm_uri = f"/api/v1/auth/password/reset/confirm/{reset_uid}/{reset_token}/"
        password_reset_confirm_data = {
            "new_password1": "codebuddies_II",
            "new_password2": "codebuddies_II",
            "uid": reset_uid,
            "token": reset_token
        }

        password_reset_confirm_response = self.client.post(password_reset_confirm_uri, password_reset_confirm_data, format='json')
        self.assertEqual(password_reset_confirm_response.status_code, status.HTTP_200_OK)
        self.assertEqual(password_reset_confirm_response.data['detail'], "Password has been reset with the new password.")


    @pytest.mark.django_db(transaction=True)
    def test_password_reset_db_change(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_email_address = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_email_address, format='json')

        # extracting what we need for the reset link
        reset_email_message = mail.outbox[0]
        reset_uri_regex = re.compile(r"(\/api\/v1\/auth\/password\/reset\/confirm\/)([\w]+)\/([\w:-]+)\/")
        reset_uri = re.search(reset_uri_regex, reset_email_message.body)
        reset_uid = reset_uri[2]
        reset_token = reset_uri[3]

        # now we POST to the uri with the UID, TOKEN and the reset data
        password_reset_confirm_uri = f"/api/v1/auth/password/reset/confirm/{reset_uid}/{reset_token}/"
        password_reset_confirm_data = {
            "new_password1": "codebuddies_II",
            "new_password2": "codebuddies_II",
            "uid": reset_uid,
            "token": reset_token
        }

        password_reset_confirm_response = self.client.post(password_reset_confirm_uri, password_reset_confirm_data, format='json')
        self.assertEqual(password_reset_confirm_response.status_code, status.HTTP_200_OK)
        self.assertEqual(password_reset_confirm_response.data['detail'], "Password has been reset with the new password.")


    @pytest.mark.django_db(transaction=True)
    def test_login_with_reset_password(self):

        # first we register through the registration endpoint
        reg_url = '/api/v1/auth/registration/'
        reg_data = {
            "username": self.user['username'],
            "email": self.user['email'],
            "password1": self.user['password1'],
            "password2": self.user['password2']
        }

        self.client.post(reg_url, reg_data, format='json')

        #next, we clean out the email outbox
        mail.outbox.clear()

        #next, we retrieve the newly created user model and their corresponding account_emailaddress
        model = get_user_model()
        user_to_reset = model.objects.get(username=reg_data['username'])
        email_to_verify = EmailAddress.objects.get(email=user_to_reset.email)

        # we set the verified flag to True for the reset_user_account_emailaddress and save
        email_to_verify.verified = 1
        email_to_verify.save()

        reset_url = '/api/v1/auth/password/reset/'
        reset_email_address = {"email": email_to_verify.email}
        response = self.client.post(reset_url, reset_email_address, format='json')

        # extracting what we need for the reset link
        reset_email_message = mail.outbox[0]
        reset_uri_regex = re.compile(r"(\/api\/v1\/auth\/password\/reset\/confirm\/)([\w]+)\/([\w:-]+)\/")
        reset_uri = re.search(reset_uri_regex, reset_email_message.body)
        reset_uid = reset_uri[2]
        reset_token = reset_uri[3]

        # now we POST to the uri with the UID, TOKEN and the reset data
        password_reset_confirm_uri = f"/api/v1/auth/password/reset/confirm/{reset_uid}/{reset_token}/"
        password_reset_confirm_data = {
            "new_password1": "codebuddies_II",
            "new_password2": "codebuddies_II",
            "uid": reset_uid,
            "token": reset_token
        }

        self.client.post(password_reset_confirm_uri, password_reset_confirm_data, format='json')


        #finally, we attempt a login with the newly reset password
        new_login_uri = '/api/v1/auth/login/'
        new_login_data = {
            "username": user_to_reset.username,
            "email": user_to_reset.email,
            "password": "codebuddies_II",
        }

        new_login_response = self.client.post(new_login_uri, new_login_data, format='json')

        # finally, we validate that the user we posted is
        # logged in with the new password and an access_token and refresh_token are returned
        self.assertEqual(new_login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_login_response.data['user']['email'], user_to_reset.email)
        self.assertEqual(new_login_response.data['user']['username'], user_to_reset.username)
        self.assertContains(new_login_response, "access_token")
        self.assertContains(new_login_response, "refresh_token")

    @pytest.mark.django_db(transaction=True)
    def test_view_user_details_authed(self):

        token_uri = '/api/v1/auth/token/'
        user_to_view = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_auth_data = {
            "username": user_to_view.username,
            "password": 'codebuddies'
        }

        authed_user_tokens = self.client.post(token_uri, user_auth_data, format='json')
        authed_user_access_token = authed_user_tokens.data['access']
        authed_user_refresh_token = authed_user_tokens.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + authed_user_access_token)

        user_details_uri = '/api/v1/auth/user/'
        user_details_response = self.client.get(user_details_uri)

        self.assertEqual(user_details_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_details_response.data['username'], user_to_view.username)

    def test_view_user_details_unauthed(self):

        details_uri = '/api/v1/auth/user/'

        details_response = self.client.get(details_uri)
        self.assertEqual(details_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(details_response.data['detail'], "Authentication credentials were not provided.")

    def test_current_user_method_authed(self):

        token_uri = '/api/v1/auth/token/'
        user_to_auth = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_to_auth_data = {
            "username": user_to_auth.username,
            "password": 'codebuddies'
        }

        authed_user_tokens = self.client.post(token_uri, user_to_auth_data, format='json')
        authed_user_access_token = authed_user_tokens.data['access']
        authed_user_refresh_token = authed_user_tokens.data['refresh']
        authed_user_uri = '/api/v1/auth/current_user/'

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + authed_user_access_token)
        current_user_request = self.client.get(authed_user_uri)

        #do we get back the "current users" view info?
        self.assertEqual(current_user_request.status_code, status.HTTP_200_OK)
        self.assertEqual(current_user_request.data['username'], user_to_auth.username)
        self.assertContains(current_user_request, 'is_superuser')
        self.assertContains(current_user_request, 'last_name')
        self.assertContains(current_user_request, 'id')

    def test_current_user_method_unauthed(self):

        unauthed_user_uri = '/api/v1/auth/current_user/'

        unauthed_current_user_request = self.client.get(unauthed_user_uri)

        #do we get rejcted by the api?
        self.assertEqual(unauthed_current_user_request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_JWTtoken_obtain_pair(self):
        token_uri = '/api/v1/auth/token/'
        user_to_auth = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_auth_data = {
            "username": user_to_auth.username,
            "password": 'codebuddies'
        }

        JWT_user_tokens = self.client.post(token_uri, user_auth_data, format='json')
        self.assertEqual(JWT_user_tokens.status_code, status.HTTP_200_OK)
        self.assertContains(JWT_user_tokens,  "access")
        self.assertContains(JWT_user_tokens, "refresh")

    def test_JWTtoken_verify_active_access_token(self):

        token_uri = '/api/v1/auth/token/'
        user_to_validate = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_validate_data = {
            "username": user_to_validate.username,
            "password": 'codebuddies'
        }

        JWT_user_validate_tokens = self.client.post(token_uri, user_validate_data, format='json')

        # now we validate the token
        validation_uri = '/api/v1/auth/token/verify/'
        data_to_validate = {
            "token": JWT_user_validate_tokens.data['access'],
        }

        validated_token = self.client.post(validation_uri, data_to_validate, format='json')
        self.assertEqual(validated_token.status_code, status.HTTP_200_OK)

    def test_JWTtoken_verify_active_refresh_token(self):

        token_uri = '/api/v1/auth/token/'
        user_to_validate = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_validate_data = {
            "username": user_to_validate.username,
            "password": 'codebuddies'
        }

        JWT_user_validate_tokens = self.client.post(token_uri, user_validate_data, format='json')

        # now we validate the token
        validation_uri = '/api/v1/auth/token/verify/'
        data_to_validate = {
            "token": JWT_user_validate_tokens.data['refresh'],
        }

        validated_token = self.client.post(validation_uri, data_to_validate, format='json')
        self.assertEqual(validated_token.status_code, status.HTTP_200_OK)

    def test_JWTtoken_verify_with_expired_access_token(self):

        #make a user to auth
        user_to_expire = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        #make a date that's yesterday
        today = datetime.datetime.now()
        diff = datetime.timedelta(days=1)
        start_time = today - diff

        #now we manually create a token with our user and a token that expired yesterday
        expired_token = AccessToken.for_user(user_to_expire)
        expired_token.set_exp(from_time=start_time)

        # now we attempt to validate the expired token
        expiration_validation_uri = '/api/v1/auth/token/verify/'
        data_to_validate_expired = {"token": str(expired_token),}
        expired_token_response = self.client.post(expiration_validation_uri, data_to_validate_expired, format='json')


        #did we get rejected by the API?
        self.assertEqual(expired_token_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expired_token_response.data['detail'], "Token is invalid or expired")
        self.assertEqual(expired_token_response.data['code'], "token_not_valid")

    def test_JWTtoken_verify_with_expired_refresh_token(self):

        #make a user to auth
        user_to_expire_refresh = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        #make a date that's yesterday
        today = datetime.datetime.now()
        diff = datetime.timedelta(days=1)
        start_time = today - diff

        #now we manually create a token with our user and a token that expired yesterday
        expired_refresh_token = RefreshToken.for_user(user_to_expire_refresh)
        expired_refresh_token.set_exp(from_time=start_time)

        # now we attempt to validate the expired token
        expiration_validation_uri = '/api/v1/auth/token/verify/'
        data_to_validate_expired_refresh = {"token": str(expired_refresh_token),}
        expired_token_response = self.client.post(expiration_validation_uri, data_to_validate_expired_refresh, format='json')


        #did we get rejected by the API?
        self.assertEqual(expired_token_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expired_token_response.data['detail'], "Token is invalid or expired")
        self.assertEqual(expired_token_response.data['code'], "token_not_valid")

    def test_JWTtoken_refresh_access_token_with_active_refresh_token(self):
        token_uri = '/api/v1/auth/token/'
        user_to_refresh = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_refresh_data = {
            "username": user_to_refresh.username,
            "password": 'codebuddies'
        }

        JWT_user_obtain_tokens = self.client.post(token_uri, user_refresh_data, format='json')

        #now we call refresh with the active refresh token
        refresh_uri = '/api/v1/auth/token/refresh/'
        data_to_refresh = {
            "refresh": JWT_user_obtain_tokens.data['refresh'],
        }

        renewed_token = self.client.post(refresh_uri, data_to_refresh, format='json')

        # Did we get a new access token in exchange for the refresh request?
        self.assertEqual(renewed_token.status_code, status.HTTP_200_OK)
        self.assertContains(renewed_token, "access")

    def test_JWTtoken_refresh_access_token_with_active_access_token(self):
        token_uri = '/api/v1/auth/token/'
        user_to_refresh_access = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))
        user_refresh_access_data = {
            "username": user_to_refresh_access.username,
            "password": 'codebuddies'
        }

        JWT_user_obtain_tokens_to_refresh = self.client.post(token_uri, user_refresh_access_data, format='json')

        #now we call refresh with the active refresh token
        refresh_uri = '/api/v1/auth/token/refresh/'
        access_data_to_refresh = {
            "refresh": JWT_user_obtain_tokens_to_refresh.data['access'],
        }

        renewed_access_token = self.client.post(refresh_uri, access_data_to_refresh, format='json')

        # Did we get rejected from refresh request due to it being an access token?
        self.assertEqual(renewed_access_token.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_JWTtoken_refresh_expired_access_token_with_expired_access_token(self):

        # make a user to auth
        user_to_expire_refresh = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        # make a date that's yesterday
        today = datetime.datetime.now()
        diff = datetime.timedelta(days=1)
        start_time = today - diff

        # now we manually create a token with our user and a token that expired yesterday
        expired_token = AccessToken.for_user(user_to_expire_refresh)
        expired_token.set_exp(from_time=start_time)

        # now we attempt to validate the expired token
        expiration_refresh_uri = '/api/v1/auth/token/refresh/'
        data_to_refresh_expired = {"refresh": str(expired_token), }
        expired_refresh_response = self.client.post(expiration_refresh_uri, data_to_refresh_expired, format='json')

        # did we get rejected by the API?
        self.assertEqual(expired_refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(expired_refresh_response.data['detail'], "Token is invalid or expired")
        self.assertEqual(expired_refresh_response.data['code'], "token_not_valid")

    def test_JWTtoken_refresh_expired_access_token_with_valid_refresh_token(self):
        # make a user to auth
        user_to_refresh = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        # make a date that's yesterday
        today = datetime.datetime.now()
        diff = datetime.timedelta(days=1)
        diff_refresh = datetime.timedelta(hours=1)
        start_time = today - diff
        start_time_refresh = today + diff_refresh


        # now we manually create a access token with our user and a token that expired yesterday
        expired_token = AccessToken.for_user(user_to_refresh)
        expired_token.set_exp(from_time=start_time)

        # next, we manually crate a valid refresh token with our user and a now() date
        refresh_token = RefreshToken.for_user(user_to_refresh)
        refresh_token.set_exp(from_time=start_time_refresh)

        # now we attempt to refresh the expired access token with the refresh token
        expiration_refresh_uri = '/api/v1/auth/token/refresh/'
        data_to_refresh_expired = {"refresh": str(refresh_token), }
        refresh_response = self.client.post(expiration_refresh_uri, data_to_refresh_expired, format='json')

        # did we get a new, valid access token from the API?
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertContains(refresh_response, 'access')

    def test_JWTtoken_refresh_expired_access_token_with_expired_refresh_token(self):
        # make a user to auth
        user_to_refresh = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        # make a date that's yesterday
        today = datetime.datetime.now()
        diff = datetime.timedelta(days=1)
        start_time = today - diff
        start_time_refresh_past = today - diff

        # now we manually create a access token with our user and a token that expired yesterday
        expired_token = AccessToken.for_user(user_to_refresh)
        expired_token.set_exp(from_time=start_time)

        # next, we manually crate a refresh token with our user and a now() date
        past_refresh_token = RefreshToken.for_user(user_to_refresh)
        past_refresh_token.set_exp(from_time=start_time_refresh_past)

        # now we attempt to refresh the expired access token with the refresh token
        expiration_refresh_uri = '/api/v1/auth/token/refresh/'
        data_to_refresh_past = {"refresh": str(past_refresh_token), }
        past_refresh_response = self.client.post(expiration_refresh_uri, data_to_refresh_past, format='json')

        # did we get rejected because the refresh token has expired?
        self.assertEqual(past_refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(past_refresh_response.data['detail'], "Token is invalid or expired")
        self.assertEqual(past_refresh_response.data['code'], "token_not_valid")
