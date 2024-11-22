from django.contrib import admin
from django.urls import path
from tracker import views
from tracker import auth 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('register/', auth.register_user, name='register'), 
]
