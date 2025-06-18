from django.urls import path
from home.views import HomeView, RegisterView

urlpatterns = [
    path(route='', 
        view=HomeView.as_view(), 
        name='index',
    ),
    path(route='register/', 
        view=RegisterView.as_view(), 
        name='register',
    ),
]