# demositex
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import User_Creation_Form

# Register your models here.

class User_Admin(UserAdmin):
    model = User
    add_form = User_Creation_Form
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Roles', 
            {
                'fields': (
                    'is_company',
                    'is_seeker',
                )
            }
        ),
    )    

class Company_Admin(admin.ModelAdmin):
    list_display = ('user', 'cname', 'ctype', 'clocation', 'estd', 'ceo', 'phone', 'logo', 'is_verified')

class Seeker_Admin(admin.ModelAdmin):
    list_display = ('user', 'name', 'sex', 'age', 'dob', 'nationality', 'qualification', 'experience', 'phone', 'address', 'issued_id', 'photo', 'is_verified')

class Post_Admin(admin.ModelAdmin):
    list_display = ('company', 'id', 'published_date', 'title', 'description', 'vacant_for', 'no_of_vacancy')

class CV_Admin(admin.ModelAdmin):
    list_display = ('seeker', 'id', 'cv', 'upload_date')

class Application_Admin(admin.ModelAdmin):
    list_display = ('seeker', 'company', 'post', 'cv_applied', 'apply_date', 'status')

# Final Registration 
admin.site.register(User, User_Admin)
admin.site.register(Company, Company_Admin)
admin.site.register(Seeker, Seeker_Admin)
admin.site.register(Post, Post_Admin)
admin.site.register(CV, CV_Admin)
admin.site.register(Application, Application_Admin)

