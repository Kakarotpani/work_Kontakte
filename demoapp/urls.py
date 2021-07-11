from django.urls import path
from . import views

app_name = 'demoapp'

urlpatterns = [
    path('', views.base, name="base"),
    path('login', views.login_method, name="login"),
    path('logout', views.logout_method, name="logout"),
    path('register/company', views.company_register, name="company_register"),
    path('register/seeker', views.seeker_register, name="seeker_register"),
    path('company/dashboard', views.company_dash, name = "company_dash"),
    path('seeker/dashboard', views.seeker_dash, name = "seeker_dash"),    
    path('profile/view', views.profile_view, name="profile_view"),
    path('profile/update', views.profile_update, name="profile_update"),
    path('profile/delete', views.profile_delete, name="profile_delete"),
    path('post/read/all/', views.post_read_all, name="post_read_all"),
    path('post/create/', views.post_create, name="post_create"),
    path('post/update/<int:id>', views.post_update, name="post_update"),
    path('post/delete/<int:id>', views.post_delete, name="post_delete"),
    path('cv/read/all', views.cv_read_all, name="cv_read_all"),
    path('cv/create/', views.cv_create, name="cv_create"),
    path('cv/update/<int:id>', views.cv_update, name="cv_update"),
    path('cv/delete/<int:id>', views.cv_delete, name="cv_delete"),
    path('search', views.search, name="search"),
    path('company/detail/<int:c_id>', views.company_detail, name = 'company_detail'),
    path('seeker/detail/<int:s_id>', views.seeker_detail, name = 'seeker_detail'),
    path('post/detail/<int:id>', views.post_detail, name = 'post_detail'),
    path('posts/all', views.all_posts, name="all_posts"),
    path('application/view', views.application_view, name= "application_view"),
    path('application/create/<int:post_id>/<int:company_id>', views.application_create, name = "application_create"),
    path('application/delete/<int:app_id>', views.application_delete, name = 'application_delete'),
    path('application/accept/<int:app_id>', views.accept_application, name = 'accept_application'),
    path('application/cancel/<int:app_id>', views.cancel_application, name = 'cancel_application'),

]

