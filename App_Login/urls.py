from django.urls import path
from App_Login import views 

app_name="App_Login"

urlpatterns=[
    path('registration/',views.RegistrationView,name='registration'),
    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('profile/',views.ProfileView,name='profile'),
    path('activate/<uidbd64>/<token>/',views.activate,name='activate'),
]