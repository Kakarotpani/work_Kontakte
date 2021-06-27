from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.

class User(AbstractUser):
    is_company = models.BooleanField(default = False)
    is_seeker = models.BooleanField(default = False)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = False, null = False)
    cname = models.CharField(max_length = 60, null = True, blank = True)    
    ctype = models.CharField(max_length = 40, null = True, blank = True)  
    clocation = models.CharField(max_length = 40, null = True, blank = True, default = "INDIA") 
    estd = models.PositiveSmallIntegerField( help_text = "(yyyy-mm-dd)",
            validators=[
                MaxValueValidator(timezone.now().year),
                MinValueValidator(1900)
            ]
    )
    ceo = models.CharField(max_length = 30, editable=True, blank=False, null=False)
    phone = PhoneNumberField(max_length = 15, default = '+91', blank = True, null = True)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.cname
       

class Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = False, null = False)
    name = models.CharField(max_length = 60, blank = False, null = False)
    sex = models.CharField(max_length = 6, blank=False, null=False)
    age = models.PositiveIntegerField(blank=False, null=False)
    dob = models.DateField(auto_now=False, auto_now_add=False, help_text = "(yyyy-mm-dd)")
    nationality = models.CharField(max_length = 30, blank=False, null=False)
    qualification = models.TextField(max_length=150, blank=False, null=False)
    experience = models.FloatField(blank=True, null=True)
    phone = PhoneNumberField(max_length = 15, default = '+91', blank = True, null = True)
    address = models.TextField(max_length=150, blank=False, null=False)
    issued_id = models.CharField(max_length = 20, blank=False, null=False)
    photo = models.ImageField(blank=True, null=True, upload_to = 'seeker_dp')
    is_verified = models.BooleanField(default = True)

    def __str__(self):  
        return self.user.username

class CV(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    cv = models.ImageField(blank=True, null=True, upload_to = 'seeker_cv')
    upload_date = models.DateTimeField(auto_now_add=True, null= True, blank = True)
    

class Post(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    published_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length = 40, blank=False, null=False)
    description = models.TextField(max_length= 200, blank=False, null=False)
    vaccant_for = models.CharField(max_length = 40, blank=False, null=False)
    no_of_vaccancy = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete= models.CASCADE, blank = False, null = False)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = False, null = False)
    company = models.ForeignKey(Company, on_delete= models.CASCADE, blank = False, null = False)
    cv_applied= models.ForeignKey(CV, on_delete = models.CASCADE, null = True, blank = True)
    apply_date = models.DateTimeField(auto_now_add=True)    
    status = models.BooleanField(default = False)
    
    def __str__(self):
        return self.seeker.name
    