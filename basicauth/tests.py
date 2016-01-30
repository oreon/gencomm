from django.test import TestCase


# -*- coding: utf-8 -*-
from django.test import TestCase
 
from django.contrib.auth import get_user_model
from . import models
from patients.models import Patient
 
 
class TestProfileModel(TestCase):
 
    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.patientUser, Patient)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.patientUser, Patient)
