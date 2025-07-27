from django.urls import path, include
from home.views import HomeView, RegisterView, LogoutView, LoginView, PerfilView

urlpatterns = [
    path(route='', 
        view=HomeView.as_view(), 
        name='index',
    ),
    path(route='register/', 
        view=RegisterView.as_view(), 
        name='register',
    ),
    path(route='login/', 
        view=LoginView.as_view(), 
        name='login',
    ),
    path(route='logout/',
        view=LogoutView.as_view(),
        name='logout',
    ),
    path(route='perfil/',
        view=PerfilView.as_view(),
        name='perfil',
    ),
    path('i18n/', include('django.conf.urls.i18n')), 
]