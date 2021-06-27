from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import Group
from django.views.generic import View
from .models import *
from django.utils import timezone
from demosite import settings
from django.contrib import messages
from django.db.models import Q
from itertools import chain


# Create your views here.


def base(request):
    posts = Post.objects.filter(company__is_verified='True').order_by('-published_date')[:4]
    return render(request, 'base.html', {'posts': posts})

def all_posts(request):
    posts = Post.objects.filter(company__is_verified='True').order_by('-published_date')
    return render(request, 'base.html', {'posts': posts})

def login_method(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                u = user.username
                print(u, " : Logged in")                                
                if user.is_company:                    
                    messages.success(request, '* Logged in as a company !!')
                    return HttpResponseRedirect('/company/dashboard')
                if user.is_seeker:                    
                    messages.success(request, "*  Logged in as an Applicant !!")
                    return HttpResponseRedirect('/seeker/dashboard')
                else:
                    messages.success(request, "* Logged in as Admin !!")
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, "User doesn't exist.")
                return HttpResponseRedirect('/login')
        else:
            messages.warning(request, "* INVALID CREDENTIALS !!")
            return HttpResponseRedirect('/login')
    else:
        return render(request, 'login_form.html')


@login_required
def logout_method(request):
    logout(request)
    messages.success(request, "* Successfully Logged out !!")
    return HttpResponseRedirect('/login')


def company_register(request):
    registered = False
    if request.method == 'POST':
        user_form = User_Form(request.POST)
        profile_form = Company_Form(request.POST)       
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            # Company Permisssions
            group = Group.objects.get(name="company")
            user.groups.add(group)
            user.is_company = True
            user.save()
            # Additional fields
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            messages.success(request, "* Successfully Registered as a Company .......")
            return HttpResponseRedirect('/login')            
        else:
            messages.error(request,"* Invalid data . Try Again !!")
            return HttpResponseRedirect('/register/company')
    else:
        context = {
            'user_form' : User_Form(),
            'profile_form' : Company_Form(), 
            'registered' : registered
        }
    return render(request, 'company_register.html',  context = context)


def seeker_register(request):
    registered = False
    if request.method == 'POST':
        user_form = User_Form(request.POST)
        profile_form = Seeker_Form(request.POST, request.FILES)        
        if user_form.is_valid() and profile_form.is_valid():             
            user = user_form.save()
            user.set_password(user.password)
            # Seeker Permissions
            group = Group.objects.get(name="seeker")
            user.groups.add(group)
            user.is_seeker = True
            user.save()
            # Additional fields
            profile = profile_form.save(commit=False)
            # age calculation
            profile.age = (datetime.datetime.now().year - profile.dob.year)
            profile.user = user
            profile.save()
            registered = True
            messages.success(request, "* Successfully Registered as an Applicant .......")
            return HttpResponseRedirect('/login')
        else:
            messages.error(request,"* Invalid data . Try Again !!")
            return HttpResponseRedirect('/register/seeker')
    else:
        context = {
            'user_form' : User_Form(),
            'profile_form' : Seeker_Form(),
            'registered' : registered 
        }        
    return render(request, 'seeker_register.html', context = context)

# DashBoard

@login_required(login_url='/login')
def company_dash(request):
    if request.user.is_company:
        return render(request, 'company_dash.html')

@login_required(login_url='/login')
def seeker_dash(request):
    if request.user.is_seeker:
        return render(request, 'seeker_dash.html')

# Profile CRUD

@login_required(login_url='/login')
def profile_view(request):
    if request.user.is_company:
        company = Company.objects.get(user=request.user)
        return render(request, 'company_profile.html', {'company': company})
    elif request.user.is_seeker:
        seeker = Seeker.objects.get(user=request.user)            
        return render(request, 'seeker_profile.html', {'seeker': seeker})
    else:
        messages.error(request,"* U r not authenticated !!")  
        return HttpResponseRedirect('/')  


