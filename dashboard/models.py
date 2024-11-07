from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    terms_agreed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Create your models here.

class CustomUser(AbstractUser):
    date_joined = models.DateField(null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    address=models.TextField(blank=True,null=True)
    mobile=models.CharField(max_length=15,null=True,blank=True)
    position=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.username




class Customers(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('Business','Business'),
        ('Individual','Individual')
    ]

    SALUTATION_CHOICES = [
        ('Mr','Mr'),
        ('Ms','Ms'),
        ('Mrs','Mrs')
    ]

    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES,blank=False, null=False)
    salutation = models.CharField(max_length=20, choices=SALUTATION_CHOICES, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    customer_display_name = models.CharField(max_length=100, blank=False, null=False)
    contact_number = models.CharField(max_length=15, blank=False, null=False)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    country_code_mobile = models.CharField(max_length=5, blank=True, null=True)
    country_code_whatsapp = models.CharField(max_length=5, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.full_name}'





# class Leads(models.Model):
#     MEDIUM_CHOICES = [
#         ('Instagram','Instagram'),
#         ('Facebook','Facebook'),
#         ('Youtube','Youtube'),
#         ('Others', 'Others'),
#     ]
#
#     full_name=models.CharField(max_length=200,blank=True,null=True)
#     medium=models.CharField(choices=MEDIUM_CHOICES,max_length=100,blank=True,null=True)
#     email=models.EmailField(blank=True,null=True)
#     mobile=models.CharField(max_length=20,blank=True,null=True)
#     place=models.CharField(max_length=200,null=True,blank=True)
#     remarks=models.CharField(max_length=200,null=True,blank=True)
#     lead_date = models.DateTimeField(default=timezone.now)
#
#     answer1 = models.CharField(max_length=250, null=True, blank=True)
#     answer2 = models.CharField(max_length=250, null=True, blank=True)
#     answer3 = models.CharField(max_length=250, null=True, blank=True)
#     answer4 = models.CharField(max_length=250, null=True, blank=True)
#     answer5 = models.CharField(max_length=250, null=True, blank=True)
#     answer6 = models.CharField(max_length=250, null=True, blank=True)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
#     attended_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return self.full_name

class Leads(models.Model):
    MEDIUM_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    status=models.CharField(choices=MEDIUM_CHOICES,max_length=100,blank=True,null=True)
    description = models.TextField()
    attended_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





# class Notification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
#     ticket = models.ForeignKey(Ticket, related_name='notifications', on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Notification for {self.user.username} - Ticket {self.ticket.id}"




