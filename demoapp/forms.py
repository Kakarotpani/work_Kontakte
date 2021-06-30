from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, request

class User_Creation_Form(UserCreationForm):  # Admin view
    class Meta:
        model = User
        fields = "__all__"


class User_Form(forms.ModelForm):   
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets =  {'password': forms.PasswordInput()}
            
    def clean(self):
        cleaned_data = super(User_Form, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
                                            

class Company_Form(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("cname", "ctype", "estd", "ceo", "phone", "clocation", "logo")
        labels = {"cname": "Company Name", "ctype" : "Company Type", "estd": "Estd.", "ceo": "CEO", "phone" : "contact no.", "clocation": "Company Address"}
        


class Seeker_Form(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ("name", "sex", "dob" , "nationality", "qualification", "experience" , "phone", "address", "issued_id", "photo")
                


class Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "description", "vaccant_for", "no_of_vaccancy",)


class CV_Form(forms.ModelForm):
    class Meta:
        model = CV
        fields = ("cv",)
        labels = {'cv': ""}





