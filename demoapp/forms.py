from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from django.core import validators
from django.http import request

class User_Creation_Form(UserCreationForm):  # Admin 
    class Meta:
        model = User
        fields = "__all__"    

class User_Form(forms.ModelForm):   
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username", "email", "password")
        help_texts = {"username": ""}
        widgets =  {'password': forms.PasswordInput()}  

    def clean_username(self):
        username = self.cleaned_data['username']        
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("username already exists !!")
        return username

    def clean(self):
        cleaned_data = super(User_Form, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match"            )
                                                 

class Company_Form(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("cname", "ctype", "estd", "ceo", "phone", "clocation", "logo")
        labels = {"cname": "Company Name", "ctype" : "Company Type", "estd": "Estd.", "ceo": "CEO",
                  "phone" : "contact no.", "clocation": "Company Address", "logo": "logo -"}
        widgets = {
            'estd': forms.TextInput(attrs={'placeholder': '(yyyy)'}),
        }


class Seeker_Form(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ("name", "sex", "dob" , "nationality", "qualification", "experience" , "phone", "address", "issued_id", "photo")
        labels = {"photo": "photo -",}
        widgets = {
            'issued_id': forms.TextInput(attrs={'placeholder': 'national-identity'}),
            'dob': forms.TextInput(attrs={'placeholder': '(yyyy-mm-dd)'}),
            'sex': forms.TextInput(attrs={'placeholder': 'male/female/other'}),
            'experience': forms.TextInput(attrs={'placeholder': ' in year :'}),            
        }  
    

class Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "description", "vacant_for", "no_of_vacancy",)
        labels = {"no_of_vaccancy": "No. of Vaccancy"}


class CV_Form(forms.ModelForm):
    class Meta:
        model = CV
        fields = ("cv",)
        labels = {'cv': ""}