@login_required(login_url='/login')
def profile_update(request):
    if request.user.is_company:
        company = Company.objects.get(user = request.user)
        company_profile = Company_Form(instance = company)
        a_company = True
        if request.method == "POST":
            data = Company_Form(data = request.POST, instance = company)
            if data.is_valid():
                data.save(commit = True)
                messages.success(request, "* Profile Updated successfully .....")
                return HttpResponseRedirect('/profile/view')
            else:
                messages.error(request,"* Invalid data . Try Again !!")
                return HttpResponseRedirect('/profile/update')   
        context = {
            'company_profile':company_profile,
            'a_company': a_company
        }
        return render(request, 'profile_update.html', context = context)

    elif request.user.is_seeker:
        seeker = Seeker.objects.get(user = request.user)
        seeker_profile = Seeker_Form(instance = seeker)
        a_seeker = True
        if request.method == "POST":
            data = Seeker_Form(request.POST, request.FILES, instance = seeker)
            if data.is_valid():
                data.save(commit = True)       
                messages.success(request, "* Profile Updated successfully !!")        
                return HttpResponseRedirect('/profile/view')
            else:
                messages.error(request,"* Invalid data . Try Again !!")
                return HttpResponseRedirect('/profile/update')
        context = {
            'seeker_profile': seeker_profile, 
            'a_seeker': a_seeker
        }
        return render(request, 'profile_update.html', context = context)
    else:
        messages.error(request, "you are not Authenticated !!")
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def profile_delete(request):
    if request.method == "GET":
        if request.user.is_company:
            user = User.objects.get(username = request.user)
            company = Company.objects.get(user = user)
            posts = Post.objects.filter(company = company)
            logout(request)  
            user.delete()
            posts.delete()
            company.delete()    
            messages.success(request, "your account was successfully deleted .")
            return HttpResponseRedirect('/')   

        elif request.user.is_seeker:
            user = User.objects.get(username = request.user)
            seeker = Seeker.objects.get(user = request.user)
            cv = CV.objects.filter(seeker = seeker)
            logout(request)
            user.delete()
            cv.delete()
            seeker.delete()
            messages.success(request, "your account was successfully deleted .")
            return HttpResponseRedirect('/')
            
        else:
            messages.error(request, "you are not Eligible .")
            return HttpResponseRedirect('/')

# POST CRUD

@login_required(login_url='/login')
def post_read_all(request):
    if request.method == "GET":
        if request.user.is_company:
            company = Company.objects.get(user=request.user)
            post = Post.objects.filter(company=company).order_by('-published_date')                    
            return render(request, 'post_view_all.html', {'post': post, 'company': company})
        else:
            messages.error(request, "* You are not authenticated !!")
            return HttpResponseRedirect('/')

@login_required(login_url='/login')
def post_create(request):
    form = Post_Form()
    company = Company.objects.get(user=request.user)
    new_post = True
    if not company.is_verified:
        messages.warning(request,"* You are not verified yet !! ")
        return HttpResponseRedirect('/company/dashboard')
    else:
        if request.method == "POST":
            data = Post_Form(data=request.POST)
            if data.is_valid():
                post = data.save(commit=False)
                post.company = company
                post.save()
                messages.success(request, "Succesfully added your Post.....")
                return HttpResponseRedirect('/post/read/all')
            else:
                raise forms.ValidationError(
                "Invalid Form . Try Again !!"
            )
        return render(request, 'post_create.html', {'form': form, 'new_post': new_post})       


@login_required(login_url='/login')
def post_update(request, id):
    post = Post.objects.get(id=id)
    form = Post_Form(instance=post)
    company = Company.objects.get(user=request.user)
    update_post = True
    if not company.is_verified:
        messages.warning(request, "* You are not verified yet !!")
        return HttpResponseRedirect('/company/dashboard')
    else:
        if request.method == "POST":
            data = Post_Form(data=request.POST, instance=post)
            if data.is_valid():
                post_instance = data.save(commit=False)
                post_instance.company = company
                post_instance.save()
                messages.success(request,"* Post is updated Successfully.....")
                return HttpResponseRedirect('/post/read/all')
            else:
                messages.error(request,"* Invalid data . Try Again !!")
                return HttpResponseRedirect('/cv/read/all')
        return render(request, 'post_create.html', {'form': form, 'update_post': update_post})


@login_required(login_url='/login')
def post_delete(request, id):
    if request.method == "GET":
        post = Post.objects.get(id=id)
        post.delete()
        messages.success(request,"* Successfully deleted your Post.....")
        return HttpResponseRedirect('/post/read/all')


#  CV CRUD

def cv_read_all(request):
    if request.method == "GET":
        if request.user.is_seeker:
            seeker = Seeker.objects.get(user=request.user)
            cv = CV.objects.filter(seeker=seeker).order_by('-upload_date')
            return render(request, 'CV_view_all.html', {'cv': cv, 'seeker': seeker})
        else:
            messages.error(request,"U r not authenticated !!")
            return HttpResponseRedirect('/')

@login_required(login_url='/login')
def cv_create(request):
    form = CV_Form()
    new_cv = True
    if request.method == "POST":
        data = CV_Form(request.POST, request.FILES)
        seeker = Seeker.objects.get(user=request.user)
        if data.is_valid():
            cv = data.save(commit=False)
            cv.seeker = seeker
            cv.save()
            messages.success(request, "* Successfully added your CV ......")
            return HttpResponseRedirect('/cv/read/all')
        else:
            messages.error(request,"* Invalid data . Try Again !!")
            return HttpResponseRedirect('/cv/read/all')
    return render(request, 'cv_create.html', {'form': form, 'new_cv': new_cv})


