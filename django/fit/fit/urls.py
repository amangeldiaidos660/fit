# from django.contrib import admin
from django.urls import path
from tracker import views, auth, user

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('register/', auth.register_user, name='register'), 
    path('main/', views.main, name='main'),
    path('auth/', auth.login_view, name="auth"),
    path('user_data/', user.get_user_data, name='get_user_data'),
    path('logout/', user.logout_view, name='logout'),
    path('workout_types/', user.get_workout_types, name='get_workout_types'),
    path('get_progress/', user.get_progress, name='get_progress'),

    

]