@login_required(login_url='/login')
def cv_update(request, id):
    cv = CV.objects.get(id=id)
    form = CV_Form(instance=cv)
    seeker = Seeker.objects.get(user=request.user)  
    update_cv = True 
    if request.method == "POST":
        data = CV_Form(request.POST, request.FILES, instance=cv)
        if data.is_valid():
            cv_instance = data.save(commit=False)
            cv_instance.seeker = seeker
            cv_instance.save()
            messages.success(request, "* Successfully updated your CV .....")
            return HttpResponseRedirect('/cv/read/all')
        else:
            messages.error(request,"* Invalid data . Try Again !!")
            return HttpResponseRedirect('/cv/read/all')
    return render(request, 'cv_create.html', {'form': form, 'update_cv': update_cv})


@login_required(login_url='/login')
def cv_delete(request, id):
    if request.method == "GET":
        cv = CV.objects.get(id=id)
        cv.delete()
        messages.success(request,"* Successfully deleted your CV !!")
        return HttpResponseRedirect('/cv/read/all')


def search(request):
    if request.method == 'GET':
        job_request = request.GET['job_request']
        if len(job_request) > 40:
            messages.warning(request, "* Please search within 40 words")
            return HttpResponseRedirect('/search')
        else:
            if Post.objects.filter(vaccant_for__icontains=job_request):
                post_request = Post.objects.filter(vaccant_for__icontains=job_request)
                return render(request, 'search.html', {'post_request': post_request})
            elif Company.objects.filter(cname__icontains=job_request) or\
                    Company.objects.filter(clocation__icontains=job_request) or\
                    Company.objects.filter(ctype__icontains=job_request):
                company = Company.objects.filter(cname__icontains=job_request) or Company.objects.filter(
                    clocation__icontains=job_request) or Company.objects.filter(ctype__icontains=job_request)
                for data in company:
                    post_request = Post.objects.filter(company=data)
                    post_count = post_request.count()
                    if post_count != 0:
                        return render(request, 'search.html', {'post_request': post_request})
                    else:
                        context = {
                            'post_request': post_request, 
                            'post_count': post_count
                        }
                        return render(request, 'search.html', context = context)
            else:
                messages.info(request,"* No Matching Results Found !!")
                return HttpResponseRedirect('/')


#  Application

@login_required(login_url='/login')
def application_view(request):
    if request.method == "GET":               
        if request.user.is_seeker:
            seeker = Seeker.objects.get(user = request.user)
            apps = Application.objects.filter(seeker = seeker).order_by('-apply_date')
            a_seeker = True            
            return render(request, 'application_view.html', {'apps': apps, 'a_seeker': a_seeker})
        elif request.user.is_company:
            company = Company.objects.get(user = request.user)
            apps = Application.objects.filter(company = company).order_by('apply_date')
            a_company = True
            return render(request, 'application_view.html', {'apps': apps, 'a_company': a_company})
        else:
            messages.error(request, "You are not Authentiated !!")
            return HttpResponseRedirect("/")


@login_required(login_url='/login')
def application_create(request, post_id, company_id):
    if request.method == 'GET':
        if request.user.is_seeker:                 
            seeker = Seeker.objects.get(user = request.user)
            post = Post.objects.get(id = post_id)
            company = Company.objects.get(id = company_id)
            cv_applied = CV.objects.filter(seeker = seeker).latest('upload_date')
            if Application.objects.filter(seeker = seeker, post = post).exists():            
                messages.error(request, "You have already applied for the post !!")
                return HttpResponseRedirect('/application/view')    
            else:
                Application.objects.create(seeker = seeker, post = post, company = company, cv_applied = cv_applied)  
                messages.success(request, "Applied Successfully !!")
                return HttpResponseRedirect('/application/view')            
        else:
            messages.error(request, "You are not Authenicated !!")
            return HttpResponseRedirect('/')


@login_required(login_url='/login')
def application_delete(request, app_id):
    if request.method == "GET":
        if request.user.is_seeker:        
            seeker = Seeker.objects.get(user = request.user)
            application = Application.objects.get(seeker = seeker, id = app_id)
            application.delete()
            messages.success(request, "Application Cancelled ..")
            return HttpResponseRedirect('/application/view')
        else:
            messages.error(request, "You are not Authenticated !!")
            return HttpResponseRedirect('/')


@login_required(login_url = '/login')
def accept_application(request, app_id):
    if request.method == 'GET':
        if request.user.is_company:
            company = Company.objects.get(user = request.user)
            Application.objects.filter(company = company, id = app_id).update(status=True)    
            messages.success(request, "You accepted the Application .....")
            return HttpResponseRedirect('/application/view')
        else:
            messages.error(request, "You are not Authenticated !!")
            return HttpResponseRedirect('/')


@login_required(login_url = '/login')
def cancel_application(request, app_id):
    if request.method == 'GET' and request.user.is_company:
        company = Company.objects.get(user = request.user)
        Application.objects.filter(company = company, id = app_id).update(status=False)
        messages.success(request, "You canceled the Application .....")
        return HttpResponseRedirect('/application/view')    
    else:
        messages.error(request, "You are not Authenticated !!")
        return HttpResponseRedirect('/')